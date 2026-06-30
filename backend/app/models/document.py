from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class DocumentType(str, enum.Enum):
    """Document types."""
    AADHAAR_CARD = "aadhaar_card"
    PAN_CARD = "pan_card"
    INCOME_CERTIFICATE = "income_certificate"
    RESIDENCE_PROOF = "residence_proof"
    BANK_STATEMENT = "bank_statement"
    OTHER = "other"


class VerificationStatus(str, enum.Enum):
    """Document verification status."""
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"


class Document(Base):
    """Document model for user uploaded documents."""
    
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_name = Column(String(255), nullable=False)
    document_type = Column(Enum(DocumentType), nullable=False)
    verification_status = Column(Enum(VerificationStatus), default=VerificationStatus.PENDING)
    extracted_text = Column(String(5000), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship
    user = relationship("User", backref="documents")
