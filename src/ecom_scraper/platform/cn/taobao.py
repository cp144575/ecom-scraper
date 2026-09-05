"""Taobao platform adapter."""

import json
from typing import Any

from ecom_scraper.models.product import Product
from ecom_scraper.models.shop import Shop
from ecom_scraper.models.sku import ProductSKU
from ecom_scraper.normalizer.currency import normalize_currency
from ecom_scraper.normalizer.identifiers import normalize_platform_id
from ecom_scraper.normalizer.price import normalize_price
from ecom_scraper.platform.base import PlatformAdapter
from ecom_scraper.request.response import Response


class TaobaoAdapter(PlatformAdapter):
    """Parses Taobao JSON responses into canonical models."""

    name = "taobao"

    def _payload(self, response: Response) -> dict[str, Any]:
        return json.loads(response.body.decode("utf-8"))

    def parse_product(self, response: Response) -> Product:
        data = self._payload(response)
        return Product(
            platform="taobao",
            platform_product_id=normalize_platform_id(data["itemId"]),
            title=data["title"],
            url=response.url,
            price=normalize_price(data.get("price")),
            currency=normalize_currency(data.get("currency", "CNY")),
            images=list(data.get("images", [])),
        )

    def parse_shop(self, response: Response) -> Shop:
        shop = self._payload(response).get("shop") or {}
        return Shop(
            platform="taobao",
            platform_shop_id=normalize_platform_id(shop.get("shopId", "")),
            name=shop.get("shopName"),
        )

    def parse_skus(self, response: Response) -> list[ProductSKU]:
        raw_skus = self._payload(response).get("skuList", [])
        return [
            ProductSKU(
                sku_id=normalize_platform_id(item.get("skuId", "")),
                attributes=dict(item.get("properties", {})),
                price=normalize_price(item.get("price")),
                currency=normalize_currency(item.get("currency", "CNY")),
                stock=item.get("quantity"),
            )
            for item in raw_skus
        ]
