"""Version numbers for ytdl-server"""

from __future__ import annotations

__all__ = ('MAIN', 'API', 'SCHEMA')

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Final

MAIN: Final = '1.1.4'
"""Main version number

This tracks all changes made to the program
"""

API: Final = '1.1.0'
"""REST API version

This only changes when there is a change to the REST API
"""

SCHEMA: Final = '1'
"""SQL schema version

This only changes when the schema of the SQL database changes
"""
