from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.repositories.base_repository import AsyncRepository


class TaskRepository(AsyncRepository[Task]):
    def __init__(self, session: AsyncSession):
        super().__init__(Task, session)

    async def get_tasks(
        self,
        search: Optional[str] = None,
        status: Optional[str] = None,
        sort: Optional[str] = None,
        category: Optional[str] = None,
    ) -> List[Task]:
        query = select(Task)

        # Search by title or description
        if search:
            query = query.where(
                or_(
                    Task.title.ilike(f"%{search}%"),
                    Task.description.ilike(f"%{search}%"),
                )
            )

        # Filter by status
        if status == "done":
            query = query.where(Task.done.is_(True))
        elif status == "undone":
            query = query.where(Task.done.is_(False))

        # Filter by category
        if category:
            query = query.where(Task.category == category)

        # Sorting
        if sort == "priority_asc":
            query = query.order_by(Task.priority.asc())
        elif sort == "priority_desc":
            query = query.order_by(Task.priority.desc())
        elif sort == "due_date_asc":
            query = query.order_by(Task.due_date.asc())
        elif sort == "due_date_desc":
            query = query.order_by(Task.due_date.desc())

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, task_id: int) -> Optional[Task]:
        result = await self.session.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()

    async def create_task(self, task_data: TaskCreate) -> Task:
        task = Task(**task_data.model_dump())
        self.session.add(task)
        return task

    async def update_task(self, task: Task, updates: TaskUpdate) -> Task:
        for key, value in updates.model_dump(exclude_unset=True).items():
            setattr(task, key, value)
        self.session.add(task)
        return task

    async def delete_task(self, task: Task) -> None:
        await self.session.delete(task)

    async def mark_done(self, task: Task, done: bool = True) -> Task:
        task.done = done
        self.session.add(task)
        return task

    async def update_priority(self, task: Task, priority: int) -> Task:
        task.priority = priority
        self.session.add(task)
        return task
