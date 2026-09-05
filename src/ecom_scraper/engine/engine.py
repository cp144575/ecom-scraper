"""Synchronous crawl engine that orchestrates the full pipeline."""

from ecom_scraper.fetcher.base import Fetcher
from ecom_scraper.models.product import Product
from ecom_scraper.pipeline.pipeline import Pipeline
from ecom_scraper.scheduler.memory import MemoryScheduler
from ecom_scraper.spider.base import Spider


class Engine:
    """Runs spiders through fetch -> parse -> pipeline."""

    def __init__(self, *, fetcher: Fetcher, pipeline: Pipeline) -> None:
        self._fetcher = fetcher
        self._pipeline = pipeline

    def run(self, spider: Spider) -> list[Product]:
        """Run a spider and return every product that was persisted."""
        scheduler = MemoryScheduler()
        for initial_request in spider.start_requests():
            scheduler.add(initial_request)

        products: list[Product] = []
        while (request := scheduler.next()) is not None:
            response = self._fetcher.fetch(request)
            product = spider.parse(response)
            if product is not None:
                self._pipeline.process(product)
                products.append(product)
        return products
