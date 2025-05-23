from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from typing import Any, Dict, Optional, List


class ExternalDataBase(BaseModel):
    endpoint: str = Field(..., min_length=1, max_length=255, description="API endpoint")
    data: Dict[str, Any] = Field(..., description="Response data")
    status_code: int = Field(..., ge=100, le=599, description="HTTP status code")
    
    @field_validator('endpoint')
    @classmethod
    def validate_endpoint(cls, v):
        if not v.strip():
            raise ValueError('Endpoint cannot be empty or whitespace')
        return v.strip()
    
    @field_validator('status_code')
    @classmethod
    def validate_status_code(cls, v):
        if not (100 <= v <= 599):
            raise ValueError('Status code must be between 100 and 599')
        return v


class ExternalDataCreate(ExternalDataBase):
    pass


class ExternalDataResponse(ExternalDataBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")


class ApiResponse(BaseModel):
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error message if any")
    status_code: Optional[int] = Field(None, description="HTTP status code")
    stored_id: Optional[int] = Field(None, description="Database record ID")


class HealthCheckResponse(BaseModel):
    status: str = Field(..., description="Health status")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Check timestamp")
    version: str = Field(default="1.0.0", description="API version")
    database_connected: bool = Field(..., description="Database connection status")


class ExternalDataListResponse(BaseModel):
    success: bool = Field(..., description="Operation success status")
    data: List[ExternalDataResponse] = Field(..., description="List of external data records")
    total: int = Field(..., description="Total number of records")
    limit: int = Field(..., description="Applied limit")


class ErrorResponse(BaseModel):
    success: bool = Field(default=False, description="Always false for errors")
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    status_code: int = Field(..., description="HTTP status code")
