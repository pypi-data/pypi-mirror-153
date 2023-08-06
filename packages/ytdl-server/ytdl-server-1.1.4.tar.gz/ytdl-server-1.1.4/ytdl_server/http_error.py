"""HTTP exceptions that are used as Flask error responses

This module is also available within the `error` module. Importing it
from there is preferred, eg:
    from ytdl_server.error import http_error
    print(http_error.DataBadType)
"""

from __future__ import annotations

__all__ = (
    'CustomOptionBadValue', 'DataBadType', 'DataMissingKey',
    'ForbiddenCustomOption', 'ForbiddenYTDLOption', 'JobAlreadyCompleted',
    'JobNotFound', 'JobNotRunning', 'KeyBadType', 'KeyBadValue',
    'UnspecifiedError', 'YTDLOptionBadValue', 'YTDLUserOptionsNotAllowed',
    'TYPE_NAMES', 'INDEFINITE_TYPE_NAMES'
)

from typing import TYPE_CHECKING
from uuid import UUID

from .error_base import YTDLServerError

if TYPE_CHECKING:
    from collections.abc import Generator
    from typing import Any, Final, Optional, Union

    from .type import JSONableTypes

TYPE_NAMES: Final = {
    dict: 'object',
    list: 'array',
    tuple: 'array',
    str: 'string',
    int: 'integer',
    float: 'float',
    bool: 'boolean',
    type(None): 'null'
}
"""Mapping of Python types to their corresponding names in JSON

Note that this makes a distinction between `int` and `float` even though
JSON technically only has a single 'number' type.
"""

INDEFINITE_TYPE_NAMES: Final = {
    dict: 'an object',
    list: 'an array',
    tuple: 'an array',
    str: 'a string',
    int: 'an integer',
    float: 'a float',
    bool: 'a boolean',
    type(None): 'null'
}
"""Same as `TYPE_NAMES`, but with 'a' or 'an' prepended to the name"""


# TODO: Add tests for these
class HTTPError(YTDLServerError):
    """Base class for errors raised by the Flask REST API

    These errors are returned to the user.

    NOTE: This class must not be raised directly; use a subclass
    instead.
    """

    __slots__ = ('code', 'description')

    code: int
    """HTTP status code"""
    description: str
    """Human-readable error message"""

    def __init__(self, code: int, description: str) -> None:
        self.code = code
        self.description = description

    def to_dict(self) -> dict[str, Any]:
        """Create a dict that can be used as the JSON response data

        All attributes defined in `__slots__` that do not start with an
        underscore will be added to the dict. This includes the slots of
        parent classes.

        Additionally, the name of the class will be added as the `error`
        key.
        """
        response_data = {}

        for attr in self._get_all_slots():
            # Skip private members
            if not attr.startswith('_'):
                value = getattr(self, attr)
                response_data[attr] = value

        error_name = type(self).__name__
        response_data['error'] = error_name

        return response_data

    @classmethod
    def _get_all_slots(cls) -> Generator[str, None, None]:
        """Recursively return all __slots__ of the class

        The class and all parent classes are checked in
        method-resolution order.

        Slots are only returned if the class the slot belongs to is a
        subclass of HTTPError.
        """
        for base_cls in cls.mro():
            if not issubclass(base_cls, HTTPError):
                continue

            if hasattr(base_cls, '__slots__'):
                for slot in base_cls.__slots__:
                    yield slot


class UnspecifiedError(HTTPError):
    """Generic fallback error used by Flask"""

    __slots__ = ('name',)

    name: str
    """Short name describing the error"""

    def __init__(
        self, name: str, code: Optional[int], description: Optional[str]
    ) -> None:
        """`code` and `description` are optional because Flask's
        `HTTPException` has them set as optional
        """
        if code is None:
            # Not sure why this is optional, so let's just raise 500
            code = 500
        if description is None:
            description = name
        super().__init__(code, description)
        self.name = name


class DataBadType(HTTPError):
    """The request data is missing or is the wrong type"""

    __slots__ = ('type',)

    type: str
    """Expected JSON type, eg 'object', 'array'"""

    def __init__(
        self, type_: JSONableTypes, *, description: Optional[str] = None
    ) -> None:
        """
        type_: Expected Python type, eg `dict`, `str`, `type(None)`
        """
        if description is None:
            type_name = INDEFINITE_TYPE_NAMES[type_]
            description = f'Request data must be {type_name}'

        super().__init__(400, description)
        self.type = TYPE_NAMES[type_]


class DataMissingKey(HTTPError):
    """The request data is missing a required top-level key"""

    __slots__ = ('key',)

    key: str
    """Name of the missing key"""

    def __init__(
        self, key: str, *, description: Optional[str] = None
    ) -> None:
        if description is None:
            description = f'Missing key in request data: {key}'
        super().__init__(400, description)
        self.key = key


