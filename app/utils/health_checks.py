from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def check_postgres(session: AsyncSession) -> bool:
    try:
        result = await session.execute(text("SELECT 1"))
        return result.scalar() == 1
    except Exception as e:
        print("Postgres error:", e)
        return False
