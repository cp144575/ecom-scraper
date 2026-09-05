from ecom_scraper.proxy.base import Proxy
from ecom_scraper.proxy.health import ProxyHealth
from ecom_scraper.proxy.pool import ProxyPool
from ecom_scraper.proxy.selector import RoundRobinSelector


def test_round_robin_selector_cycles_within_policy() -> None:
    pool = ProxyPool(
        [
            Proxy(url="http://a", policy="residential"),
            Proxy(url="http://b", policy="residential"),
        ]
    )
    selector = RoundRobinSelector(pool)
    assert selector.select("residential") == Proxy(url="http://a", policy="residential")
    assert selector.select("residential") == Proxy(url="http://b", policy="residential")
    assert selector.select("residential") == Proxy(url="http://a", policy="residential")


def test_round_robin_selector_returns_none_for_unknown_policy() -> None:
    selector = RoundRobinSelector(ProxyPool())
    assert selector.select("residential") is None


def test_proxy_health_tracks_status() -> None:
    health = ProxyHealth()
    assert health.healthy is False
    health.record_success()
    assert health.healthy is True
    assert health.success == 1
    health.record_failure()
    assert health.healthy is False
    assert health.failure == 1