class KeyBadType(HTTPError):
    """A key within the request data object has the wrong type"""

    __slots__ = ('key', 'type')

    key: str
    """Name of the key"""
    type: str
    """Expected JSON type, eg 'object', 'array'"""

    def __init__(
        self, key: str, type_: JSONableTypes, *,
        description: Optional[str] = None
    ) -> None:
        """
        type_: Expected Python type, eg `dict`, `str`, `type(None)`
        """
        if description is None:
            type_name = INDEFINITE_TYPE_NAMES[type_]
            description = f'The key {key!r} must be {type_name}'
        super().__init__(400, description)
        self.key = key
        self.type = TYPE_NAMES[type_]


class KeyBadValue(HTTPError):
    """A key within the request data object has an invalid value"""

    __slots__ = ('key',)

    key: str
    """Name of the key"""

    def __init__(
        self, key: str, *, description: Optional[str] = None
    ) -> None:
        if description is None:
            description = f'The key {key!r} has an invalid value'
        super().__init__(400, description)
        self.key = key


class YTDLUserOptionsNotAllowed(HTTPError):
    """The user tried to provide their own ytdl_opts or custom_opts
    when it's forbidden by the server config"""

    __slots__ = ('key',)

    key: str
    """Name of the key"""

    def __init__(
        self, key: str, *, description: Optional[str] = None
    ) -> None:
        if description is None:
            description = 'The server does not allow custom youtube-dl options'
        super().__init__(403, description)
        self.key = key


class ForbiddenYTDLOption(HTTPError):
    """The user provided a ytdl_opt that isn’t whitelisted"""

    __slots__ = ('option',)

    option: str
    """Name of the ytdl_opt"""

    def __init__(
        self, option: str, *, description: Optional[str] = None
    ) -> None:
        if description is None:
            description = f'Forbidden ytdl_opt: {option}'
        super().__init__(403, description)
        self.option = option


class YTDLOptionBadValue(HTTPError):
    """The user provided a ytdl_opt with an invalid value"""

    __slots__ = ('option',)

    option: str
    """Name of the ytdl_opt"""

    def __init__(
        self, option: str, code: int, *, description: Optional[str] = None
    ) -> None:
        if description is None:
            description = f'The ytdl_opt {option!r} has an invalid value'
        super().__init__(code, description)
        self.option = option


class ForbiddenCustomOption(HTTPError):
    """The user provided a custom_opt that isn’t whitelisted"""

    __slots__ = ('option',)

    option: str
    """Name of the custom_opt"""

    def __init__(
        self, option: str, *, description: Optional[str] = None
    ) -> None:
        if description is None:
            description = f'Forbidden custom_opt: {option}'
        super().__init__(403, description)
        self.option = option


class CustomOptionBadValue(HTTPError):
    """The user provided a custom_opt with an invalid value"""

    __slots__ = ('option',)

    option: str
    """Name of the custom_opt"""

    def __init__(
        self, option: str, code: int, *, description: Optional[str] = None
    ) -> None:
        if description is None:
            description = f'The custom_opt {option!r} has an invalid value'
        super().__init__(code, description)
        self.option = option


class JobNotFound(HTTPError):
    """No job exists that matches the given job ID"""

    __slots__ = ('id',)

    id: str
    """Job ID"""

    def __init__(
        self, id_: Union[str, UUID], *, description: Optional[str] = None
    ) -> None:
        if description is None:
            description = 'Job ID not found'
        super().__init__(404, description)

        # Convert the UUID to a str if needed so that it's JSONable
        if isinstance(id_, UUID):
            id_ = str(id_)
        self.id = id_


class JobAlreadyCompleted(HTTPError):
    """The user tried to cancel a job that has already completed"""

    __slots__ = ('id', 'status_url')

    id: str
    """Job ID"""
    status_url: str
    """URL to get the status of the job"""

    def __init__(
        self, id_: Union[str, UUID], status_url: str, *,
        description: Optional[str] = None
    ) -> None:
        if description is None:
            description = (
                'Unable to cancel the job because it already completed'
            )
        super().__init__(400, description)

        # Convert the UUID to a str if needed so that it's JSONable
        if isinstance(id_, UUID):
            id_ = str(id_)
        self.id = id_
        self.status_url = status_url


class JobNotRunning(HTTPError):
    """The user tried to cancel a running job, but the Celery task
    isn’t running"""

    __slots__ = ('id', 'status_url')

    id: str
    """Job ID"""
    status_url: str
    """URL to get the status of the job"""

    def __init__(
        self, id_: Union[str, UUID], status_url: str, *,
        description: Optional[str] = None
    ) -> None:
        if description is None:
            description = (
                'Unable to cancel the job because it doesn\'t appear to be '
                'running'
            )
        super().__init__(500, description)

        # Convert the UUID to a str if needed so that it's JSONable
        if isinstance(id_, UUID):
            id_ = str(id_)
        self.id = id_
        self.status_url = status_url
