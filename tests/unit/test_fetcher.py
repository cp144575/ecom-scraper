import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient, TestServer

from ecom_scraper.exceptions import FetchError
from ecom_scraper.fetcher.aiohttp import AiohttpFetcher
from ecom_scraper.request.request import Request


async def test_fetcher_returns_response() -> None:
    async def handler(request: web.Request) -> web.Response:
        return web.Response(text="hello")

    app = web.Application()
    app.router.add_get("/product", handler)
    server = TestServer(app)
    client = TestClient(server)
    await client.start_server()
    try:
        fetcher = AiohttpFetcher(session=client.session)
        response = await fetcher.fetch(Request(url=str(client.make_url("/product"))))
        assert response.status_code == 200
        assert response.body == b"hello"
    finally:
        await client.close()


async def test_fetcher_wraps_connection_error() -> None:
    fetcher = AiohttpFetcher(timeout=1.0)
    try:
        with pytest.raises(FetchError):
            await fetcher.fetch(Request(url="http://127.0.0.1:1/"))
    finally:
        await fetcher.close()
