from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base


class AuditLog(Base):
    """Audit log model for tracking all agent actions."""
    
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    agent = Column(String(255), nullable=False, index=True)
    action = Column(String(255), nullable=False, index=True)
    result = Column(String(50), nullable=False)  # authorized, unauthorized, blocked
    details = Column(Text, nullable=True)
    user_id = Column(Integer, nullable=True, index=True)  # Optional user context
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
