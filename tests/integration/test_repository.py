from decimal import Decimal

from ecom_scraper.models.product import Product
from ecom_scraper.models.shop import Shop
from ecom_scraper.models.sku import ProductSKU
from ecom_scraper.storage.repository import AsyncProductRepository


def _product(price: str = "51.77") -> Product:
    return Product(
        platform="books",
        platform_product_id="id-1",
        title="A Light in the Attic",
        url="https://example.com/1",
        price=Decimal(price),
        currency="GBP",
    )


def _catalog_product() -> Product:
    return Product(
        platform="jd",
        platform_product_id="id-1",
        title="某商品",
        url="https://example.com/1",
        price=Decimal("99.00"),
        currency="CNY",
        shop=Shop(platform="jd", platform_shop_id="S1", name="某店"),
        skus=[
            ProductSKU(sku_id="A", price=Decimal("99.00"), stock=10),
            ProductSKU(sku_id="B", price=Decimal("109.00"), stock=20),
        ],
    )


async def test_save_and_get(repository: AsyncProductRepository) -> None:
    await repository.save(_product())
    product = await repository.get("books", "id-1")
    assert product is not None
    assert product.title == "A Light in the Attic"
    assert product.price == Decimal("51.77")


async def test_save_is_upsert(repository: AsyncProductRepository) -> None:
    await repository.save(_product())
    updated = _product(price="60.00").model_copy(update={"title": "Updated title"})
    await repository.save(updated)
    products = await repository.list_all()
    assert len(products) == 1
    assert products[0].title == "Updated title"
    assert products[0].price == Decimal("60.00")


async def test_save_persists_catalog_and_snapshots(repository: AsyncProductRepository) -> None:
    await repository.save(_catalog_product())
    product = await repository.get("jd", "id-1")
    assert product is not None
    assert product.brand is None
    prices = await repository.list_price_snapshots("jd", "id-1")
    assert len(prices) == 1
    assert prices[0].price == Decimal("99.00")
    stocks = await repository.list_inventory_snapshots("jd", "id-1")
    assert len(stocks) == 1
    assert stocks[0].stock == 30


async def test_price_snapshots_accumulate_history(repository: AsyncProductRepository) -> None:
    await repository.save(_product(price="10.00"))
    await repository.save(_product(price="12.00"))
    snapshots = await repository.list_price_snapshots("books", "id-1")
    assert [snapshot.price for snapshot in snapshots] == [Decimal("10.00"), Decimal("12.00")]
