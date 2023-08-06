"""Manage custom_opts and convert them to ytdl_opts"""

from __future__ import annotations

__all__ = ('CustomOpt', 'CUSTOM_OPTS', 'load_custom_opts', 'merge_custom_opts')

import re
from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

from .util import import_object

if TYPE_CHECKING:
    from collections.abc import Callable, Generator, Iterable, Mapping
    from typing import Any, Final, Optional, Union

    from .task import TaskArgs
    from .type import ParseMetadataDict, ReplaceInMetadataDict


def load_custom_opts(args: TaskArgs) -> dict[str, Any]:
    """Convert the custom_opts dict into a ytdl_opts dict that can be
    passed to `ytdl.Downloader`"""
    loaded_opts: list[dict[str, Any]] = []
    merged_opts: dict[str, Any] = {}

    for opt in CUSTOM_OPTS:
        loaded = opt.load(args)
        if loaded:
            loaded_opts.append(loaded)

    # Merge the loaded opts
    #
    # The postprocessors lists are combined together at the end so that
    # they don't overwrite each other
    postprocessors = []
    for loaded in loaded_opts:
        if 'postprocessors' in loaded:
            postprocessors += loaded.pop('postprocessors')
        merged_opts |= loaded
    if postprocessors:
        merged_opts['postprocessors'] = postprocessors

    return merged_opts


def merge_custom_opts(
    ytdl_opts: Mapping[str, Any], loaded_custom_opts: Mapping[str, Any]
) -> dict[str, Any]:
    """Merge the loaded custom_opts into ytdl_opts

    For conflicting keys, the value in loaded_custom_opts will be used

    If both mappings contain the 'postprocessors' list, the ytdl_opts
    list will be appended to the loaded_custom_opts dict instead of
    overwriting it.
    This prevents custom_opts from overwriting postprocessors completely
    """
    PP: Final = 'postprocessors'
    postprocessors: Optional[tuple[Any, ...]] = None

    # Only merge the postprocessor lists if they're both sequences so
    # that it doesn't break if the user sets it to a weird type
    if (
        PP in ytdl_opts and PP in loaded_custom_opts and
        isinstance(ytdl_opts[PP], Sequence) and
        isinstance(loaded_custom_opts[PP], Sequence)
    ):
        postprocessors = tuple(loaded_custom_opts[PP]) + tuple(ytdl_opts[PP])

    merged_opts = dict(ytdl_opts)
    merged_opts |= loaded_custom_opts
    if postprocessors is not None:
        merged_opts[PP] = postprocessors

    return merged_opts


@dataclass(frozen=True)
class CustomOpt:
    """Dataclass for handling custom_opts and merging them into
    ytdl_opts"""

    custom_opts: tuple[str, ...]
    """List of custom_opts that are handled by this instance

    `handler` will only be called if *any* of these custom_opts are
    given by the user and their value isn't `None`
    """
    handler: Callable[[TaskArgs], Optional[dict[str, Any]]]
    """The function that will be used to load the custom_opts

    The function should return a dict of ytdl_opts, which will be merged
    into the final ytdl_opts.
    It can also return `None` if no options should be added
    """

    def load(self, args: TaskArgs) -> Optional[dict[str, Any]]:
        """Load the custom_opts based on the given TaskArgs

        Returns `None` if the custom_opts within `args` does not contain
        any corresponding custom_opts
        """
        for opt in self.custom_opts:
            if opt in args.custom_opts and args.custom_opts[opt] is not None:
                # mypy incorrectly infers the type of callable objects
                # when using a frozen dataclass:
                # https://github.com/python/mypy/issues/7404
                return self.handler(args)  # type: ignore
        else:
            return None


def _load_daterange(args: TaskArgs) -> dict[str, Any]:
    """Use 'dateafter' and 'datebefore' to create a DateRange object,
    which is assigned to the 'daterange' ytdl_opt

    'daterange' can't be given directly as a ytdl_opt because it's not
    JSONable
    """
    DateRange = import_object(args.daterange_module, args.daterange_class)
    dateafter = args.custom_opts.get('dateafter', None)
    datebefore = args.custom_opts.get('datebefore', None)

    daterange = DateRange(dateafter, datebefore)
    return {
        'daterange': daterange
    }


