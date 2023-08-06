"""Flask blueprint and functions for managing jobs"""

from __future__ import annotations

__all__ = ('bp', 'create_job', 'get_status', 'cancel_job')

import pathlib
import re
from typing import cast, TYPE_CHECKING

import flask
import celery.states

from . import db_util, task
from .error import http_error, JobNotFoundError
from .util import has_path_seps, StatusEnum

if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Any, Union
    from uuid import UUID

bp = flask.Blueprint('job', __name__)


def _check_outtmpl_dir(outtmpl: Union[str, dict[str, str]]) -> None:
    """Verifies that 'outtmpl' isn't being used to escape the download
    dir

    It works by verifying that 'outtmpl' is a child path within the
    download dir

    Also verifies the type of 'outtmpl'

    'outtmpl' can be a dict when using yt-dlp. In this case, every path
    in the dict is checked

    This function is safe to use with 'outtmpl' because youtube-dl
    removes path separators before injecting values into the template
    """
    config = flask.current_app.config['YTDL_CONFIG']

    if not config.force_download_dir:
        # Only check `outtmpl` if the relevant config option is enabled
        return

    if isinstance(outtmpl, str):
        # Convert str values to a single-item dict so we can iterate
        # over it
        #
        # The value of the key is unimportant
        outtmpl = {
            '_': outtmpl
        }
    elif not isinstance(outtmpl, dict):
        raise http_error.YTDLOptionBadValue(
            'outtmpl', 400, description=(
                "The ytdl_opt 'outtmpl' must be either a string or "
                'an object of strings'
            )
        )

    download_dir = config.download_dir
    parent_dir = pathlib.Path(download_dir).resolve()

    for filepath in outtmpl.values():
        if not isinstance(filepath, str):
            raise http_error.YTDLOptionBadValue(
                'outtmpl', 400, description=(
                    "All values within the 'outtmpl' object must be strings. "
                    f'Invalid value: {filepath!r}'
                )
            )

        # Append the download dir to the child path only if the child
        # path is relative
        if pathlib.Path(filepath).is_absolute():
            child_path = pathlib.Path(filepath).resolve()
        else:
            child_path = pathlib.Path(download_dir, filepath).resolve()

        if (
            parent_dir == child_path or
            not child_path.is_relative_to(parent_dir)
        ):
            raise http_error.YTDLOptionBadValue(
                'outtmpl', 403, description=(
                    "The ytdl_opt 'outtmpl' must be either a relative path or "
                    'a subpath of the download directory. '
                    f'Download directory: {download_dir!r}. '
                    f'Invalid path: {filepath!r}'
                )
            )


def _check_path_seps(opt_name: str, opt_value: str) -> None:
    """Verifies that the given ytdl_opt doesn't contain path separators

    Used for the following ytdl_opts:
        'outtmpl_na_placeholder', 'merge_output_format', 'final_ext'

    Path seperators are removed because these options can escape the
    download dir if a value such as '../../..' is given

    Unlike 'outtmpl', youtube-dl does not remove path separators when
    injecting variables into the template, so we can't use the parent
    method like in `_check_outtmpl_dir()`
    """
    config = flask.current_app.config['YTDL_CONFIG']
    if not config.force_download_dir:
        # Only check for separators if the relevant config option is
        # enabled
        return

    if not isinstance(opt_value, str):
        raise http_error.YTDLOptionBadValue(
            opt_name, 400,
            description=f'The ytdl_opt {opt_name!r} must be a string'
        )

    if has_path_seps(opt_value):
        raise http_error.YTDLOptionBadValue(
            opt_name, 403, description=(
                f'The ytdl_opt {opt_name!r} must not contain path separators'
            )
        )


def _create_job_check_input() -> None:
    """Verify that the user input received by `create_job()` is valid

    If the input is valid, it returns `None`

    If the input isn't valid, it raises `http_error.HTTPError`, which
    should be returned to the user as the response data.
    """
    # Assert that the request data is the right type
    if not isinstance(flask.request.json, dict):
        raise http_error.DataBadType(dict)

    # Assert that 'urls' exists in the request data
    if 'urls' not in flask.request.json:
        raise http_error.DataMissingKey('urls')

    urls = flask.request.json['urls']

    # Assert that 'urls' is a non-empty list
    if not isinstance(urls, list):
        raise http_error.KeyBadType('urls', list)
    if not urls:
        raise http_error.KeyBadValue(
            'urls', description="The 'urls' array must not be empty"
        )

    # Check user-supplied ytdl_opts
    ytdl_user_opts = flask.request.json.get('ytdl_opts', None)
    if ytdl_user_opts is not None:
        _check_ytdl_user_opts(ytdl_user_opts)

    # Check custom_opts
    custom_opts = flask.request.json.get('custom_opts', None)
    if custom_opts is not None:
        _check_custom_opts(custom_opts)


