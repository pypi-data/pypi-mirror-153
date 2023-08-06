"""Flask blueprint for getting metadata about the REST API"""

from __future__ import annotations

__all__ = ('bp', 'get_meta')

from typing import TYPE_CHECKING

import flask

from . import version

if TYPE_CHECKING:
    from typing import Any, Final

bp = flask.Blueprint('meta', __name__)

_META_RESPONSE: Final = {
    'version': version.API
}


@bp.route('', methods=('GET',))
def get_meta() -> tuple[dict[str, Any], int]:
    """Return metadata about the REST API"""
    return _META_RESPONSE, 200
