from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.task_repository import TaskRepository
from app.db.db import get_session
from app.core.logger import AppLogger
from app.repositories.unit_of_work import UnitOfWork
from uuid import UUID
from app.schemas.task import (
    TaskCreate,
    TaskOut,
    TaskUpdate,
    TaskMarkDone,
    TaskPriorityUpdate,
)

logger = AppLogger().get_logger()
router = APIRouter(prefix="/tasks")


# GET /tasks/
@router.get("/", response_model=List[TaskOut], status_code=status.HTTP_200_OK)
async def list_tasks(
    search: Optional[str] = None,
    status: Optional[str] = None,
    sort: Optional[str] = None,
    category: Optional[str] = None,
    session: AsyncSession = Depends(get_session),
):
    async with UnitOfWork(session, {"tasks": TaskRepository}) as uow:
        try:
            tasks = await uow.tasks.get_tasks(search, status, sort, category)
            logger.info(
                f"Fetched {len(tasks)} tasks (search={search}, status={status}, sort={sort})"
            )
            return tasks
        except Exception as e:
            logger.exception("Failed to fetch tasks")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )


# GET /tasks/{task_id}
@router.get("/{task_id}", response_model=TaskOut, status_code=status.HTTP_200_OK)
async def get_task_details(task_id: UUID, session: AsyncSession = Depends(get_session)):
    async with UnitOfWork(session, {"tasks": TaskRepository}) as uow:
        task = await uow.tasks.get_by_id(task_id)
        if not task:
            logger.warning(f"Task {task_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )
        logger.info(f"Fetched task {task_id}")
        return task


# POST /tasks/
@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    task: TaskCreate, session: AsyncSession = Depends(get_session)
):
    async with UnitOfWork(session, {"tasks": TaskRepository}) as uow:
        try:
            new_task = await uow.tasks.create_task(task)
            logger.info(f"Created task {new_task.id} - {new_task.title}")
            return new_task
        except Exception as e:
            logger.exception("Failed to create task")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )


# PUT /tasks/{task_id}
@router.put("/{task_id}", response_model=TaskOut, status_code=status.HTTP_200_OK)
async def update_existing_task(
    task_id: UUID, updates: TaskUpdate, session: AsyncSession = Depends(get_session)
):
    async with UnitOfWork(session, {"tasks": TaskRepository}) as uow:
        task = await uow.tasks.get_by_id(task_id)
        if not task:
            logger.warning(f"Task {task_id} not found for update")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )
        updated_task = await uow.tasks.update_task(task, updates)
        logger.info(f"Updated task {task_id}")
        return updated_task


# DELETE /tasks/{task_id}
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_task(
    task_id: UUID, session: AsyncSession = Depends(get_session)
):
    async with UnitOfWork(session, {"tasks": TaskRepository}) as uow:
        task = await uow.tasks.get_by_id(task_id)
        if not task:
            logger.warning(f"Task {task_id} not found for deletion")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )
        await uow.tasks.delete(task)
        logger.info(f"Deleted task {task_id}")
        return {"ok": True}


# PATCH /tasks/{task_id}/done
@router.patch("/{task_id}/done", response_model=TaskOut, status_code=status.HTTP_200_OK)
async def mark_task_as_done(
    task_id: UUID, data: TaskMarkDone, session: AsyncSession = Depends(get_session)
):
    async with UnitOfWork(session, {"tasks": TaskRepository}) as uow:
        task = await uow.tasks.get_by_id(task_id)
        if not task:
            logger.warning(f"Task {task_id} not found for marking done")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )
        task = await uow.tasks.mark_done(task, done=data.done)
        logger.info(f"Task {task_id} marked as {'done' if data.done else 'undone'}")
        return task


# PATCH /tasks/{task_id}/priority
@router.patch(
    "/{task_id}/priority", response_model=TaskOut, status_code=status.HTTP_200_OK
)
async def change_task_priority(
    task_id: UUID,
    data: TaskPriorityUpdate,
    session: AsyncSession = Depends(get_session),
):
    async with UnitOfWork(session, {"tasks": TaskRepository}) as uow:
        task = await uow.tasks.get_by_id(task_id)
        if not task:
            logger.warning(f"Task {task_id} not found for priority update")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )
        task = await uow.tasks.update_priority(task, data.priority)
        logger.info(f"Task {task_id} priority updated to {data.priority}")
        return task
