"""Class and helper functions for running youtube-dl"""

from __future__ import annotations

__all__ = ('Downloader', 'censor_opts')

from collections.abc import Sequence
from datetime import datetime, timezone
from typing import TYPE_CHECKING
import threading

from . import db_util
from .database import db
from .util import Log, LogEnum, Progress, StatusEnum

if TYPE_CHECKING:
    from collections.abc import Collection, Iterable, Mapping
    from logging import Logger
    from typing import Any, Optional
    from uuid import UUID


class Downloader:
    """Class used by `task` to run YoutubeDL

    The class works by running YoutubeDL in a separate thread while
    handling all database transactions in the main thread. This prevents
    the download from slowing down due to slow database IO.

    `db_util.insert_job()` must be called before initializing this class
    so that the job exists in the database
    """

    __slots__ = (
        'job_id', 'urls', 'ytdl_opts', 'ytdl_class', 'logger', '_ytdl_logger',
        '_download_started', '_download_thread', '_progress_lock', '_log_lock',
        '_progress_queue', '_log_queue', '_download_exception'
    )

    job_id: UUID
    """ID of the job that's being downloaded"""
    urls: tuple[str, ...]
    """List of URLs to download"""
    ytdl_opts: dict[str, Any]
    """Dict of kwargs that will be passed to `ytdl_class`"""
    ytdl_class: type
    """YoutubeDL class to use

    Normally, this should be `youtube_dl.YoutubeDL` unless you're using
    a fork with a different module name
    """
    logger: Logger
    """Logger object to log to"""

    _ytdl_logger: YTDLLogger
    """YTDLLogger instance that's used for the job"""
    _download_started: bool
    """Whether or not `download()` has been called already"""
    _download_thread: threading.Thread
    """Thread that's used to run YoutubeDL"""
    _progress_lock: threading.Lock
    """Lock used to access `_progress_queue`"""
    _log_lock: threading.Lock
    """Lock used to access `_log_queue`"""
    _progress_queue: list[Progress]
    """List of progress entries that need to be written to the database"""
    _log_queue: list[Log]
    """List of logs that need to be written to the database"""
    _download_exception: Optional[Exception]
    """If the download thread fails, this will be set to the exception
    that was raised

    Otherwise, this will be set to `None` once the download thread exits
    normally.
    """

    def __init__(
        self, job_id: UUID, urls: Iterable[str], ytdl_opts: Mapping[str, Any],
        ytdl_class: type, logger: Logger
    ) -> None:
        self.job_id = job_id
        self.urls = tuple(urls)
        self.ytdl_opts = dict(ytdl_opts)
        self.ytdl_class = ytdl_class
        self.logger = logger

        self._download_started = False
        self._progress_lock = threading.Lock()
        self._log_lock = threading.Lock()
        self._progress_queue = []
        self._log_queue = []

        if 'progress_hooks' not in self.ytdl_opts:
            self.ytdl_opts['progress_hooks'] = (self.progress_hook,)
        else:
            self.ytdl_opts['progress_hooks'] = (
                tuple(ytdl_opts['progress_hooks']) + (self.progress_hook,)
            )

        # Prevent ytdl from injecting ANSI escape codes into the logs
        self.ytdl_opts['no_color'] = True
        # Prevent progress from being printed to the debug log (the
        # progress hook is used instead)
        self.ytdl_opts['noprogress'] = True
        # Disable youtube-dl version check
        # This is disabled by default. Set it explicitly so it can't be
        # enabled
        self.ytdl_opts['call_home'] = False

        self._ytdl_logger = self.YTDLLogger(self)
        self.ytdl_opts['logger'] = self._ytdl_logger

    def progress_hook(self, progress_map: dict[str, Any]) -> None:
        progress = Progress(progress_map, datetime.now(tz=timezone.utc))
        with self._progress_lock:
            self._progress_queue.append(progress)

    class YTDLLogger:
        __slots__ = ('_downloader',)

        _downloader: Downloader

        def __init__(self, downloader: Downloader) -> None:
            self._downloader = downloader

        def _insert(self, level: LogEnum, msg: str) -> None:
            log = Log(level, msg, datetime.now(tz=timezone.utc))
            with self._downloader._log_lock:
                self._downloader._log_queue.append(log)

        def debug(self, msg: str) -> None:
            self._insert(LogEnum.debug, msg)

        def warning(self, msg: str) -> None:
            self._insert(LogEnum.warning, msg)

        def error(self, msg: str) -> None:
            self._insert(LogEnum.error, msg)

    def _download(self) -> None:
        """Run youtube-dl

        This should be run in its own daemon thread
        """
        try:
            with self.ytdl_class(self.ytdl_opts) as ytdl:
                ytdl.download(self.urls)
        except Exception as e:
            self._download_exception = e
        else:
            self._download_exception = None

    def _set_final_status(self) -> None:
        """Set the status of the job after the download is complete"""
        if self._download_exception is None:
            self.logger.info('Job finished: %s', self.job_id)
            db_util.update_job(
                self.job_id,
                status=StatusEnum.finished, finished=db_util.CURRENT_TIMESTAMP
            )
        else:
            self.logger.error(
                'Job failed: %s', self.job_id,
                exc_info=self._download_exception
            )
            error_msg = (
                f'{type(self._download_exception).__name__}: '
                f'{self._download_exception}'
            )
            db_util.update_job(
                self.job_id,
                status=StatusEnum.error, finished=db_util.CURRENT_TIMESTAMP,
                # The error message is only logged from within `ytdl`
                # so that the user is only shown it when the error is
                # from youtube-dl
                error=error_msg
            )

    def _manage(self) -> None:
        """Manage the download from the main thread

        Performs the following tasks:
          - Every second, insert any logs and download progress that are
            generated by the download thread into the database.
          - Write the final job status to the database once the download
            thread completes.
        """
        download_is_running = True
        while download_is_running:
            self._download_thread.join(1)
            if not self._download_thread.is_alive():
                self.logger.debug('Download thread exited')
                download_is_running = False

            self._insert_logs_and_progress()

        self._set_final_status()

    def _insert_logs_and_progress(self) -> None:
        """Pop all logs and progress-entries from the queues, and insert
        them into the database

        The logs and progress-entries are inserted in a single
        transaction.
        """
        logs = self._pop_logs()
        progress = self._pop_progress()
        if not logs and not progress:
            return

        with db.session.begin():
            self._insert_logs(logs)
            self._insert_progress(progress)

    def _pop_logs(self) -> list[Log]:
        """Pop and return all logs from the queue"""
        with self._log_lock:
            logs = self._log_queue
            self._log_queue = []
        return logs

    def _pop_progress(self) -> list[Progress]:
        """Pop and return all progress-entries from the queue"""
        with self._progress_lock:
            progress = self._progress_queue
            self._progress_queue = []
        return progress

    def _insert_logs(self, popped_logs: Collection[Log]) -> None:
        """Insert the given logs into the database

        Does nothing if the collection is empty.

        This does not commit the SQL statement. Running it within a
        transaction is recommended.
        """
        if not popped_logs:
            return

        self.logger.debug('Inserting %d logs into DB', len(popped_logs))
        db_util.insert_logs(self.job_id, popped_logs, commit=False)

    def _insert_progress(self, popped_progress: Sequence[Progress]) -> None:
        """Insert the given progress entries into the database

        Does nothing if the sequence is empty.

        This does not commit the SQL statement. Running it within a
        transaction is recommended.
        """
        if not popped_progress:
            return

        self.logger.debug(
            'Inserting %d progress entries into DB', len(popped_progress)
        )
        db_util.upsert_progress(self.job_id, popped_progress, commit=False)

    def download(self) -> None:
        """Start the download

        This function can only be run once per instance. Attempting to
        run it again will raise `RuntimeError`
        """
        if self._download_started:
            raise RuntimeError('downloader can only be run once')
        self._download_started = True

        self.logger.info('Starting downloader for job %s', self.job_id)
        db_util.update_job(
            self.job_id,
            status=StatusEnum.downloading, started=db_util.CURRENT_TIMESTAMP
        )

        self._download_thread = threading.Thread(
            # Run as a daemon so that youtube-dl doesn't keep running
            # silently if the main thread crashes
            target=self._download, daemon=True
        )
        self._download_thread.start()

        self._manage()


def censor_opts(
    ytdl_opts: Mapping[str, Any], sensitive_opts: Iterable[str]
) -> dict[str, Any]:
    """Return a censored version of the given youtube-dl option dict
    that's safe to show to the user

    Sensitive options such as passwords are set to `None`

    ytdl_opts: Uncensored youtube-dl options
    sensitive_opts: List of keys that should be censored. If any of
        these options are in ytdl_opts, the value will be set to None
    """
    opts = dict(ytdl_opts)

    for opt in sensitive_opts:
        if opt in opts:
            opts[opt] = None

    return opts