def _check_ytdl_user_opts(ytdl_user_opts: Any) -> None:
    """Verify that the user-supplied ytdl_opts are valid

    Raises `http_error.HTTPError` if the ytdl_opts are invalid
    """
    if not isinstance(ytdl_user_opts, dict):
        raise http_error.KeyBadType('ytdl_opts', dict)
    if not ytdl_user_opts:
        # Skip checks if `ytdl_user_opts` is empty
        return None

    config = flask.current_app.config['YTDL_CONFIG']
    logger = flask.current_app.logger

    if not config.allow_user_opts:
        raise http_error.YTDLUserOptionsNotAllowed('ytdl_opts')

    if config.ytdl_enable_whitelist:
        allowed_opts = set(config.ytdl_whitelist)
        allowed_opts |= config.ytdl_whitelist_add
        allowed_opts -= config.ytdl_whitelist_remove

        for opt in ytdl_user_opts:
            if opt not in allowed_opts:
                raise http_error.ForbiddenYTDLOption(opt)

    # Check the value of individual ytdl_opts
    try:
        if 'outtmpl' in ytdl_user_opts:
            _check_outtmpl_dir(ytdl_user_opts['outtmpl'])

        for opt in (
            'outtmpl_na_placeholder', 'merge_output_format', 'final_ext'
        ):
            if opt in ytdl_user_opts:
                _check_path_seps(opt, ytdl_user_opts[opt])
    except http_error.YTDLOptionBadValue as e:
        # Log the error before re-raising it
        logger.debug(
            'create_job: %s: Invalid user-supplied ytdl_opt. Aborting',
            e.option
        )
        raise


def _check_custom_opt_extractaudio(custom_opts: Mapping[str, Any]) -> None:
    """Check the extractaudio custom_opt"""
    extractaudio = custom_opts.get('extractaudio', None)
    if extractaudio is None:
        return

    if not isinstance(extractaudio, dict):
        raise http_error.CustomOptionBadValue(
            'extractaudio', 400,
            description='Option must be an object or null'
        )

    audio_opts = (
        ('audioformat', str), ('audioquality', int),
        ('nopostoverwrites', bool)
    )
    for field, type_ in audio_opts:
        if field in extractaudio:
            value = extractaudio[field]
            if not isinstance(value, type_):
                type_name = http_error.INDEFINITE_TYPE_NAMES[type_]
                raise http_error.CustomOptionBadValue(
                    'extractaudio', 400,
                    description=f'The field {field!r} must be {type_name}'
                )

    if 'audioquality' in extractaudio and extractaudio['audioquality'] < 0:
        raise http_error.CustomOptionBadValue(
            'extractaudio', 400,
            description="The field 'audioquality' cannot be less than zero"
        )


def _check_custom_opt_split_chapters(custom_opts: Mapping[str, Any]) -> None:
    """Check the split_chapters custom_opt"""
    split_chapters = custom_opts.get('split_chapters', None)
    if split_chapters is None:
        return

    if not isinstance(split_chapters, dict):
        raise http_error.CustomOptionBadValue(
            'split_chapters', 400,
            description='Option must be an object or null'
        )

    force_keyframes = split_chapters.get('force_keyframes', None)
    if (
        force_keyframes is not None and
        not isinstance(force_keyframes, bool)
    ):
        if not isinstance(force_keyframes, bool):
            raise http_error.CustomOptionBadValue(
                'split_chapters', 400, description=(
                    "The field 'force_keyframes' must be a boolean or null"
                )
            )


