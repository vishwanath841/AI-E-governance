import os
import pytesseract
from PIL import Image
from typing import Dict, Any, Optional
from pathlib import Path
from app.agents.base_agent import BaseAgent
from app.core.config import settings


class DocumentAgent(BaseAgent):
    """
    Document Verification Agent - Processes and verifies user documents.
    
    Responsibilities:
    - Accept PDF/JPG uploads
    - Extract text using OCR
    - Verify required documents exist
    - Return verification result
    """
    
    def __init__(self):
        super().__init__("document_agent")
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(exist_ok=True)
    
    def _perform_action(self, action: str, **kwargs) -> Any:
        """Perform document-specific actions."""
        if action == "upload_document":
            return self._upload_document(
                kwargs.get("file"),
                kwargs.get("user_id"),
                kwargs.get("document_type")
            )
        elif action == "extract_text":
            return self._extract_text(kwargs.get("file_path"))
        elif action == "verify_document":
            return self._verify_document(
                kwargs.get("file_path"),
                kwargs.get("document_type")
            )
        elif action == "delete_document":
            return self._delete_document(kwargs.get("file_path"))
        elif action == "get_document":
            return self._get_document(kwargs.get("document_id"))
        else:
            raise ValueError(f"Unknown action: {action}")
    
    def _upload_document(self, file, user_id: int, document_type: str) -> Dict[str, Any]:
        """
        Upload and process a document.
        
        Args:
            file: The uploaded file
            user_id: The user ID
            document_type: The type of document
            
        Returns:
            Dictionary containing upload result
        """
        try:
            # Generate unique filename
            file_extension = Path(file.filename).suffix
            filename = f"{user_id}_{document_type}_{file.filename}"
            file_path = self.upload_dir / filename
            
            # Save file
            with open(file_path, "wb") as buffer:
                content = file.file.read()
                buffer.write(content)
            
            # Extract text from document
            extracted_text = self._extract_text(str(file_path))
            
            return {
                "success": True,
                "file_path": str(file_path),
                "filename": filename,
                "document_type": document_type,
                "extracted_text": extracted_text,
                "message": "Document uploaded successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to upload document"
            }
    
    def _extract_text(self, file_path: str) -> str:
        """
        Extract text from document using OCR.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Extracted text
        """
        try:
            # Check if file is an image
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
                image = Image.open(file_path)
                text = pytesseract.image_to_string(image)
                return text.strip()
            else:
                # For PDF files, in production you'd use pdf2image or similar
                # For MVP, we'll return a placeholder
                return "PDF text extraction - requires additional dependencies"
                
        except Exception as e:
            return f"OCR extraction failed: {str(e)}"
    
    def _verify_document(self, file_path: str, document_type: str) -> Dict[str, Any]:
        """
        Verify a document meets requirements.
        
        Args:
            file_path: Path to the document
            document_type: Expected document type
            
        Returns:
            Dictionary containing verification result
        """
        if not os.path.exists(file_path):
            return {
                "valid": False,
                "reason": "File not found"
            }
        
        # Extract text
        extracted_text = self._extract_text(file_path)
        
        # Basic validation based on document type
        validation_rules = {
            "aadhaar_card": self._validate_aadhaar_document,
            "pan_card": self._validate_pan_document,
            "income_certificate": self._validate_income_certificate,
            "residence_proof": self._validate_residence_proof,
            "bank_statement": self._validate_bank_statement
        }
        
        validator = validation_rules.get(document_type, lambda x: {"valid": True, "reason": "Document type recognized"})
        validation_result = validator(extracted_text)
        
        return {
            "valid": validation_result["valid"],
            "reason": validation_result["reason"],
            "extracted_text": extracted_text,
            "document_type": document_type
        }
    
    def _validate_aadhaar_document(self, text: str) -> Dict[str, Any]:
        """Validate Aadhaar card document."""
        # Check for Aadhaar number pattern in extracted text
        import re
        aadhaar_pattern = r'\d{4}\s*\d{4}\s*\d{4}'
        if re.search(aadhaar_pattern, text):
            return {"valid": True, "reason": "Aadhaar number detected"}
        return {"valid": False, "reason": "Aadhaar number not found"}
    
    def _validate_pan_document(self, text: str) -> Dict[str, Any]:
        """Validate PAN card document."""
        import re
        pan_pattern = r'[A-Z]{5}[0-9]{4}[A-Z]{1}'
        if re.search(pan_pattern, text.upper()):
            return {"valid": True, "reason": "PAN number detected"}
        return {"valid": False, "reason": "PAN number not found"}
    
    def _validate_income_certificate(self, text: str) -> Dict[str, Any]:
        """Validate income certificate."""
        keywords = ["income", "certificate", "salary", "earnings"]
        text_lower = text.lower()
        if any(keyword in text_lower for keyword in keywords):
            return {"valid": True, "reason": "Income certificate keywords detected"}
        return {"valid": False, "reason": "Income certificate not validated"}
    
    def _validate_residence_proof(self, text: str) -> Dict[str, Any]:
        """Validate residence proof document."""
        keywords = ["address", "residence", "proof", "electricity", "water"]
        text_lower = text.lower()
        if any(keyword in text_lower for keyword in keywords):
            return {"valid": True, "reason": "Residence proof keywords detected"}
        return {"valid": False, "reason": "Residence proof not validated"}
    
    def _validate_bank_statement(self, text: str) -> Dict[str, Any]:
        """Validate bank statement."""
        keywords = ["bank", "statement", "account", "balance"]
        text_lower = text.lower()
        if any(keyword in text_lower for keyword in keywords):
            return {"valid": True, "reason": "Bank statement keywords detected"}
        return {"valid": False, "reason": "Bank statement not validated"}
    
    def _delete_document(self, file_path: str) -> Dict[str, Any]:
        """
        Delete a document.
        
        Args:
            file_path: Path to the document to delete
            
        Returns:
            Dictionary containing deletion result
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return {
                    "success": True,
                    "message": "Document deleted successfully"
                }
            else:
                return {
                    "success": False,
                    "message": "File not found"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to delete document"
            }
    
    def _get_document(self, document_id: int) -> Dict[str, Any]:
        """
        Get document information.
        
        Args:
            document_id: The document ID
            
        Returns:
            Dictionary containing document information
        """
        # In a real implementation, this would query the database
        return {
            "document_id": document_id,
            "message": "Document retrieved"
        }
