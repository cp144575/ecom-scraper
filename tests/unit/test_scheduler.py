from ecom_scraper.request.request import Request
from ecom_scraper.scheduler.memory import MemoryScheduler


def test_scheduler_is_fifo() -> None:
    scheduler = MemoryScheduler()
    first = Request(url="https://example.com/1")
    second = Request(url="https://example.com/2")
    scheduler.add(first)
    scheduler.add(second)
    assert scheduler.next() == first
    assert scheduler.next() == second
    assert scheduler.next() is None


def test_scheduler_deduplicates_urls() -> None:
    scheduler = MemoryScheduler()
    scheduler.add(Request(url="https://example.com/1"))
    scheduler.add(Request(url="https://example.com/1"))
    assert len(scheduler) == 1


def test_scheduler_next_on_empty_returns_none() -> None:
    assert MemoryScheduler().next() is None