def _check_custom_opt_remove_chapters(custom_opts: Mapping[str, Any]) -> None:
    """Check the remove_chapters custom_opt"""
    remove_chapters = custom_opts.get('remove_chapters', None)
    if remove_chapters is None:
        return

    if not isinstance(remove_chapters, dict):
        raise http_error.CustomOptionBadValue(
            'remove_chapters', 400,
            description='Option must be an object or null'
        )

    patterns = remove_chapters.get('patterns', None)
    ranges = remove_chapters.get('ranges', None)
    if not patterns and not ranges:
        raise http_error.CustomOptionBadValue(
            'remove_chapters', 400, description=(
                "The 'patterns' and/or 'ranges' fields must be non-empty "
                'arrays'
            )
        )

    if patterns is not None and not isinstance(patterns, list):
        raise http_error.CustomOptionBadValue(
            'remove_chapters', 400,
            description="The field 'patterns' must be an array or null"
        )
    if ranges is not None and not isinstance(ranges, list):
        raise http_error.CustomOptionBadValue(
            'remove_chapters', 400,
            description="The field 'ranges' must be an array or null"
        )

    if patterns:
        for pattern in patterns:
            if not isinstance(pattern, str):
                raise http_error.CustomOptionBadValue(
                    'remove_chapters', 400, description=(
                        "The field 'patterns' must only contain strings"
                    )
                )

            try:
                re.compile(pattern)
            except re.error:
                raise http_error.CustomOptionBadValue(
                    'remove_chapters', 400, description=(
                        "The field 'patterns' contains an invalid regular "
                        f'expression: {pattern}'
                    )
                )

    if ranges:
        for range_ in ranges:
            if not isinstance(range_, list):
                raise http_error.CustomOptionBadValue(
                    'remove_chapters', 400, description=(
                        "The field 'ranges' must only contain number-pair "
                        'arrays'
                    )
                )

            length = len(range_)
            if length != 2:
                raise http_error.CustomOptionBadValue(
                    'remove_chapters', 400, description=(
                        "The field 'ranges' contains an array with an "
                        f'invalid length. Expected 2. Got {length}'
                    )
                )

            for number in range_:
                if not isinstance(number, (int, float)):
                    raise http_error.CustomOptionBadValue(
                        'remove_chapters', 400, description=(
                            "The field 'ranges' contains an array with an "
                            'invalid type. Expected an array of numbers, '
                            f'not {range_}'
                        )
                    )

                if number < 0:
                    raise http_error.CustomOptionBadValue(
                        'remove_chapters', 400, description=(
                            "The field 'ranges' contains an array with a "
                            f'negative number: {range_}. Numbers must be '
                            'positive or zero'
                        )
                    )

            if range_[0] >= range_[1]:
                raise http_error.CustomOptionBadValue(
                    'remove_chapters', 400, description=(
                        "The field 'ranges' contains an array where the "
                        f'start is greater than the end: {range_}'
                    )
                )

    force_keyframes = remove_chapters.get('force_keyframes', None)
    if (
        force_keyframes is not None and
        not isinstance(force_keyframes, bool)
    ):
        raise http_error.CustomOptionBadValue(
            'remove_chapters', 400, description=(
                "The field 'force_keyframes' must be a boolean or null"
            )
        )


def _check_custom_opt_parse_metadata(custom_opts: Mapping[str, Any]) -> None:
    """Check the parse_metadata custom_opt"""
    parse_metadata = custom_opts.get('parse_metadata', None)
    if parse_metadata is None:
        return

    if not isinstance(parse_metadata, list):
        raise http_error.CustomOptionBadValue(
            'parse_metadata', 400,
            description='Option must be an array or null'
        )

    for interpreter in parse_metadata:
        if not isinstance(interpreter, dict):
            raise http_error.CustomOptionBadValue(
                'parse_metadata', 400,
                description='Option must only contain objects'
            )

        for field in ('from', 'to'):
            if field not in interpreter:
                raise http_error.CustomOptionBadValue(
                    'parse_metadata', 400,
                    description=f'Missing field: {field}'
                )

            value = interpreter[field]
            if not isinstance(value, str):
                raise http_error.CustomOptionBadValue(
                    'parse_metadata', 400,
                    description=f'The field {field!r} must be a string'
                )


