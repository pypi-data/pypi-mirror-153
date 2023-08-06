"""Flask blueprint for getting the ytdl-server configuration"""

from __future__ import annotations

__all__ = ('bp', 'get_config')

from typing import TYPE_CHECKING

import flask

from .ytdl import censor_opts

if TYPE_CHECKING:
    from typing import Any, Final

    from .config import Config

bp = flask.Blueprint('config', __name__)

_WHITELISTED_OPTS: Final = frozenset((
    'download_dir', 'force_download_dir', 'allow_user_opts',
    'ytdl_enable_whitelist', 'ytdl_sensitive_opts', 'custom_default_opts',
    'custom_enable_whitelist'
))


def _create_config_dict(config: Config) -> dict[str, Any]:
    config_dict = {}
    for opt, value in config.items():
        if opt in _WHITELISTED_OPTS:
            config_dict[opt] = value

    # Censor 'ytdl_default_opts' so that it doesn't contain passwords
    config_dict['ytdl_default_opts'] = censor_opts(
        config.ytdl_default_opts, sensitive_opts=config.ytdl_sensitive_opts
    )

    if config.allow_user_opts and config.ytdl_enable_whitelist:
        # Merge 'ytdl_whitelist' with 'ytdl_whitelist_add' and
        # 'ytdl_whitelist_remove' so that the user only sees the final
        # whitelist
        merged_whitelist = set(config.ytdl_whitelist)
        merged_whitelist |= config.ytdl_whitelist_add
        merged_whitelist -= config.ytdl_whitelist_remove
        config_dict['ytdl_whitelist'] = tuple(sorted(merged_whitelist))
    else:
        # Set 'ytdl_whitelist' to 'None' if it's not being used
        config_dict['ytdl_whitelist'] = None

    if config.allow_user_opts and config.custom_enable_whitelist:
        config_dict['custom_whitelist'] = tuple(
            sorted(config.custom_whitelist)
        )
    else:
        # Set 'custom_whitelist' to 'None' if it's not being used
        config_dict['custom_whitelist'] = None

    return config_dict


@bp.route('', methods=('GET',))
def get_config() -> tuple[dict[str, Any], int]:
    """Return the server ytdl configuration"""
    config = flask.current_app.config['YTDL_CONFIG']

    config_dict = _create_config_dict(config)
    return config_dict, 200
