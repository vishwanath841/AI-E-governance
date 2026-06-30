from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base


class Scheme(Base):
    """Government welfare scheme model."""
    
    __tablename__ = "schemes"
    
    id = Column(Integer, primary_key=True, index=True)
    scheme_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    eligibility_rules = Column(Text, nullable=True)  # JSON string of rules
    benefits = Column(Text, nullable=True)
    required_documents = Column(Text, nullable=True)  # JSON array of required document types
    min_income = Column(Integer, nullable=True)
    max_income = Column(Integer, nullable=True)
    age_requirement = Column(Integer, nullable=True)
    is_active = Column(Integer, default=1)  # Boolean as integer
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
