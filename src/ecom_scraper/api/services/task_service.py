"""In-memory task lifecycle service."""

from datetime import UTC, datetime
from uuid import uuid4

from ecom_scraper.models.task import Task, TaskStatus


class TaskService:
    """Creates and transitions crawl tasks in an in-memory store."""

    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}

    async def create(self, platform: str, product_urls: list[str]) -> Task:
        """Create a pending task."""
        task = Task(
            id=uuid4().hex,
            platform=platform,
            product_urls=product_urls,
        )
        self._tasks[task.id] = task
        return task

    async def get(self, task_id: str) -> Task | None:
        """Return a task by id, or None."""
        return self._tasks.get(task_id)

    async def list_tasks(self) -> list[Task]:
        """Return all tasks."""
        return list(self._tasks.values())

    async def start(self, task_id: str) -> Task | None:
        """Mark a task running."""
        return await self._transition(task_id, TaskStatus.RUNNING, started=True)

    async def stop(self, task_id: str) -> Task | None:
        """Mark a task stopped."""
        return await self._transition(task_id, TaskStatus.STOPPED, finished=True)

    async def retry(self, task_id: str) -> Task | None:
        """Reset a task back to pending."""
        task = self._tasks.get(task_id)
        if task is None:
            return None
        updated = task.model_copy(
            update={
                "status": TaskStatus.PENDING,
                "started_at": None,
                "finished_at": None,
            }
        )
        self._tasks[task_id] = updated
        return updated

    async def complete(self, task_id: str) -> Task | None:
        """Mark a task completed."""
        return await self._transition(task_id, TaskStatus.COMPLETED, finished=True)

    async def fail(self, task_id: str) -> Task | None:
        """Mark a task failed."""
        return await self._transition(task_id, TaskStatus.FAILED, finished=True)

    async def _transition(
        self,
        task_id: str,
        status: TaskStatus,
        *,
        started: bool = False,
        finished: bool = False,
    ) -> Task | None:
        task = self._tasks.get(task_id)
        if task is None:
            return None
        now = datetime.now(UTC)
        update: dict[str, object] = {"status": status}
        if started:
            update["started_at"] = now
        if finished:
            update["finished_at"] = now
        updated = task.model_copy(update=update)
        self._tasks[task_id] = updated
        return updated