def _load_pp_sponsorblock(args: TaskArgs) -> dict[str, Any]:
    """Add the `SponsorBlock` postprocessor

    Requires yt-dlp.

    The 'sponsorblock' dict is also used by the 'remove_chapters' and
    'addmetadata' custom_opts.
    """
    sponsorblock: dict[str, Any] = args.custom_opts['sponsorblock']

    mark: list[str] = sponsorblock.get('mark') or []
    remove: list[str] = sponsorblock.get('remove') or []
    api: Optional[str] = sponsorblock.get('api', None)

    # Merge the categories and remove duplicates.
    #
    # The 'SponsorBlock' PP doesn't differentiate between the two lists.
    # Removal is handled in the 'remove_chapters' custom_opt.
    categories = frozenset(mark) | frozenset(remove)

    pp = {
        'key': 'SponsorBlock',
        'categories': categories,
        'when': 'pre_process'
    }
    # Add the API only if given so that yt-dlp can fallback to its
    # default value
    if api is not None:
        pp['api'] = api

    return {
        'postprocessors': (pp,)
    }


def _generate_metadata_actions(
    Actions: Any, parse_metadata: Iterable[ParseMetadataDict],
    replace_in_metadata: Iterable[ReplaceInMetadataDict]
) -> Generator[
    Union[tuple[Any, str, str], tuple[Any, str, str, str]],
    None, None
]:
    """Parse the MetadataParser custom_opts, and yield a list of actions
    to be added to the postprocessor

    `Actions` should be the `MetadataParserPP.Actions` enum, which has
    the members `INTERPRET` and `REPLACE`.

    The postprocessor accepts a mixed list of `INTERPRET` actions
    (generated from the 'parse_metadata' custom_opt) and `REPLACE`
    actions (generated from the 'replace_in_metadata' custom_opt).

    Syntax of `INTERPRET` actions:
        (Actions.INTERPRET, 'FROM', 'TO')

    Syntax of `REPLACE` actions:
        (Actions.REPLACE, 'FIELD', 'REGEX', 'REPLACE')
    """
    for interpreter in parse_metadata:
        yield (Actions.INTERPRET, interpreter['from'], interpreter['to'])

    for replacer in replace_in_metadata:
        for field in replacer['fields']:
            yield (
                Actions.REPLACE, field, replacer['regex'], replacer['replace']
            )


def _load_pp_metadataparser(args: TaskArgs) -> Optional[dict[str, Any]]:
    """Add the `MetadataParser` postprocessor

    The postprocessor requires the `MetadataParserPP.Actions` enum,
    which we have to import from yt-dlp.
    """
    MetadataParserPP = import_object(args.metadata_module, args.metadata_class)
    parse_metadata: Optional[Sequence[ParseMetadataDict]] = (
        args.custom_opts.get('parse_metadata', ())
    )
    replace_in_metadata: Optional[Sequence[ReplaceInMetadataDict]] = (
        args.custom_opts.get('replace_in_metadata', ())
    )

    if parse_metadata is None:
        parse_metadata = ()
    if replace_in_metadata is None:
        replace_in_metadata = ()

    actions = tuple(_generate_metadata_actions(
        MetadataParserPP.Actions, parse_metadata, replace_in_metadata
    ))

    if actions:
        return {
            'postprocessors': ({
                'key': 'MetadataParser',
                'actions': actions,
                'when': 'pre_process'
            },)
        }
    else:
        return None


def _load_pp_metadatafromtitle(args: TaskArgs) -> dict[str, Any]:
    """Add the `MetadataFromTitle` postprocessor"""
    return {
        'postprocessors': ({
            'key': 'MetadataFromTitle',
            'titleformat': args.custom_opts['metafromtitle']
        },)
    }


