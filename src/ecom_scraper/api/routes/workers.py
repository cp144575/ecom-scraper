"""Worker API routes."""

from fastapi import APIRouter, Depends

from ecom_scraper.api.dependencies import get_worker_registry
from ecom_scraper.distributed.coordination import WorkerRegistry

router = APIRouter(prefix="/workers", tags=["workers"])


@router.get("")
async def list_workers(
    registry: WorkerRegistry | None = Depends(get_worker_registry),
) -> list[str]:
    """Return the ids of known workers."""
    if registry is None:
        return []
    return await registry.list_workers()


@router.get("/{worker_id}")
async def get_worker(
    worker_id: str,
    registry: WorkerRegistry | None = Depends(get_worker_registry),
) -> dict[str, str]:
    """Return the status of a worker."""
    if registry is None:
        return {"worker_id": worker_id, "status": "unknown", "load": "0"}
    return await registry.get_worker(worker_id)
