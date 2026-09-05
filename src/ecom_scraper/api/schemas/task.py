"""Task API schemas."""

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Payload for creating a crawl task."""

    platform: str
    product_urls: list[str] = Field(default_factory=list)