def _check_custom_opt_replace_in_metadata(
    custom_opts: Mapping[str, Any]
) -> None:
    """Check the replace_in_metadata custom_opt"""
    replace_in_metadata = custom_opts.get('replace_in_metadata', None)
    if replace_in_metadata is None:
        return

    if not isinstance(replace_in_metadata, list):
        raise http_error.CustomOptionBadValue(
            'replace_in_metadata', 400,
            description='Option must be an array or null'
        )

    for replacer in replace_in_metadata:
        if not isinstance(replacer, dict):
            raise http_error.CustomOptionBadValue(
                'replace_in_metadata', 400,
                description='Option must only contain objects'
            )

        fields = (
            ('fields', list),
            ('regex', str),
            ('replace', str)
        )
        for field, type_ in fields:
            if field not in replacer:
                raise http_error.CustomOptionBadValue(
                    'replace_in_metadata', 400,
                    description=f'Missing field: {field}'
                )

            value = replacer[field]
            if not isinstance(value, type_):
                type_name = http_error.INDEFINITE_TYPE_NAMES[type_]
                raise http_error.CustomOptionBadValue(
                    'replace_in_metadata', 400,
                    description=f'The field {field!r} must be {type_name}'
                )

        for field in replacer['fields']:
            if not isinstance(field, str):
                raise http_error.CustomOptionBadValue(
                    'replace_in_metadata', 400,
                    description=(
                        "The field 'fields' must be an array of strings. "
                        f'Unexpected value: {field!r}'
                    )
                )


def _check_custom_opt_sponsorblock(custom_opts: Mapping[str, Any]) -> None:
    """Check the sponsorblock custom_opt"""
    sponsorblock = custom_opts.get('sponsorblock', None)
    if sponsorblock is None:
        return

    if not isinstance(sponsorblock, dict):
        raise http_error.CustomOptionBadValue(
            'sponsorblock', 400,
            description='Option must be an object or null'
        )

    mark = sponsorblock.get('mark', None)
    remove = sponsorblock.get('remove', None)

    if not mark and not remove:
        raise http_error.CustomOptionBadValue(
            'sponsorblock', 400, description=(
                "The 'mark' and/or 'remove' fields must be non-empty arrays"
            )
        )

    if mark is not None and not isinstance(mark, list):
        raise http_error.CustomOptionBadValue(
            'sponsorblock', 400,
            description="The field 'mark' must be an array or null"
        )
    if remove is not None and not isinstance(remove, list):
        raise http_error.CustomOptionBadValue(
            'sponsorblock', 400,
            description="The field 'remove' must be an array or null"
        )

    if mark:
        for category in mark:
            if not isinstance(category, str):
                raise http_error.CustomOptionBadValue(
                    'sponsorblock', 400, description=(
                        "The field 'mark' must only contain strings"
                    )
                )
    if remove:
        for category in remove:
            if not isinstance(category, str):
                raise http_error.CustomOptionBadValue(
                    'sponsorblock', 400, description=(
                        "The field 'remove' must only contain strings"
                    )
                )

    for field in ('template', 'api'):
        value = sponsorblock.get(field, None)
        if value is not None and not isinstance(value, str):
            raise http_error.CustomOptionBadValue(
                'sponsorblock', 400,
                description=f'The field {field} must be a string or null'
            )

    force_keyframes = sponsorblock.get('force_keyframes', None)
    if (
        force_keyframes is not None and
        not isinstance(force_keyframes, bool)
    ):
        if not isinstance(force_keyframes, bool):
            raise http_error.CustomOptionBadValue(
                'sponsorblock', 400, description=(
                    "The field 'force_keyframes' must be a boolean or null"
                )
            )