def _load_pp_ffmpegextractaudio(args: TaskArgs) -> dict[str, Any]:
    """Add the `FFmpegExtractAudio` postprocessor"""
    extractaudio = args.custom_opts['extractaudio']
    loaded_opts: dict[str, Any] = {}

    # Automatically set the format so that it only downloads audio when
    # possible
    keepvideo = args.ytdl_opts.get('keepvideo', False)
    format_ = args.ytdl_opts.get('format', None)
    if not keepvideo and format_ is None:
        loaded_opts['format'] = 'bestaudio/best'

    loaded_opts['postprocessors'] = ({
        'key': 'FFmpegExtractAudio',
        'preferredcodec': extractaudio.get('audioformat', 'best'),
        'preferredquality': str(extractaudio.get('audioquality', '5')),
        'nopostoverwrites': extractaudio.get('nopostoverwrites', False)
    },)

    return loaded_opts


def _load_pp_ffmpegvideoconverter(args: TaskArgs) -> dict[str, Any]:
    """Add the `FFmpegVideoConvertor` postprocessor"""
    recodevideo: str = args.custom_opts['recodevideo']
    return {
        'postprocessors': ({
            'key': 'FFmpegVideoConvertor',
            # Typo is intentional
            'preferedformat': recodevideo
        },)
    }


def _load_pp_ffmpegvideoremuxer(args: TaskArgs) -> Optional[dict[str, Any]]:
    """Add the `FFmpegVideoRemuxer` postprocessor

    Requires yt-dlp.

    This option is ignored if the 'recodevideo' custom_opt is also
    given.
    """
    remuxvideo: str = args.custom_opts['remuxvideo']
    recodevideo: Optional[str] = args.custom_opts.get('recodevideo', None)

    if recodevideo is not None:
        args.logger.warning(
            'Conflicting custom_opts: recodevideo and remuxvideo. '
            'Ignoring remuxvideo.'
        )
        return None

    return {
        'postprocessors': ({
            'key': 'FFmpegVideoRemuxer',
            # Typo is intentional
            'preferedformat': remuxvideo
        },)
    }


def _load_pp_modifychapters(args: TaskArgs) -> Optional[dict[str, Any]]:
    """Add the `ModifyChapters` postprocessor

    Requires yt-dlp.

    The PP is used by the 'remove_chapters' and 'sponsorblock'
    custom_opts.
    """
    force_keyframes: Optional[bool] = None

    remove_chapters: Optional[dict[str, Any]] = (
        args.custom_opts.get('remove_chapters', None)
    )
    if remove_chapters:
        patterns: Optional[list[str]] = remove_chapters.get('patterns', None)
        ranges: Optional[list[list[Union[int, float]]]] = (
            remove_chapters.get('ranges', None)
        )
        force_keyframes = remove_chapters.get('force_keyframes', None)
    else:
        patterns = None
        ranges = None

    sponsorblock: Optional[dict[str, Any]] = (
        args.custom_opts.get('sponsorblock', None)
    )
    if sponsorblock:
        sponsorblock_remove: Optional[list[str]] = (
            sponsorblock.get('remove', None)
        )
        sponsorblock_template: Optional[str] = (
            sponsorblock.get('template', None)
        )
        if force_keyframes is None:
            force_keyframes = sponsorblock.get('force_keyframes', None)
    else:
        sponsorblock_remove = None
        sponsorblock_template = None

    if force_keyframes is None:
        force_keyframes = False

    # Compile all of the regexes
    if patterns:
        regex_patterns: Optional[tuple[re.Pattern[str], ...]] = tuple(
            re.compile(pattern) for pattern in patterns
        )
    else:
        regex_patterns = None

    pp: dict[str, Any] = {
        'key': 'ModifyChapters',
        'force_keyframes': force_keyframes
    }

    # Only return the PP if any args that do something were given.
    #
    # This will be `False` if only the 'sponsorblock' custom_opt was
    # used, and it doesn't have the 'remove' field.
    return_pp = False

    # Add the native remove_chapters args if given
    if regex_patterns:
        pp['remove_chapters_patterns'] = regex_patterns
        return_pp = True
    if ranges:
        pp['remove_ranges'] = ranges
        return_pp = True

    # Add the SponsorBlock args if given
    if sponsorblock_remove:
        pp['remove_sponsor_segments'] = frozenset(sponsorblock_remove)
        return_pp = True
    if sponsorblock_template:
        pp['sponsorblock_chapter_title'] = sponsorblock_template

    if return_pp:
        return {
            'postprocessors': (pp,)
        }
    else:
        return None


