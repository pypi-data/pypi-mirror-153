"""Celery tasks"""

from __future__ import annotations

__all__ = ('download', 'TaskArgs')

import os
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

# billiard is used because it allows tasks to create child processes
from billiard import Process
from celery.exceptions import SoftTimeLimitExceeded
from celery.utils.log import get_task_logger

from . import db_util
from .celery import app
from .custom_opt import load_custom_opts, merge_custom_opts
from .database import db
from .util import import_object, StatusEnum, terminate
from .ytdl import Downloader, censor_opts

if TYPE_CHECKING:
    from logging import Logger
    from typing import Any, Iterable, Mapping, Sequence

    from .type import Terminatable

_logger = get_task_logger(__name__)


# Ignore typing error about the decorator being untyped
@app.task(bind=True)  # type: ignore[misc]
def download(
    self: Any, *, urls: Sequence[str], ytdl_opts: Mapping[str, Any],
    custom_opts: Mapping[str, Any], sensitive_opts: Iterable[str],
    download_dir: str, ytdl_module: str, ytdl_class: str,
    daterange_module: str, daterange_class: str, metadata_module: str,
    metadata_class: str
) -> None:
    """Download the given URLs via youtube-dl

    See `TaskArgs` for a documentation about the args

    `db_util.insert_job()` must be called first so that the job exists
    in the database
    """
    try:
        args = TaskArgs(
            urls=urls, ytdl_opts=ytdl_opts, custom_opts=custom_opts,
            sensitive_opts=sensitive_opts, download_dir=download_dir,
            ytdl_module=ytdl_module, ytdl_class=ytdl_class,
            daterange_module=daterange_module, daterange_class=daterange_class,
            metadata_module=metadata_module, metadata_class=metadata_class,
            logger=_logger
        )
        _real_download(self, args)
    except Exception:
        # Log unexpected errors, and set the job status to 'error'
        _logger.exception('Celery task failed')
        job_id = UUID(self.request.id)
        _set_job_status(job_id, StatusEnum.error)


@dataclass(frozen=True)
class TaskArgs:
    """Dataclass of arguments to pass to `_real_download()`

    This isn't used for `download()` because it's not JSONable
    """

    urls: Sequence[str]
    """List of URLs to download"""
    ytdl_opts: Mapping[str, Any]
    """ytdl_opts to pass to the YoutubeDL class

    custom_opts will be merged into this after they're parsed
    """
    custom_opts: Mapping[str, Any]
    """custom_opts that will be merged with ytdl_opts"""
    sensitive_opts: Iterable[str]
    """List of sensitive ytdl_opts, which will be censored before being
    added to the SQL database"""
    download_dir: str
    """Default download directory"""
    ytdl_module: str
    """Name of the module that ytdl_class will be imported from"""
    ytdl_class: str
    """Name of the YoutubeDL class"""
    daterange_module: str
    """Name of the module that daterange_class will be imported from"""
    daterange_class: str
    """Name of the DateRange class"""
    metadata_module: str
    """Name of the module that metadata_class will be imported from"""
    metadata_class: str
    """Name of the MetadataParserPP class"""

    logger: Logger
    """Logger to use for logging

    This is used by functions within `custom_opt` so that they don't
    depend on Celery. The `task` module uses the Celery logger directly.
    """


def _real_download(task: Any, args: TaskArgs) -> None:
    """Used by `download()` to download the URLs within a try-clause"""
    job_id = UUID(task.request.id)

    if task.is_aborted():
        _logger.info('Task aborted before the download started. Exiting')
        _set_job_status(job_id, StatusEnum.cancelled)
        return

    _logger.debug(
        'Importing youtube-dl class %r from module %r',
        args.ytdl_class, args.ytdl_module
    )
    YoutubeDL = import_object(args.ytdl_module, args.ytdl_class)

    _logger.debug('Changing to download dir: %s', args.download_dir)
    os.chdir(args.download_dir)

    _logger.debug('Loading custom_opts: %r', args.custom_opts)
    loaded_custom_opts = load_custom_opts(args)
    _logger.debug('Loaded custom_opts. Result: %r', loaded_custom_opts)

    merged_ytdl_opts = merge_custom_opts(args.ytdl_opts, loaded_custom_opts)

    censored_opts = censor_opts(merged_ytdl_opts, args.sensitive_opts)
    _logger.debug('Censored ytdl_opts: %r', censored_opts)
    db_util.update_job(job_id, ytdl_opts=censored_opts)

    # Run the downloader as a child process so that we can kill it if
    # the task is aborted or times out.
    downloader = Downloader(
        job_id=job_id, urls=args.urls,
        ytdl_opts=merged_ytdl_opts, ytdl_class=YoutubeDL,
        logger=_logger
    )
    process = Process(target=downloader.download)

    # Reset the DB connection pool so that the pool isn't shared with
    # the child process. Sharing the pool causes intermittent errors.
    #
    # More info:
    #   https://docs.sqlalchemy.org/en/14/core/pooling.html#using-connection-pools-with-multiprocessing-or-os-fork
    #
    # This must be called in the parent instead of the child because
    # calling it in the child doesn't completely eliminate the errors if
    # the parent accesses the pool after forking.
    db.engine.dispose()

    try:
        _logger.debug('Starting YTDL process')
        process.start()
        _logger.debug('Child PID: %s', process.pid)
        _ytdl_loop(job_id, process, task)
    # TODO: Add tests for this
    except SoftTimeLimitExceeded:
        # The time limit is configured via the `task_soft_time_limit`
        # Celery option
        _logger.warning('Task timed out. Terminating the YTDL process')
        terminate(process)
        _logger.debug('Process successfully terminated')
        _set_job_status(job_id, StatusEnum.timeout)


def _ytdl_loop(job_id: UUID, process: Terminatable, task: Any) -> None:
    """Continuously check the status of the YTDL process until it either
    exits or is aborted"""
    while True:
        # sleep() is used instead of join() because of this issue:
        # https://github.com/celery/billiard/issues/270
        time.sleep(1)
        # process.join(1)

        if not process.is_alive():
            _logger.info("YTDL process isn't running. Exiting")
            break

        if task.is_aborted():
            _logger.info('Task aborted. Terminating the YTDL process')
            terminate(process)
            _logger.debug('Process successfully terminated')
            _set_job_status(job_id, StatusEnum.cancelled)
            break


def _set_job_status(job_id: UUID, status: StatusEnum) -> None:
    """Set the status of the given job

    Also sets the 'finished' column to the current time
    """
    _logger.debug('Setting job status to %r', status.name)
    db_util.update_job(
        job_id, status=status, finished=db_util.CURRENT_TIMESTAMP
    )
