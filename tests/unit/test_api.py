from collections.abc import AsyncIterator
from decimal import Decimal

import httpx
import pytest

from ecom_scraper.api.app import create_app
from ecom_scraper.api.services.task_service import TaskService
from ecom_scraper.models.product import Product
from ecom_scraper.models.snapshot import InventorySnapshot, PriceSnapshot


@pytest.fixture()
async def client() -> AsyncIterator[httpx.AsyncClient]:
    app = create_app(task_service=TaskService())
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as http_client:
        yield http_client


async def test_health(client: httpx.AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_platforms(client: httpx.AsyncClient) -> None:
    response = await client.get("/platforms")
    assert response.json() == ["jd", "taobao", "amazon"]


async def test_task_lifecycle(client: httpx.AsyncClient) -> None:
    created = await client.post(
        "/tasks", json={"platform": "jd", "product_urls": ["https://example.com/1"]}
    )
    assert created.status_code == 201
    task = created.json()
    task_id = task["id"]
    assert task["status"] == "pending"

    assert len((await client.get("/tasks")).json()) == 1
    assert (await client.post(f"/tasks/{task_id}/start")).json()["status"] == "running"
    assert (await client.post(f"/tasks/{task_id}/stop")).json()["status"] == "stopped"
    assert (await client.post(f"/tasks/{task_id}/retry")).json()["status"] == "pending"


async def test_task_not_found(client: httpx.AsyncClient) -> None:
    assert (await client.get("/tasks/nope")).status_code == 404


async def test_metrics_endpoint(client: httpx.AsyncClient) -> None:
    response = await client.get("/metrics")
    assert response.status_code == 200
    assert "crawler_requests_total" in response.text


class _FakeRepository:
    async def list_all(self) -> list[Product]:
        return [
            Product(platform="jd", platform_product_id="1", title="A", url="u", price=Decimal("10"))
        ]

    async def list_price_snapshots(self, platform: str, product_id: str) -> list[PriceSnapshot]:
        return [
            PriceSnapshot(platform=platform, platform_product_id=product_id, price=Decimal("10"))
        ]

    async def list_inventory_snapshots(
        self, platform: str, product_id: str
    ) -> list[InventorySnapshot]:
        return [InventorySnapshot(platform=platform, platform_product_id=product_id, stock=5)]


async def test_analytics_with_repository() -> None:
    app = create_app(repository=_FakeRepository())
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as http_client:
        assert (await http_client.get("/analytics/products")).json() == {"count": 1}
        prices = (await http_client.get("/analytics/prices?platform=jd&product_id=1")).json()
        assert prices["min"] == "10"
        assert (await http_client.get("/analytics/platforms")).json() == {"jd": "10"}
