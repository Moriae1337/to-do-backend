from fastapi import status
import pytest
from .constants import HEALTHCHECK, HEALTHCHECK_DB, HEALTH_RESPONSE


def assert_health_response(response):
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == HEALTH_RESPONSE


def test_health_check(client):
    response = client.get(HEALTHCHECK)
    assert_health_response(response)


@pytest.mark.asyncio
async def test_health_db(async_client):
    response = await async_client.get(HEALTHCHECK_DB)
    assert_health_response(response)
