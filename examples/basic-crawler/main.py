"""Run a minimal crawl against books.toscrape.com."""

from ecom_scraper.config.settings import Settings
from ecom_scraper.engine.engine import Engine
from ecom_scraper.fetcher.http import HttpxFetcher
from ecom_scraper.pipeline.pipeline import Pipeline
from ecom_scraper.spider.books import BooksSpider
from ecom_scraper.storage.repository import ProductRepository
from ecom_scraper.storage.session import create_all, create_session_factory, make_engine


def main() -> None:
    settings = Settings()
    engine = make_engine(settings.database_url)
    create_all(engine)
    repository = ProductRepository(create_session_factory(engine))
    fetcher = HttpxFetcher()
    try:
        crawler = Engine(fetcher=fetcher, pipeline=Pipeline(repository))
        products = crawler.run(BooksSpider())
        for product in products:
            print(
                f"{product.platform_product_id}: {product.title} "
                f"@ {product.price} {product.currency}"
            )
        print(f"Saved {len(products)} product(s) to {settings.database_url}")
    finally:
        fetcher.close()


if __name__ == "__main__":
    main()
