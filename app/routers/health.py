from fastapi import APIRouter, status, Depends, HTTPException
from app.schemas.health import HealthCheckResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.health_checks import check_postgres
from app.db import db
from app.core.logger import AppLogger

logger = AppLogger().get_logger()

router = APIRouter(prefix="/healthcheck")


@router.get(
    "/",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    description="Returns the status of the Quiz App backend",
)
def health_check():
    logger.info("Health check endpoint '/' called")
    return HealthCheckResponse(status_code=200, detail="ok", result="working")


@router.get("/db", response_model=HealthCheckResponse)
async def postgres_health_check(session: AsyncSession = Depends(db.get_session)):
    logger.info("Health check endpoint '/db' called")
    if await check_postgres(session):
        logger.info("Postgres is working")
        return HealthCheckResponse(
            status_code=status.HTTP_200_OK, detail="ok", result="working"
        )
    logger.error("Postgres unavailable")
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Postgres unavailable"
    )
