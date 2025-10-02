from typing import AsyncContextManager, Dict, Type
from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork(AsyncContextManager):
    def __init__(self, session: AsyncSession, repos: Dict[str, Type]):
        self.session = session
        self._repos: Dict[str, Type] = {}
        for name, repo_class in repos.items():
            self._repos[name] = repo_class(session)

    def __getattr__(self, item):
        if item in self._repos:
            return self._repos[item]
        raise AttributeError(f"Repository {item} not found in this UnitOfWork")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()
