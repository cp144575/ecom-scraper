from decimal import Decimal

from ecom_scraper.models.product import Product
from ecom_scraper.storage.repository import AsyncProductRepository


def _product() -> Product:
    return Product(
        platform="books",
        platform_product_id="id-1",
        title="A Light in the Attic",
        url="https://example.com/1",
        price=Decimal("51.77"),
        currency="GBP",
    )


async def test_save_and_get(repository: AsyncProductRepository) -> None:
    await repository.save(_product())
    product = await repository.get("books", "id-1")
    assert product is not None
    assert product.title == "A Light in the Attic"
    assert product.price == Decimal("51.77")


async def test_save_is_upsert(repository: AsyncProductRepository) -> None:
    await repository.save(_product())
    updated = _product().model_copy(update={"title": "Updated title"})
    await repository.save(updated)
    products = await repository.list_all()
    assert len(products) == 1
    assert products[0].title == "Updated title"
