"""Entrypoint for the Celery worker

Usage: celery -A ytdl_server.run_celery worker
"""

__all__ = ('app',)

from . import flask
from .celery import app

flask_app = flask.with_logging()
