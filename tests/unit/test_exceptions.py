from ecom_scraper.exceptions import EcomScraperError, FetchError


def test_fetch_error_is_ecom_scraper_error() -> None:
    assert issubclass(FetchError, EcomScraperError)
