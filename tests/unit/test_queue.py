import asyncio

from ecom_scraper.queue.memory import MemoryQueue
from ecom_scraper.request.request import Request


async def test_memory_queue_is_fifo_and_dedups() -> None:
    queue = MemoryQueue()
    first = Request(url="https://example.com/1")
    assert await queue.put(first) is True
    assert await queue.put(first) is False
    assert await queue.put(Request(url="https://example.com/2")) is True

    item = await queue.get()
    assert item.url == "https://example.com/1"
    assert (await queue.get()).url == "https://example.com/2"


async def test_memory_queue_backpressure_blocks_when_full() -> None:
    queue = MemoryQueue(maxsize=1)
    assert await queue.put(Request(url="https://example.com/1")) is True
    second_put = asyncio.create_task(queue.put(Request(url="https://example.com/2")))
    await asyncio.sleep(0.01)
    assert not second_put.done()

    item = await queue.get()
    assert item.url == "https://example.com/1"
    assert await second_put is True
