"""Celery app and utilities"""

from __future__ import annotations

__all__ = ('app', 'init_celery')

from typing import TYPE_CHECKING

from celery import Celery
from celery.contrib.abortable import AbortableTask
from celery.signals import after_setup_task_logger, worker_process_init

from .database import db
from .util import get_env_log_level

if TYPE_CHECKING:
    from collections.abc import Mapping
    from logging import Logger
    from typing import Any, Optional

    from flask import Flask

app = Celery(__name__)
app.conf.update({
    'imports': ('ytdl_server.task',)
})


# Ignore typing error about the decorator being untyped
@after_setup_task_logger.connect  # type: ignore[misc]
def set_up_logger(logger: Logger, *args: Any, **kwargs: Any) -> None:
    """Set the log level for Celery tasks

    The log level is set via the `$YTDL_LOG_LEVEL` env-var. If the var
    isn't set, the Celery logger won't be changed.
    """
    log_level = get_env_log_level()
    if log_level is not None:
        logger.setLevel(log_level)


def init_celery(
    flask_app: Flask, celery_config: Optional[Mapping[str, Any]] = None
) -> Celery:
    # Ignore typing error about `AbortableTask` not being subclassable
    # because it's `Any`
    class AbortableFlaskTask(AbortableTask):  # type: ignore[misc]
        """Abortable task with Flask context"""

        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    # Ignore typing error about the decorator being untyped
    @worker_process_init.connect  # type: ignore[misc]
    def reset_engine(**kwargs: Any) -> None:
        """Prevent SQLAlchemy from breaking when running multiple tasks
        at once

        https://stackoverflow.com/a/54751019
        """
        with flask_app.app_context():
            db.engine.dispose()

    if celery_config is not None:
        app.conf.update(celery_config)

    # Set the default base task to AbortableDatabaseTask
    app.Task = AbortableFlaskTask
    # Prevent `reset_engine` from being garbage-collected when this
    # function exits
    app._reset_engine_sig = reset_engine
