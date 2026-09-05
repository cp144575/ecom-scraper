"""HTTP request value object."""

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class Request:
    """A crawlable URL with optional headers and metadata."""

    url: str
    method: str = "GET"
    headers: dict[str, str] = field(default_factory=dict)
    meta: dict[str, object] = field(default_factory=dict)
    request_id: str = field(default_factory=lambda: uuid4().hex)
