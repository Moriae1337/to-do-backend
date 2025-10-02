from typing import TypeVar, Generic, Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

T = TypeVar("T")


class AsyncRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_all(self) -> list[T]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def get_by_id(self, id) -> Optional[T]:
        return await self.session.get(self.model, id)

    async def add(self, obj: T):
        self.session.add(obj)

    async def delete(self, obj: T):
        await self.session.delete(obj)
