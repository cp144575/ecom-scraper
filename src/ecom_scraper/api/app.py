"""FastAPI application factory."""

from fastapi import FastAPI
from fastapi.responses import Response

from ecom_scraper.api.routes import analytics, platforms, products, tasks, workers
from ecom_scraper.api.services.task_service import TaskService
from ecom_scraper.distributed.coordination import WorkerRegistry
from ecom_scraper.observability.metrics import render_metrics
from ecom_scraper.storage.repository import AsyncProductRepository


def create_app(
    *,
    task_service: TaskService | None = None,
    repository: AsyncProductRepository | None = None,
    worker_registry: WorkerRegistry | None = None,
) -> FastAPI:
    """Build the FastAPI app with the given dependencies."""
    app = FastAPI(title="ecom-scraper", version="0.5.0")
    app.state.task_service = task_service or TaskService()
    app.state.repository = repository
    app.state.worker_registry = worker_registry

    app.include_router(tasks.router)
    app.include_router(platforms.router)
    app.include_router(workers.router)
    app.include_router(products.router)
    app.include_router(analytics.router)

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/metrics")
    async def metrics() -> Response:
        return Response(content=render_metrics(), media_type="text/plain")

    return app


app = create_app()
