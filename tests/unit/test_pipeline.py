from ecom_scraper.models.product import Product
from ecom_scraper.pipeline.pipeline import Pipeline
from ecom_scraper.storage.repository import ProductRepository


class _SpyRepository(ProductRepository):
    def __init__(self) -> None:
        self.saved: list[Product] = []

    def save(self, product: Product) -> None:
        self.saved.append(product)


def test_pipeline_persists_product() -> None:
    repository = _SpyRepository()
    pipeline = Pipeline(repository)
    product = Product(platform="p", platform_product_id="1", title="T", url="https://example.com")
    pipeline.process(product)
    assert repository.saved == [product]
