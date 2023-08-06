"""Custom types for type-checking"""

from __future__ import annotations

__all__ = (
    'JSONableTypes', 'Terminatable', 'ParseMetadataDict',
    'ReplaceInMetadataDict'
)

from typing import Protocol, TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import Any, Optional, Union

    JSONableTypes = Union[
        type[dict], type[list], type[tuple[Any, ...]],
        type[str], type[int], type[float], type[bool], type[None]
    ]
    """Types that can be serialized to JSON

    Used by some subclasses of `error.http_error.HTTPError`
    """


class Terminatable(Protocol):
    """Protocol that represents a process that can be terminated

    Objects that match this protocol can be used as an argument with
    `util.terminate()`

    Example: `multiprocessing.Process`

    A protocol is used so that it will also accept alternative
    process objects such as `billiard.Process`
    """
    @property
    def pid(self) -> Optional[int]:
        ...

    def is_alive(self) -> bool:
        ...

    def join(self, timeout: Optional[int] = None) -> Any:
        ...

    def terminate(self) -> Any:
        ...


# This uses the old syntax because 'from' isn't a valid name for a class
# var
ParseMetadataDict = TypedDict(
    'ParseMetadataDict', {
        'from': str,
        'to': str
    }
)
"""Type that represents a single value of the parse_metadata custom_opt

Used by `custom_opt._generate_metadata_actions()`
"""


class ReplaceInMetadataDict(TypedDict):
    """Type that represents a single value of the replace_in_metadata
    custom_opt

    Used by `custom_opt._generate_metadata_actions()`
    """
    fields: Iterable[str]
    regex: str
    replace: str
