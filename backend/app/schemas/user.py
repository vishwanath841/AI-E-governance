from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema."""
    name: str = Field(..., min_length=2, max_length=255)
    aadhaar: str = Field(..., min_length=12, max_length=12)
    mobile: str = Field(..., min_length=10, max_length=10)
    email: Optional[str] = None
    
    @validator('aadhaar')
    def validate_aadhaar(cls, v):
        if not v.isdigit():
            raise ValueError('Aadhaar must contain only digits')
        return v
    
    @validator('mobile')
    def validate_mobile(cls, v):
        if not v.isdigit():
            raise ValueError('Mobile must contain only digits')
        if not v.startswith(('6', '7', '8', '9')):
            raise ValueError('Invalid mobile number')
        return v


class UserCreate(UserBase):
    """Schema for creating a user."""
    pass


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    name: Optional[str] = None
    email: Optional[str] = None
    is_verified: Optional[bool] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    is_verified: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login."""
    aadhaar: str
    mobile: str
