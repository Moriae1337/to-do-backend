from datetime import datetime
from sqlalchemy import Integer, String, Boolean
from app.db.base import Base
from sqlalchemy.orm import mapped_column, Mapped
from app.core.mixins import IdMixin, DueDateMixin


class Task(Base, IdMixin, DueDateMixin):
    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    priority: Mapped[int] = mapped_column(Integer, default=5)
    category: Mapped[str] = mapped_column(String(255), nullable=True)
