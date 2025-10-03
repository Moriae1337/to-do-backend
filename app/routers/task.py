from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.db.db import get_session
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskOut,
    TaskMarkDone,
    TaskPriorityUpdate,
)
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks")


def get_service(session: AsyncSession = Depends(get_session)):
    return TaskService(session)


@router.get("/", response_model=List[TaskOut])
async def list_tasks(
    search: Optional[str] = None,
    status_: Optional[str] = None,
    sort: Optional[str] = None,
    category: Optional[str] = None,
    service: TaskService = Depends(get_service),
):
    return await service.list_tasks(search, status_, sort, category)


@router.get("/{task_id}", response_model=TaskOut)
async def get_task(task_id: UUID, service: TaskService = Depends(get_service)):
    task = await service.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, service: TaskService = Depends(get_service)):
    return await service.create_task(task)


@router.put("/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: UUID, data: TaskUpdate, service: TaskService = Depends(get_service)
):
    task = await service.update_task(task_id, data)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: UUID, service: TaskService = Depends(get_service)):
    deleted = await service.delete_task(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return {"ok": True}


@router.patch("/{task_id}/done", response_model=TaskOut)
async def mark_done(
    task_id: UUID, data: TaskMarkDone, service: TaskService = Depends(get_service)
):
    task = await service.mark_done(task_id, data.done)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@router.patch("/{task_id}/priority", response_model=TaskOut)
async def change_priority(
    task_id: UUID, data: TaskPriorityUpdate, service: TaskService = Depends(get_service)
):
    task = await service.update_priority(task_id, data.priority)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task
