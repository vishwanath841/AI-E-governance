from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AuditLogBase(BaseModel):
    """Base audit log schema."""
    agent: str
    action: str
    result: str
    details: Optional[str] = None


class AuditLogCreate(AuditLogBase):
    """Schema for creating an audit log entry."""
    user_id: Optional[int] = None
    ip_address: Optional[str] = None


class AuditLogResponse(AuditLogBase):
    """Schema for audit log response."""
    id: int
    timestamp: datetime
    user_id: Optional[int] = None
    ip_address: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class AgentActionLog(BaseModel):
    """Schema for agent action logging."""
    agent_name: str
    action: str
    allowed: bool
    reason: Optional[str] = None
    timestamp: datetime
