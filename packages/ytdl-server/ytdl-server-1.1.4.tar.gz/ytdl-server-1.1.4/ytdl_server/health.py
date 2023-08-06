"""Flask blueprint that contains a heath-check route"""

from __future__ import annotations

__all__ = ('bp', 'health_check')

from typing import TYPE_CHECKING

import flask

if TYPE_CHECKING:
    from typing import Any, Final

bp = flask.Blueprint('health', __name__)

_HEALTHY_RESPONSE: Final = {
    'healthy': True
}


@bp.route('', methods=('GET',))
def health_check() -> tuple[dict[str, Any], int]:
    """Health check

    Always returns `True` when the route is responding.
    """
    return _HEALTHY_RESPONSE, 200
