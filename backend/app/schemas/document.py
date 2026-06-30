from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.document import DocumentType, VerificationStatus


class DocumentBase(BaseModel):
    """Base document schema."""
    document_type: DocumentType
    file_name: str


class DocumentCreate(DocumentBase):
    """Schema for creating a document."""
    pass


class DocumentUpdate(BaseModel):
    """Schema for updating a document."""
    verification_status: Optional[VerificationStatus] = None
    extracted_text: Optional[str] = None


class DocumentResponse(DocumentBase):
    """Schema for document response."""
    id: int
    user_id: int
    file_path: str
    verification_status: VerificationStatus
    extracted_text: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class DocumentVerificationResult(BaseModel):
    """Schema for document verification result."""
    document_id: int
    is_valid: bool
    verification_status: VerificationStatus
    message: str
    extracted_text: Optional[str] = None
