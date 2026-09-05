"""Post-processing pipeline that persists canonical products."""

from ecom_scraper.models.product import Product
from ecom_scraper.storage.repository import ProductRepository


class Pipeline:
    """Validates and persists parsed products."""

    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository

    def process(self, product: Product) -> None:
        """Persist a canonical product through the repository."""
        self._repository.save(product)
