"""Proxy value object."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Proxy:
    """A proxy endpoint with an optional policy tag."""

    url: str
    policy: str = "default"
    username: str | None = None
    password: str | None = None
