"""Browser lifecycle protocol."""

from typing import Protocol


class BrowserLifecycle(Protocol):
    """Start/stop contract for browser-backed components."""

    async def start(self) -> None: ...

    async def stop(self) -> None: ...
