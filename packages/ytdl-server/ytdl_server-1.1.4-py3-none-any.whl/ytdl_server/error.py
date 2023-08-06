"""Custom ytdl-server exceptions"""

from __future__ import annotations

__all__ = ('YTDLServerError', 'JobNotFoundError', 'http_error')

from typing import TYPE_CHECKING

from . import http_error
from .error_base import YTDLServerError

if TYPE_CHECKING:
    from typing import Optional
    from uuid import UUID


class JobNotFoundError(YTDLServerError):
    """Raised by `db_util.get_job()` and `db_util.get_job_status()`
    when no matching job is found"""

    __slots__ = ('job_id', 'message')

    job_id: UUID
    """Job ID that caused the error"""
    message: str
    """Description of the error"""

    def __init__(self, job_id: UUID, message: Optional[str] = None) -> None:
        self.job_id = job_id
        if message is not None:
            self.message = message
        else:
            self.message = 'Job ID not found within the SQL database'