def _check_custom_opts(custom_opts: Any) -> None:
    """Verify that the user-supplied custom_opts are valid

    Raises `http_error.HTTPError` if the custom_opts are invalid
    """
    if not isinstance(custom_opts, dict):
        raise http_error.KeyBadType('custom_opts', dict)
    if not custom_opts:
        # Skip checks if `custom_opts` is empty
        return None

    config = flask.current_app.config['YTDL_CONFIG']
    logger = flask.current_app.logger

    # Verify that user-supplied custom_opts is allowed
    if not config.allow_user_opts:
        raise http_error.YTDLUserOptionsNotAllowed('custom_opts')

    # Verify that there are no non-whitelisted custom_opts
    if config.custom_enable_whitelist:
        for opt in custom_opts:
            if opt not in config.custom_whitelist:
                raise http_error.ForbiddenCustomOption(opt)

    # Check custom_opts that are supposed to be a str
    for opt in (
        'dateafter', 'datebefore', 'metafromtitle', 'remuxvideo',
        'recodevideo', 'convertsubtitles', 'convertthumbnails'
    ):
        value = custom_opts.get(opt, None)
        if value is not None and not isinstance(value, str):
            raise http_error.CustomOptionBadValue(
                opt, 400, description='Option must be a string or null'
            )

    # Check custom_opts that are supposed to be bools
    for opt in (
        'addmetadata', 'addchapters', 'embedsubtitles', 'embedthumbnail',
        'xattrs'
    ):
        if opt in custom_opts:
            value = custom_opts.get(opt, None)
            if value is not None and not isinstance(value, bool):
                raise http_error.CustomOptionBadValue(
                    opt, 400, description='Option must be a bool or null'
                )

    # Verify that vulnerable custom_opts don't contain path separators
    if config.force_download_dir:
        for opt in (
            'remuxvideo', 'recodevideo', 'convertsubtitles',
            'convertthumbnails'
        ):
            value = custom_opts.get(opt, None)
            if value is not None and has_path_seps(value):
                raise http_error.CustomOptionBadValue(
                    opt, 403,
                    description='Option must not contain path separators'
                )

    # Check individual custom_opts
    try:
        _check_custom_opt_extractaudio(custom_opts)
        _check_custom_opt_split_chapters(custom_opts)
        _check_custom_opt_remove_chapters(custom_opts)
        _check_custom_opt_parse_metadata(custom_opts)
        _check_custom_opt_replace_in_metadata(custom_opts)
        _check_custom_opt_sponsorblock(custom_opts)
    except http_error.CustomOptionBadValue as e:
        # Log the error before re-raising it
        logger.debug(
            'create_job: %s: Invalid user-supplied custom_opt. Aborting',
            e.option
        )
        raise


def _cancel_job_check_input() -> None:
    """Verify that the user input received by `cancel_job()` is valid

    If the input isn't valid, it raises `http_error.HTTPError`, which
    should be returned to the user as the response data.
    """
    # Assert that the request data is the right type
    if not isinstance(flask.request.json, dict):
        raise http_error.DataBadType(dict)

    # Assert that 'status' exists in the request data
    if 'status' not in flask.request.json:
        raise http_error.DataMissingKey('status')

    status = flask.request.json['status']

    # Assert that the status is the proper value
    if status != StatusEnum.cancelled.name:
        raise http_error.KeyBadValue(
            'status', description=f'Unsupported status: {status}'
        )


@bp.route('/', methods=('POST',))
def create_job() -> tuple[dict[str, Any], int]:
    """Create a new job

    The request data must be a json object that matches the below format
        {
            "urls": [ "video1", "video2", "video3" ]
            "ytdl_opts": { ... }
            "custom_opts": { ... }
        }
    `ytdl_opts` is an optional object containing options that will be
    passed directly to youtube-dl

    `custom_opts` is an optional object containing custom ytdl options.
    See the documentation for more info

    `ytdl_opts` and `custom_opts` may be disabled or restricted
    depending on the server configuration
    """
    try:
        _create_job_check_input()
    except http_error.HTTPError as e:
        return e.to_dict(), e.code

    config = flask.current_app.config['YTDL_CONFIG']
    logger = flask.current_app.logger

    # Override type of the request json because it was verified in
    # `_create_job_check_input()`
    request_data = cast('dict[str, Any]', flask.request.json)
    urls = request_data['urls']
    ytdl_user_opts = request_data.get('ytdl_opts') or {}
    custom_user_opts = request_data.get('custom_opts') or {}

    logger.info('create_job: creating job')

    ytdl_opts = config.ytdl_default_opts | ytdl_user_opts
    custom_opts = config.custom_default_opts | custom_user_opts

    job_id = db_util.insert_job(urls=urls)
    logger.info('create_job: job_id: %s', job_id)

    logger.debug('create_job: %s: queuing task', job_id)
    task.download.apply_async(task_id=str(job_id), kwargs={
        'urls': urls,
        'ytdl_opts': ytdl_opts,
        'custom_opts': custom_opts,
        'sensitive_opts': config.ytdl_sensitive_opts,
        'download_dir': config.download_dir,
        'ytdl_module': config.ytdl_module,
        'ytdl_class': config.ytdl_class,
        'daterange_module': config.daterange_module,
        'daterange_class': config.daterange_class,
        'metadata_module': config.metadata_module,
        'metadata_class': config.metadata_class
    })

    # Return once the task is queued
    return {
        'id': job_id,
        'status_url': flask.url_for(
            '.get_status', job_id=job_id, _external=True
        )
    }, 202


