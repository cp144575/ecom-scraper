"""Task API routes."""

from fastapi import APIRouter, Depends, HTTPException, status

from ecom_scraper.api.dependencies import get_task_service
from ecom_scraper.api.schemas.task import TaskCreate
from ecom_scraper.api.services.task_service import TaskService
from ecom_scraper.models.task import Task

router = APIRouter(prefix="/tasks", tags=["tasks"])


async def _get_task_or_404(task_id: str, service: TaskService) -> Task:
    task = await service.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    return task


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_task(
    payload: TaskCreate, service: TaskService = Depends(get_task_service)
) -> Task:
    return await service.create(payload.platform, payload.product_urls)


@router.get("")
async def list_tasks(service: TaskService = Depends(get_task_service)) -> list[Task]:
    return await service.list_tasks()


@router.get("/{task_id}")
async def get_task(task_id: str, service: TaskService = Depends(get_task_service)) -> Task:
    return await _get_task_or_404(task_id, service)


@router.post("/{task_id}/start")
async def start_task(task_id: str, service: TaskService = Depends(get_task_service)) -> Task:
    task = await service.start(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    return task


@router.post("/{task_id}/stop")
async def stop_task(task_id: str, service: TaskService = Depends(get_task_service)) -> Task:
    task = await service.stop(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    return task


@router.post("/{task_id}/retry")
async def retry_task(task_id: str, service: TaskService = Depends(get_task_service)) -> Task:
    task = await service.retry(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    return task
