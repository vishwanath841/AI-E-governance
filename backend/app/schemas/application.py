from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.application import ApplicationStatus


class ApplicationBase(BaseModel):
    """Base application schema."""
    scheme_id: int
    application_data: Optional[str] = None  # JSON string


class ApplicationCreate(ApplicationBase):
    """Schema for creating an application."""
    pass


class ApplicationUpdate(BaseModel):
    """Schema for updating an application."""
    status: Optional[ApplicationStatus] = None
    application_data: Optional[str] = None
    eligibility_score: Optional[int] = None
    rejection_reason: Optional[str] = None


class ApplicationResponse(ApplicationBase):
    """Schema for application response."""
    id: int
    user_id: int
    status: ApplicationStatus
    eligibility_score: Optional[int] = None
    rejection_reason: Optional[str] = None
    submitted_at: Optional[datetime] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ApplicationStatusResponse(BaseModel):
    """Schema for application status response."""
    application_id: int
    scheme_name: str
    status: ApplicationStatus
    eligibility_score: Optional[int] = None
    rejection_reason: Optional[str] = None
    submitted_at: Optional[datetime] = None
    last_updated: Optional[datetime] = None
