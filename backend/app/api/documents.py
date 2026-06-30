from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.document import DocumentResponse, DocumentVerificationResult
from app.models.document import Document, DocumentType, VerificationStatus
from app.models.user import User
from app.api.auth import get_current_user
from app.agents.document_agent import DocumentAgent

router = APIRouter()
document_agent = DocumentAgent()


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    document_type: DocumentType = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a document for verification.
    """
    if not document_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document type is required"
        )
    
    # Use Document Agent to upload and process
    result = document_agent.execute_action(
        "upload_document",
        file=file,
        user_id=current_user.id,
        document_type=document_type.value
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Failed to upload document")
        )
    
    # Save document record to database
    new_document = Document(
        user_id=current_user.id,
        file_path=result["data"]["file_path"],
        file_name=result["data"]["filename"],
        document_type=document_type,
        verification_status=VerificationStatus.PENDING,
        extracted_text=result["data"]["extracted_text"]
    )
    
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    
    return DocumentResponse.model_validate(new_document)


@router.get("/", response_model=List[DocumentResponse])
async def get_user_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all documents for current user.
    """
    documents = db.query(Document).filter(
        Document.user_id == current_user.id
    ).all()
    
    return [DocumentResponse.model_validate(doc) for doc in documents]


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific document by ID.
    """
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return DocumentResponse.model_validate(document)


@router.post("/{document_id}/verify", response_model=DocumentVerificationResult)
async def verify_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Verify a document using the Document Agent.
    """
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Use Document Agent to verify
    result = document_agent.execute_action(
        "verify_document",
        file_path=document.file_path,
        document_type=document.document_type.value
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Failed to verify document")
        )
    
    # Update document verification status
    verification_data = result["data"]
    if verification_data["valid"]:
        document.verification_status = VerificationStatus.VERIFIED
    else:
        document.verification_status = VerificationStatus.REJECTED
    
    document.extracted_text = verification_data.get("extracted_text", document.extracted_text)
    
    db.commit()
    db.refresh(document)
    
    return DocumentVerificationResult(
        document_id=document_id,
        is_valid=verification_data["valid"],
        verification_status=document.verification_status,
        message=verification_data["reason"],
        extracted_text=verification_data.get("extracted_text")
    )


@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a document.
    """
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Use Document Agent to delete file
    result = document_agent.execute_action(
        "delete_document",
        file_path=document.file_path
    )
    
    # Delete database record
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}
