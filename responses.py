from typing import TypeVar, Generic, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum

T = TypeVar("T")


class StatusCode(str, Enum):

    SUCCESS = "success"
    ERROR = "error"
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND = "not_found"
    UNAUTHORIZED = "unauthorized"
    INTERNAL_ERROR = "internal_error"


class APIResponse(BaseModel, Generic[T]):

    status: StatusCode = Field(..., description="Response status")
    message: str = Field(..., description="Human-readable message")
    data: Optional[T] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error details")
    timestamp: str = Field(..., description="Response timestamp")

    @staticmethod
    def success(
        data: Optional[T] = None,
        message: str = "Request successful",
        timestamp: str = None
    ) -> "APIResponse[T]":
        from datetime import datetime
        return APIResponse(
            status=StatusCode.SUCCESS,
            message=message,
            data=data,
            error=None,
            timestamp=timestamp or datetime.utcnow().isoformat()
        )

    @staticmethod
    def error(
        message: str = "Request failed",
        error: str = None,
        status: StatusCode = StatusCode.ERROR,
        timestamp: str = None
    ) -> "APIResponse":
        from datetime import datetime
        return APIResponse(
            status=status,
            message=message,
            data=None,
            error=error,
            timestamp=timestamp or datetime.utcnow().isoformat()
        )

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Request successful",
                "data": {},
                "error": None,
                "timestamp": "2024-01-15T10:30:00.000000"
            }
        }
