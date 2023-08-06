"""Miscellaneous utility functions and classes"""

from __future__ import annotations

__all__ = (
    'StatusEnum', 'LogEnum', 'Log', 'Job', 'has_path_seps', 'import_object',
    'terminate', 'get_env_log_level'
)

import importlib
import os
import signal
import time
from dataclasses import dataclass, field
from enum import auto, Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence
    from datetime import datetime
    from typing import Any, Optional
    from uuid import UUID

    from .type import Terminatable


class StatusEnum(Enum):
    """Job statuses"""
    queued = auto()
    """Job was created, but hasn't been started by a worker yet"""
    downloading = auto()
    """Job is currently running"""
    finished = auto()
    """Job completed successfully"""
    error = auto()
    """Job failed"""
    cancelled = auto()
    """Job was cancelled by the user"""
    timeout = auto()
    """Celery task running the job timed out"""


class LogEnum(Enum):
    """YoutubeDL log levels"""
    debug = auto()
    warning = auto()
    error = auto()


@dataclass
class Log:
    level: LogEnum
    message: str
    timestamp: datetime

    def get_json(self) -> dict[str, Any]:
        return {
            'level': self.level.name,
            'message': self.message,
            'timestamp': self.timestamp.isoformat()
        }


@dataclass
class Progress:
    progress: dict[str, Any]
    timestamp: datetime
    filename: str = field(init=False)

    def __post_init__(self) -> None:
        self.filename = self.progress['filename']

    def get_json(self) -> dict[str, Any]:
        return self.progress


@dataclass
class Job:
    id: UUID
    status: StatusEnum
    urls: Sequence[str]
    ytdl_opts: Optional[Mapping[str, Any]] = None
    started: Optional[datetime] = None
    finished: Optional[datetime] = None
    logs: Sequence[Log] = tuple()
    error: Optional[str] = None
    progress: Sequence[Progress] = tuple()

    @staticmethod
    def _iso_or_none(datetime_: Optional[datetime]) -> Optional[str]:
        """Returns an ISO timestamp or None"""
        if datetime_ is not None:
            return datetime_.isoformat()
        else:
            return None

    def get_json(self) -> dict[str, Any]:
        return {
            'id': str(self.id),
            'status': self.status.name,
            'urls': tuple(self.urls),
            'ytdl_opts': self.ytdl_opts,
            'started': self._iso_or_none(self.started),
            'finished': self._iso_or_none(self.finished),
            'logs': tuple(
                log.get_json() for log in self.logs
            ),
            'error': self.error,
            'progress': tuple(
                progress.get_json() for progress in self.progress
            )
        }


def _kill(pid: int) -> None:
    """Manually kill the given PID by sending SIGKILL

    Raises `NotImplementedError` on Windows because it doesn't have
    SIGKILL
    """
    if hasattr(signal, 'SIGKILL'):
        os.kill(pid, signal.SIGKILL)
    else:
        raise NotImplementedError("SIGKILL isn't supported on Windows")


def _join(process: Terminatable, timeout: int) -> None:
    """Manual re-implementation of `Process.join()`

    This is used because `join()` randomly raises an exception when
    using `billiard.Process`
    (https://github.com/celery/billiard/issues/270)
    """
    for _ in range(timeout):
        time.sleep(1)
        if not process.is_alive():
            return


def terminate(process: Terminatable, timeout: int = 10) -> bool:
    """Terminate the given process

    First, SIGTERM is sent to the process. If the process doesn't exit
    within `timeout` seconds, SIGKILL is sent.

    If SIGKILL is unable to kill the process within 5 seconds,
    `ChildProcessError` is raised

    Returns `True` if SIGTERM successfully terminated the process, or
    `False` if SIGKILL was needed

    Since the function waits on both SIGTERM and SIGKILL, the maximum
    amount of time that the function can wait is `timeout` + 5 seconds
    """
    if not process.is_alive():
        return True

    process.terminate()
    _join(process, timeout)

    if process.is_alive():
        skip_wait = False

        # Unlike `multiprocessing.Process`, `billiard.Process` doesn't
        # have a `kill()` method, so we have to send SIGKILL manually
        if hasattr(process, 'kill'):
            # Ignore typing error about `kill()` not being defined
            # because we just checked it
            # (https://github.com/python/mypy/issues/1424)
            process.kill()  # type: ignore[attr-defined]
        else:
            try:
                # Ignore typing error about `process.pid` being the
                # wrong type. `process.pid` always returns an int after
                # the process is started
                _kill(process.pid)  # type: ignore[arg-type]
            except NotImplementedError:
                skip_wait = True

        if not skip_wait:
            _join(process, 5)

        if process.is_alive():
            raise ChildProcessError(
                'Timed out while waiting for the process to die'
            )
        else:
            return False
    else:
        return True


def import_object(module: str, attr: str) -> Any:
    """Import the given module, and return the given attribute from it"""
    module_imported = importlib.import_module(module)
    attr_value = getattr(module_imported, attr)
    return attr_value


def has_path_seps(str_: str) -> bool:
    """Returns `True` if the string contains path separators"""
    has_sep = os.sep in str_
    has_altsep = os.altsep is not None and os.altsep in str_
    return has_sep or has_altsep


def get_env_log_level() -> Optional[str]:
    """Get the log level from the env-var `$YTDL_LOG_LEVEL`

    This allows configuring the log level for both Flask and Celery with
    a single env-var.

    Returns `None` if the env-var isn't set. In this case, the logging
    shouldn't be configured.
    """
    log_level = os.environ.get('YTDL_LOG_LEVEL', None)
    if log_level:
        return log_level.upper()
    else:
        return None