def _load_pp_ffmpegmetadata(args: TaskArgs) -> Optional[dict[str, Any]]:
    """Add the `FFmpegMetadata` postprocessor

    This is used by the 'addmetadata', 'addchapters', and
    'sponsorblock' custom_opts.

    The 'add_chapters' and 'add_metadata' kwargs are exclusive to
    yt-dlp, so we only add them if a yt-dlp custom_opt ('addchapters' or
    'sponsorblock') was given.
    When using yt-dlp, they both default to `True` if not given.
    """
    addmetadata: Optional[bool] = args.custom_opts.get('addmetadata', None)
    addchapters: Optional[bool] = args.custom_opts.get('addchapters', None)
    sponsorblock: Optional[dict[str, Any]] = (
        args.custom_opts.get('sponsorblock', None)
    )
    if sponsorblock and 'mark' in sponsorblock:
        sponsorblock_mark: Optional[list[str]] = sponsorblock['mark']
    else:
        sponsorblock_mark = None

    if addchapters is None and not sponsorblock_mark:
        # Don't add the extra kwargs when the yt-dlp custom_opts aren't
        # given in order to maintain backwards-compatibility with
        # youtube-dl
        if addmetadata:
            return {
                'postprocessors': ({
                    'key': 'FFmpegMetadata'
                },)
            }
        else:
            return None
    else:
        # 'addchapters' and/or 'sponsorblock.mark' was given.
        # Requires yt-dlp.
        if addchapters is None:
            addchapters = bool(addmetadata or sponsorblock_mark)
        if addmetadata is None:
            addmetadata = False

        if addmetadata or addchapters:
            return {
                'postprocessors': ({
                    'key': 'FFmpegMetadata',
                    'add_chapters': addchapters,
                    'add_metadata': addmetadata
                },)
            }
        else:
            # Don't add the PP if both kwargs are False, since it won't
            # do anything.
            return None


def _load_pp_ffmpegsubtitlesconverter(args: TaskArgs) -> dict[str, Any]:
    """Add the `FFmpegSubtitlesConvertor` postprocessor"""
    return {
        'postprocessors': ({
            'key': 'FFmpegSubtitlesConvertor',
            'format': args.custom_opts['convertsubtitles']
        },)
    }


def _load_pp_ffmpegthumbnailsconverter(args: TaskArgs) -> dict[str, Any]:
    """Add the `FFmpegThumbnailsConvertor` postprocessor

    Requires yt-dlp.
    """
    return {
        'postprocessors': ({
            'key': 'FFmpegThumbnailsConvertor',
            'format': args.custom_opts['convertthumbnails'],
            'when': 'before_dl'
        },)
    }


def _load_pp_ffmpegembedsubtitle(args: TaskArgs) -> Optional[dict[str, Any]]:
    """Add the `FFmpegEmbedSubtitle` postprocessor"""
    if args.custom_opts['embedsubtitles']:
        return {
            'postprocessors': ({
                'key': 'FFmpegEmbedSubtitle'
            },)
        }
    else:
        return None


def _load_pp_embedthumbnail(args: TaskArgs) -> Optional[dict[str, Any]]:
    """Add the `EmbedThumbnail` postprocessor"""
    if args.custom_opts['embedthumbnail']:
        loaded_opts: dict[str, Any] = {}

        writethumbnail = args.ytdl_opts.get('writethumbnail', False)
        write_all_thumbnails = args.ytdl_opts.get(
            'write_all_thumbnails', False
        )

        # The thumbnail file will be deleted after it's embedded if this
        # is False
        already_have_thumbnail = bool(writethumbnail or write_all_thumbnails)
        if not already_have_thumbnail:
            loaded_opts['writethumbnail'] = True

        loaded_opts['postprocessors'] = ({
            'key': 'EmbedThumbnail',
            'already_have_thumbnail': already_have_thumbnail
        },)

        return loaded_opts
    else:
        return None


def _load_pp_ffmpegsplitchapters(args: TaskArgs) -> dict[str, Any]:
    """Add the `FFmpegSplitChapters` postprocessor"""
    split_chapters: dict[str, Any] = args.custom_opts['split_chapters']
    force_keyframes: Optional[bool] = (
        split_chapters.get('force_keyframes', None)
    )
    if force_keyframes is None:
        force_keyframes = False

    return {
        'postprocessors': ({
            'key': 'FFmpegSplitChapters',
            'force_keyframes': force_keyframes
        },)
    }


