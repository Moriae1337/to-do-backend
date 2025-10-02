from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from uuid import UUID


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[int] = 5
    done: Optional[bool] = False
    due_date: Optional[datetime] = None
    category: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    priority: Optional[int]
    done: Optional[bool]
    due_date: Optional[datetime]
    category: Optional[str]


class TaskMarkDone(BaseModel):
    done: bool = True


class TaskPriorityUpdate(BaseModel):
    priority: int


class TaskOut(TaskBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class TaskList(BaseModel):
    tasks: List[TaskOut]
    total: int
