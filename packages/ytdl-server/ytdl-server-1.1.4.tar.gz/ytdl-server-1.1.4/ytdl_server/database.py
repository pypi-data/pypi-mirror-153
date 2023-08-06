"""SQLAlchemy database and models"""

from __future__ import annotations

__all__ = ('db', 'Job', 'Log', 'Progress')

from typing import TYPE_CHECKING

import sqlalchemy as sql
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB, UUID

from . import json
from .util import LogEnum, StatusEnum

if TYPE_CHECKING:
    from flask_sqlalchemy.model import DefaultMeta

# Allow using `db` as a parent class.
# https://github.com/dropbox/sqlalchemy-stubs/issues/76#issuecomment-595839159
db: DefaultMeta = SQLAlchemy(
    engine_options={
        # When inserting data into JSONB columns, quietly convert
        # unserializable objects to strings instead of raising an
        # exception.
        # This prevents Job.ytdl_opts from breaking when using some
        # custom_opts
        'json_serializer': json.dumps_quiet
    }
)


# Ignore typing error about `db.Model` not being subclassable because
# it's `Any`
class Job(db.Model):  # type: ignore[misc]
    __tablename__ = 'ytdl_server_jobs'

    id = sql.Column(
        UUID(as_uuid=True), primary_key=True,
        server_default=sql.text('gen_random_uuid()'), comment='Job ID'
    )

    status = sql.Column(
        sql.Enum(StatusEnum), nullable=False, comment='Job status'
    )
    error = sql.Column(sql.UnicodeText, nullable=True, comment='Error message')

    urls = sql.Column(
        sql.ARRAY(sql.UnicodeText, dimensions=1, as_tuple=True),
        nullable=False, comment='Video URLs to download'
    )
    ytdl_opts = sql.Column(JSONB, nullable=True, comment='youtube-dl options')

    started = sql.Column(
        sql.TIMESTAMP(timezone=True), nullable=True, comment='Time job started'
    )
    finished = sql.Column(
        sql.TIMESTAMP(timezone=True), nullable=True,
        comment='Time job finished'
    )


class Log(db.Model):  # type: ignore[misc]
    __tablename__ = 'ytdl_server_logs'
    __table_args__ = (
        sql.Index(
            'ytdl_server_logs_job_id_timestamp_idx', 'job_id', 'timestamp'
        ),
    )

    id = sql.Column(
        UUID(as_uuid=True), primary_key=True,
        server_default=sql.text('gen_random_uuid()'), comment='Primary key'
    )
    job_id = sql.Column(
        UUID(as_uuid=True), sql.ForeignKey(
            Job.id, ondelete='CASCADE', onupdate='CASCADE'
        ), nullable=False, comment='Job ID'
    )
    level = sql.Column(sql.Enum(LogEnum), nullable=False, comment='Log level')
    message = sql.Column(
        sql.UnicodeText, nullable=False, comment='Log message'
    )
    timestamp = sql.Column(
        sql.TIMESTAMP(timezone=True), nullable=False,
        server_default=sql.text('CURRENT_TIMESTAMP'),
        comment='Time the message was logged'
    )


class Progress(db.Model):  # type: ignore[misc]
    __tablename__ = 'ytdl_server_progress'
    __table_args__ = (
        # Ensure that only one row exists for each file that's
        # downloaded instead of creating a new row for every progress
        # update
        sql.UniqueConstraint('job_id', 'filename'),
        sql.Index(
            'ytdl_server_progress_job_id_timestamp_idx', 'job_id', 'timestamp'
        )
    )

    id = sql.Column(
        UUID(as_uuid=True), primary_key=True,
        server_default=sql.text('gen_random_uuid()'), comment='Primary key'
    )
    job_id = sql.Column(
        UUID(as_uuid=True), sql.ForeignKey(
            Job.id, ondelete='CASCADE', onupdate='CASCADE'
        ), nullable=False, comment='Job ID'
    )
    filename = sql.Column(
        sql.UnicodeText, nullable=False,
        comment='Filename of the downloaded file'
    )
    progress = sql.Column(
        JSONB, nullable=False,
        comment='Object containing the download progress info'
    )
    timestamp = sql.Column(
        sql.TIMESTAMP(timezone=True), nullable=False,
        server_default=sql.text('CURRENT_TIMESTAMP'),
        comment='Time the progress info was last updated'
    )
