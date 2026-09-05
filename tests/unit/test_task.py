from ecom_scraper.api.services.task_service import TaskService
from ecom_scraper.models.task import TaskStatus


async def test_task_service_create_and_transition() -> None:
    service = TaskService()
    task = await service.create("jd", ["https://example.com/1"])
    assert task.status == TaskStatus.PENDING

    started = await service.start(task.id)
    assert started is not None
    assert started.status == TaskStatus.RUNNING
    assert started.started_at is not None

    stopped = await service.stop(task.id)
    assert stopped is not None
    assert stopped.status == TaskStatus.STOPPED
    assert stopped.finished_at is not None

    retried = await service.retry(task.id)
    assert retried is not None
    assert retried.status == TaskStatus.PENDING
    assert retried.started_at is None


async def test_task_service_get_missing() -> None:
    assert await TaskService().get("missing") is None
