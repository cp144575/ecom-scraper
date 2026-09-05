"""FastAPI dependencies."""

from fastapi import Request

from ecom_scraper.api.services.task_service import TaskService
from ecom_scraper.distributed.coordination import WorkerRegistry
from ecom_scraper.storage.repository import AsyncProductRepository


def get_task_service(request: Request) -> TaskService:
    """Return the task service bound to the app."""
    return request.app.state.task_service


def get_repository(request: Request) -> AsyncProductRepository | None:
    """Return the product repository bound to the app, or None."""
    return getattr(request.app.state, "repository", None)


def get_worker_registry(request: Request) -> WorkerRegistry | None:
    """Return the worker registry bound to the app, or None."""
    return getattr(request.app.state, "worker_registry", None)
