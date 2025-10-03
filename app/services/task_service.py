from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Optional

from app.repositories.unit_of_work import UnitOfWork
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.core.logger import AppLogger

logger = AppLogger().get_logger()


class TaskService:
    def __init__(self, session: AsyncSession):
        self.uow = UnitOfWork(session, {"tasks": TaskRepository})

    async def list_tasks(
        self,
        search: Optional[str],
        status: Optional[str],
        sort: Optional[str],
        category: Optional[str],
    ) -> List[TaskOut]:
        async with self.uow:
            tasks = await self.uow.tasks.get_tasks(search, status, sort, category)
            logger.info(f"Fetched {len(tasks)} tasks")
            return tasks

    async def get_task(self, task_id: UUID) -> TaskOut:
        async with self.uow:
            task = await self.uow.tasks.get_by_id(task_id)
            return task

    async def create_task(self, data: TaskCreate) -> TaskOut:
        async with self.uow:
            new_task = await self.uow.tasks.create_task(data)
            logger.info(f"Created task {new_task.id}")
            return new_task

    async def update_task(self, task_id: UUID, data: TaskUpdate) -> TaskOut:
        async with self.uow:
            task = await self.uow.tasks.get_by_id(task_id)
            if not task:
                return None
            return await self.uow.tasks.update_task(task, data)

    async def delete_task(self, task_id: UUID) -> bool:
        async with self.uow:
            task = await self.uow.tasks.get_by_id(task_id)
            if not task:
                return False
            await self.uow.tasks.delete(task)
            return True

    async def mark_done(self, task_id: UUID, done: bool) -> TaskOut | None:
        async with self.uow:
            task = await self.uow.tasks.get_by_id(task_id)
            if not task:
                return None
            return await self.uow.tasks.mark_done(task, done)

    async def update_priority(self, task_id: UUID, priority: int) -> TaskOut | None:
        async with self.uow:
            task = await self.uow.tasks.get_by_id(task_id)
            if not task:
                return None
            return await self.uow.tasks.update_priority(task, priority)