def _load_pp_xattrmetadata(args: TaskArgs) -> Optional[dict[str, Any]]:
    """Add the `XAttrMetadata` postprocessor"""
    if args.custom_opts['xattrs']:
        return {
            'postprocessors': ({
                'key': 'XAttrMetadata'
            },)
        }
    else:
        return None


def _load_final_ext(args: TaskArgs) -> Optional[dict[str, str]]:
    """Add the `final_ext` ytdl_opt if needed

    The final_ext ytdl_opt is used by yt-dlp to detect if the file is
    already downloaded. It's needed when a postprocessor changes the
    file extension.

    final_ext will be set to the value of the first existing custom_opt:
        recodevideo, remuxvideo, extractaudio.audioformat

    Based on the yt-dlp source:
        https://github.com/yt-dlp/yt-dlp/blob/df03de2c02192e43e5b51c8708619179a268b4cf/yt_dlp/__init__.py#L587-L591
    """
    # Don't override the existing value when it's manually set
    existing_final_ext: Optional[str] = args.ytdl_opts.get('final_ext', None)
    if existing_final_ext is not None:
        return None

    recodevideo: Optional[str] = args.custom_opts.get('recodevideo', None)
    remuxvideo: Optional[str] = args.custom_opts.get('remuxvideo', None)
    extractaudio: Optional[dict[str, Any]] = (
        args.custom_opts.get('extractaudio', None)
    )
    if extractaudio:
        audioformat: Optional[str] = extractaudio.get('audioformat', None)
    else:
        audioformat = None

    final_ext: Optional[str] = None

    # Only the first option that isn't `None` is checked so that we
    # don't check options that have been overridden.
    # For example, remuxvideo is ignored if recodevideo is set.
    if recodevideo is not None:
        # Only set final_ext if the option only contains alphanumeric
        # characters. This prevents it from being set if the option is
        # set to a value like 'aac>m4a/mov>mp4/mkv'.
        # yt-dlp handles this more accurately by checking if the value
        # is in the set of supported extensions, but we don't have
        # access to that information.
        if recodevideo.isalnum():
            final_ext = recodevideo
    elif remuxvideo is not None:
        if remuxvideo.isalnum():
            final_ext = remuxvideo
    elif audioformat is not None and audioformat != 'best':
        final_ext = audioformat

    if final_ext is not None:
        return {
            'final_ext': final_ext
        }
    else:
        return None


CUSTOM_OPTS: Final = (
    CustomOpt(('datebefore', 'dateafter'), _load_daterange),
    CustomOpt(('sponsorblock',), _load_pp_sponsorblock),
    CustomOpt(
        ('parse_metadata', 'replace_in_metadata'), _load_pp_metadataparser
    ),
    CustomOpt(('metafromtitle',), _load_pp_metadatafromtitle),
    CustomOpt(('convertsubtitles',), _load_pp_ffmpegsubtitlesconverter),
    CustomOpt(('convertthumbnails',), _load_pp_ffmpegthumbnailsconverter),
    CustomOpt(('extractaudio',), _load_pp_ffmpegextractaudio),
    CustomOpt(('remuxvideo',), _load_pp_ffmpegvideoremuxer),
    CustomOpt(('recodevideo',), _load_pp_ffmpegvideoconverter),
    CustomOpt(('embedsubtitles',), _load_pp_ffmpegembedsubtitle),
    CustomOpt(('remove_chapters', 'sponsorblock'), _load_pp_modifychapters),
    CustomOpt(
        ('addmetadata', 'addchapters', 'sponsorblock'), _load_pp_ffmpegmetadata
    ),
    CustomOpt(('embedthumbnail',), _load_pp_embedthumbnail),
    CustomOpt(('split_chapters',), _load_pp_ffmpegsplitchapters),
    CustomOpt(('xattrs',), _load_pp_xattrmetadata),
    CustomOpt(('recodevideo', 'remuxvideo', 'extractaudio'), _load_final_ext),
)
"""List of custom_opts that will be loaded

The order of the postprocessor custom_opts is important.
"""
