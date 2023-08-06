"""Shared base exception used by the `error` and `http_error` modules"""

__all__ = ('YTDLServerError',)


class YTDLServerError(Exception):
    """Base exception for all other exceptions in the `error` module

    This should be imported from the `error` module, eg:
        from ytdl_server.error import YTDLServerError
    """

    __slots__ = ()