@bp.route('/<uuid:job_id>', methods=('GET',))
def get_status(job_id: UUID) -> tuple[dict[str, Any], int]:
    """Get information about an existing job"""
    logger = flask.current_app.logger

    logger.debug('get_status: %s: Getting job status', job_id)
    try:
        job = db_util.get_job(job_id)
    except JobNotFoundError:
        logger.debug('get_status: %s: Job not found. Aborting', job_id)
        return_data = http_error.JobNotFound(job_id)
        return return_data.to_dict(), return_data.code

    logger.debug('get_status: %s: Getting logs', job_id)
    job.logs = db_util.get_logs(job_id)

    logger.debug('get_status: %s: Getting progress', job_id)
    job.progress = db_util.get_progress(job_id)

    return job.get_json(), 200


@bp.route('/<uuid:job_id>', methods=('PATCH',))
def cancel_job(job_id: UUID) -> tuple[dict[str, Any], int]:
    """Asynchronously cancel the given job by aborting the Celery task

    Does not wait for the job to be cancelled. The user must check the
    status of the job via `get_status()` if they want to know when it
    actually gets cancelled

    The request data must be a json object that matches the below format
        {
            "status": "cancelled"
        }
    """
    try:
        _cancel_job_check_input()
    except http_error.HTTPError as e:
        return e.to_dict(), e.code

    logger = flask.current_app.logger

    logger.debug('cancel_job: %s: Getting job status', job_id)
    try:
        status = db_util.get_job_status(job_id)
    except JobNotFoundError:
        logger.debug('cancel_job: %s: Job not found. exiting', job_id)
        return_data: http_error.HTTPError = http_error.JobNotFound(job_id)
        return return_data.to_dict(), return_data.code
    logger.debug('cancel_job: %s: Job status: %s', job_id, status.name)

    # Assert that the job is currently running
    if status in {StatusEnum.finished, StatusEnum.error, StatusEnum.timeout}:
        logger.debug('cancel_job: %s: Job already completed. Exiting', job_id)
        return_data = http_error.JobAlreadyCompleted(
            job_id, flask.url_for('.get_status', job_id=job_id, _external=True)
        )
        return return_data.to_dict(), return_data.code

    # Return if the job was already cancelled
    if status is StatusEnum.cancelled:
        logger.debug(
            'cancel_job: %s: Job is already cancelled. Exiting', job_id
        )
        return {
            'id': job_id,
            'status_url': flask.url_for(
                '.get_status', job_id=job_id, _external=True
            ),
            'description': (
                'The job is already cancelled. No action has been taken'
            )
        }, 200

    logger.debug('cancel_job: %s: Retrieving Celery task result', job_id)
    result = task.download.AsyncResult(str(job_id))
    logger.debug('cancel_job: %s: Task state: %r', job_id, result.state)

    # Return if the Celery task was already aborted
    #
    # Aborts are asynchronous, so the task doesn't always exit right
    # away, but the state updates immediately when `abort()` is called
    if result.state == 'ABORTED':
        logger.debug(
            'cancel_job: %s: Task was already aborted. Exiting', job_id
        )
        return {
            'id': job_id,
            'status_url': flask.url_for(
                '.get_status', job_id=job_id, _external=True
            ),
            'description': 'The job is already pending cancellation'
        }, 202

    # READY_STATES value: {'REVOKED', 'FAILURE', 'SUCCESS'}
    if result.state in celery.states.READY_STATES:
        logger.error(
            'cancel_job: %s: Task state: %r, Job status: %r: '
            'Celery task already completed, but the job status indicates that '
            'it should still be running. The task probably crashed '
            'unexpectedly',
            job_id, result.state, status.name
        )
        return_data = http_error.JobNotRunning(
            job_id, flask.url_for('.get_status', job_id=job_id, _external=True)
        )
        return return_data.to_dict(), return_data.code

    logger.info('cancel_job: %s: Aborting task', job_id)
    result.abort()

    return {
        'id': job_id,
        'status_url': flask.url_for(
            '.get_status', job_id=job_id, _external=True
        ),
        'description': 'The job is pending cancellation'
    }, 202
