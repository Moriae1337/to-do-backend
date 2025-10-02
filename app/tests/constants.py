from fastapi import status

# test_health
HEALTHCHECK = "/healthcheck"
HEALTHCHECK_DB = "/healthcheck/db"
HEALTH_RESPONSE = {
    "status_code": status.HTTP_200_OK,
    "detail": "ok",
    "result": "working",
}
