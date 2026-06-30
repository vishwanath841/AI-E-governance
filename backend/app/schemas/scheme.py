from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SchemeBase(BaseModel):
    """Base scheme schema."""
    scheme_name: str = Field(..., min_length=2, max_length=255)
    description: Optional[str] = None
    eligibility_rules: str  # JSON string
    benefits: Optional[str] = None
    required_documents: str  # JSON array
    min_income: Optional[int] = None
    max_income: Optional[int] = None
    age_requirement: Optional[int] = None


class SchemeCreate(SchemeBase):
    """Schema for creating a scheme."""
    pass


class SchemeUpdate(BaseModel):
    """Schema for updating a scheme."""
    scheme_name: Optional[str] = None
    description: Optional[str] = None
    eligibility_rules: Optional[str] = None
    benefits: Optional[str] = None
    required_documents: Optional[str] = None
    min_income: Optional[int] = None
    max_income: Optional[int] = None
    age_requirement: Optional[int] = None
    is_active: Optional[bool] = None


class SchemeResponse(SchemeBase):
    """Schema for scheme response."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class EligibilityResult(BaseModel):
    """Schema for eligibility check result."""
    scheme_id: int
    scheme_name: str
    is_eligible: bool
    eligibility_score: int
    missing_documents: List[str]
    reasons: List[str]
