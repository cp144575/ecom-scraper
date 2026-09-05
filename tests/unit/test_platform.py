from decimal import Decimal
from pathlib import Path

from ecom_scraper.platform.base import PlatformSpider
from ecom_scraper.platform.cn.jd import JdAdapter
from ecom_scraper.platform.cn.taobao import TaobaoAdapter
from ecom_scraper.platform.intl.amazon import AmazonAdapter
from ecom_scraper.request.request import Request
from ecom_scraper.request.response import Response

_FIXTURES = Path(__file__).parent.parent / "fixtures" / "json"


def _response(name: str) -> Response:
    body = (_FIXTURES / name).read_bytes()
    request = Request(url=f"https://example.com/{name}")
    return Response(request=request, url=request.url, status_code=200, headers={}, body=body)


def test_jd_adapter_parses_product() -> None:
    adapter = JdAdapter()
    response = _response("jd_product.json")
    product = adapter.parse_product(response)
    assert product.platform == "jd"
    assert product.platform_product_id == "100012043978"
    assert product.price == Decimal("3999.00")
    assert product.currency == "CNY"
    assert product.brand == "某品牌"
    assert adapter.parse_shop(response).platform_shop_id == "1000004123"
    skus = adapter.parse_skus(response)
    assert len(skus) == 2
    assert skus[0].attributes == {"颜色": "黑色"}
    assert skus[1].stock == 0


def test_taobao_adapter_parses_product() -> None:
    adapter = TaobaoAdapter()
    response = _response("taobao_product.json")
    product = adapter.parse_product(response)
    assert product.platform == "taobao"
    assert product.platform_product_id == "654321"
    assert product.price == Decimal("199.00")
    assert adapter.parse_shop(response).name == "某旗舰店"
    assert [sku.sku_id for sku in adapter.parse_skus(response)] == ["S1", "S2"]


def test_amazon_adapter_parses_product() -> None:
    adapter = AmazonAdapter()
    response = _response("amazon_product.json")
    product = adapter.parse_product(response)
    assert product.platform == "amazon"
    assert product.platform_product_id == "B0ABC123"
    assert product.price == Decimal("49.99")
    assert product.currency == "USD"
    assert adapter.parse_shop(response).platform_shop_id == "A1B2C3D4"
    assert len(adapter.parse_skus(response)) == 2


def test_platform_spider_assembles_and_validates() -> None:
    adapter = JdAdapter()
    spider = PlatformSpider(adapter, ["https://example.com/jd_product.json"])
    product = spider.parse(_response("jd_product.json"))
    assert product is not None
    assert product.shop is not None
    assert product.shop.name == "某品牌京东自营旗舰店"
    assert len(product.skus) == 2
