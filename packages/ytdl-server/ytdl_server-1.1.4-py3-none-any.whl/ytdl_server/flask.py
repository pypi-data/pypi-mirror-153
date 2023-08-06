"""Module for creating the Flask app"""

from __future__ import annotations

__all__ = ('create_app', 'with_logging')

from typing import TYPE_CHECKING
import logging

from flask import Flask

from . import celery, flask_config, health, job, json, meta
from .config import Config
from .database import db
from .util import get_env_log_level

if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Any, Optional


def _init_db(app: Flask) -> None:
    """Initialize the SQLAlchemy database for the given Flask app

    Raises `RuntimeError` if the database dialect isn't PostgreSQL.
    """
    # Disable deprecation warning about this option
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        dialect = db.session.bind.dialect.name
    if dialect != 'postgresql':
        raise RuntimeError(
            f'SQL database dialect must be PostgreSQL, not {dialect}'
        )

    # Create the tables if they don't exist
    db.create_all(app=app)


def create_app(test_config: Optional[Mapping[str, Any]] = None) -> Flask:
    """Create and return the Flask app

    `test_config` is an optional dict that will be used to load the
    `config.Config` class. Intended for testing.
    """
    app = Flask(__name__)

    if test_config is None:
        config = Config(logger=app.logger)
    else:
        app.config['TESTING'] = True
        config = Config(
            logger=app.logger, config_dict=test_config, load_env_vars=False
        )

    app.config['YTDL_CONFIG'] = config
    app.config.from_mapping(config.flask_config)

    app.json_encoder = json.JSONEncoderWithWarning
    app.register_blueprint(json.bp)
    app.register_blueprint(job.bp, url_prefix='/jobs')
    app.register_blueprint(flask_config.bp, url_prefix='/config')
    app.register_blueprint(meta.bp, url_prefix='/meta')
    app.register_blueprint(health.bp, url_prefix='/health')

    app.logger.debug(
        'Initializing database: %s', config.database_uri
    )
    _init_db(app)

    app.logger.debug('Loading Celery config: %s', config.celery_config)
    celery.init_celery(app, config.celery_config)

    return app


def with_logging() -> Flask:
    """Set up logging, and create the Flask app

    The log level is set via the `$YTDL_LOG_LEVEL` env-var. If the var
    isn't set, logging won't be set up, which means that the level will
    default to 'WARNING'.

    This can be used as the entrypoint when running ytdl-server through
    a WSGI server (such as Gunicorn).
    """
    log_level = get_env_log_level()
    if log_level is not None:
        log_level = log_level.upper()
        logging.basicConfig(level=log_level)

    return create_app()
