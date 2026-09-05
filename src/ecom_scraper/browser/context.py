"""Browser context creation."""

from typing import Any


class BrowserContextFactory:
    """Creates isolated browser contexts with a shared default viewport."""

    def __init__(
        self,
        *,
        user_agent: str | None = None,
        viewport: dict[str, int] | None = None,
    ) -> None:
        self._user_agent = user_agent
        self._viewport = viewport or {"width": 1280, "height": 720}

    async def create(self, browser: Any) -> Any:
        """Create a context bound to the given browser."""
        return await browser.new_context(user_agent=self._user_agent, viewport=self._viewport)
