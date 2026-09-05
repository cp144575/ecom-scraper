"""Post-processing pipeline that persists canonical products."""

from typing import Protocol

from ecom_scraper.models.product import Product


class ProductSaver(Protocol):
    """A sink that persists canonical products."""

    async def save(self, product: Product) -> None: ...


class PipelineLike(Protocol):
    """A post-processing step for parsed products."""

    async def process(self, product: Product) -> None: ...


class Pipeline:
    """Validates and persists parsed products."""

    def __init__(self, repository: ProductSaver) -> None:
        self._repository = repository

    async def process(self, product: Product) -> None:
        """Persist a canonical product through the repository."""
        await self._repository.save(product)
