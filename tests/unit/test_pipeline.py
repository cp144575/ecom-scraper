from ecom_scraper.models.product import Product
from ecom_scraper.pipeline.pipeline import Pipeline


class _SpyRepository:
    def __init__(self) -> None:
        self.saved: list[Product] = []

    async def save(self, product: Product) -> None:
        self.saved.append(product)


async def test_pipeline_persists_product() -> None:
    repository = _SpyRepository()
    pipeline = Pipeline(repository)
    product = Product(platform="p", platform_product_id="1", title="T", url="https://example.com")
    await pipeline.process(product)
    assert repository.saved == [product]
