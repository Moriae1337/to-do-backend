from pydantic import BaseModel, Field


class HealthCheckResponse(BaseModel):
    status_code: int = Field(..., description="HTTP status code of the response")
    detail: str = Field(..., description="Short description of the status")
    result: str = Field(..., description="Result message, e.g. 'working'")
