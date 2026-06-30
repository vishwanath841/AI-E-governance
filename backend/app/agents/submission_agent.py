import json
from datetime import datetime
from typing import Dict, Any, Optional
from app.agents.base_agent import BaseAgent


class SubmissionAgent(BaseAgent):
    """
    Application Submission Agent - Handles scheme application submission.
    
    Responsibilities:
    - Generate application form
    - Simulate submission
    - Store application status
    - Update application details
    """
    
    def __init__(self):
        super().__init__("submission_agent")
    
    def _perform_action(self, action: str, **kwargs) -> Any:
        """Perform submission-specific actions."""
        if action == "generate_form":
            return self._generate_application_form(
                kwargs.get("scheme_id"),
                kwargs.get("user_profile")
            )
        elif action == "submit_application":
            return self._submit_application(
                kwargs.get("user_id"),
                kwargs.get("scheme_id"),
                kwargs.get("application_data")
            )
        elif action == "update_status":
            return self._update_application_status(
                kwargs.get("application_id"),
                kwargs.get("status"),
                kwargs.get("rejection_reason")
            )
        elif action == "get_application":
            return self._get_application(kwargs.get("application_id"))
        else:
            raise ValueError(f"Unknown action: {action}")
    
    def _generate_application_form(self, scheme_id: int, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate an application form for a specific scheme.
        
        Args:
            scheme_id: The scheme ID
            user_profile: User profile information
            
        Returns:
            Dictionary containing the generated form
        """
        # Mock scheme data - in production, fetch from database
        scheme_forms = {
            1: {
                "scheme_name": "Pradhan Mantri Awas Yojana",
                "form_fields": [
                    {
                        "field_name": "full_name",
                        "field_type": "text",
                        "label": "Full Name",
                        "required": True,
                        "value": user_profile.get("name", "")
                    },
                    {
                        "field_name": "aadhaar_number",
                        "field_type": "text",
                        "label": "Aadhaar Number",
                        "required": True,
                        "value": user_profile.get("aadhaar", "")
                    },
                    {
                        "field_name": "annual_income",
                        "field_type": "number",
                        "label": "Annual Income (INR)",
                        "required": True,
                        "value": user_profile.get("income", "")
                    },
                    {
                        "field_name": "residence_type",
                        "field_type": "select",
                        "label": "Residence Type",
                        "required": True,
                        "options": ["rural", "urban"],
                        "value": user_profile.get("residence_type", "")
                    },
                    {
                        "field_name": "current_address",
                        "field_type": "textarea",
                        "label": "Current Address",
                        "required": True,
                        "value": ""
                    },
                    {
                        "field_name": "bank_account_number",
                        "field_type": "text",
                        "label": "Bank Account Number",
                        "required": True,
                        "value": ""
                    },
                    {
                        "field_name": "ifsc_code",
                        "field_type": "text",
                        "label": "IFSC Code",
                        "required": True,
                        "value": ""
                    }
                ]
            },
            2: {
                "scheme_name": "National Health Protection Scheme",
                "form_fields": [
                    {
                        "field_name": "full_name",
                        "field_type": "text",
                        "label": "Full Name",
                        "required": True,
                        "value": user_profile.get("name", "")
                    },
                    {
                        "field_name": "aadhaar_number",
                        "field_type": "text",
                        "label": "Aadhaar Number",
                        "required": True,
                        "value": user_profile.get("aadhaar", "")
                    },
                    {
                        "field_name": "family_members",
                        "field_type": "number",
                        "label": "Number of Family Members",
                        "required": True,
                        "value": user_profile.get("family_size", "")
                    },
                    {
                        "field_name": "bpl_card_number",
                        "field_type": "text",
                        "label": "BPL Card Number",
                        "required": True,
                        "value": ""
                    }
                ]
            }
        }
        
        form_data = scheme_forms.get(scheme_id, {
            "scheme_name": "General Application Form",
            "form_fields": []
        })
        
        return {
            "scheme_id": scheme_id,
            "form": form_data,
            "generated_at": datetime.utcnow().isoformat(),
            "message": "Application form generated successfully"
        }
    
    def _submit_application(self, user_id: int, scheme_id: int, application_data: str) -> Dict[str, Any]:
        """
        Submit an application for a scheme.
        
        Args:
            user_id: The user ID
            scheme_id: The scheme ID
            application_data: JSON string of application data
            
        Returns:
            Dictionary containing submission result
        """
        try:
            # Parse application data
            form_data = json.loads(application_data) if application_data else {}
            
            # Validate required fields
            validation_result = self._validate_application_data(form_data)
            if not validation_result["valid"]:
                return {
                    "success": False,
                    "error": validation_result["error"],
                    "message": "Application validation failed"
                }
            
            # In a real implementation, this would save to the database
            # application = Application(
            #     user_id=user_id,
            #     scheme_id=scheme_id,
            #     status=ApplicationStatus.SUBMITTED,
            #     application_data=application_data,
            #     submitted_at=datetime.utcnow()
            # )
            # db.add(application)
            # db.commit()
            
            # Generate application ID (mock)
            application_id = f"APP{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
            
            return {
                "success": True,
                "application_id": application_id,
                "user_id": user_id,
                "scheme_id": scheme_id,
                "status": "submitted",
                "submitted_at": datetime.utcnow().isoformat(),
                "message": "Application submitted successfully"
            }
            
        except json.JSONDecodeError:
            return {
                "success": False,
                "error": "Invalid application data format",
                "message": "Application submission failed"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Application submission failed"
            }
    
    def _validate_application_data(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate application form data.
        
        Args:
            form_data: Dictionary containing form data
            
        Returns:
            Dictionary containing validation result
        """
        # Basic validation - check for required fields
        required_fields = ["full_name", "aadhaar_number"]
        
        for field in required_fields:
            if field not in form_data or not form_data[field]:
                return {
                    "valid": False,
                    "error": f"Required field '{field}' is missing or empty"
                }
        
        # Validate Aadhaar format
        aadhaar = form_data.get("aadhaar_number", "")
        if not aadhaar or len(aadhaar) != 12 or not aadhaar.isdigit():
            return {
                "valid": False,
                "error": "Invalid Aadhaar number format"
            }
        
        return {
            "valid": True,
            "message": "Application data is valid"
        }
    
    def _update_application_status(self, application_id: str, status: str, rejection_reason: Optional[str] = None) -> Dict[str, Any]:
        """
        Update the status of an application.
        
        Args:
            application_id: The application ID
            status: New status
            rejection_reason: Optional rejection reason
            
        Returns:
            Dictionary containing update result
        """
        # Valid statuses
        valid_statuses = ["draft", "submitted", "under_review", "approved", "rejected"]
        
        if status not in valid_statuses:
            return {
                "success": False,
                "error": f"Invalid status. Must be one of: {valid_statuses}"
            }
        
        # In a real implementation, this would update the database
        # application = db.query(Application).filter(Application.id == application_id).first()
        # if application:
        #     application.status = status
        #     if rejection_reason:
        #         application.rejection_reason = rejection_reason
        #     if status == "under_review":
        #         application.reviewed_at = datetime.utcnow()
        #     db.commit()
        
        return {
            "success": True,
            "application_id": application_id,
            "new_status": status,
            "rejection_reason": rejection_reason,
            "updated_at": datetime.utcnow().isoformat(),
            "message": "Application status updated successfully"
        }
    
    def _get_application(self, application_id: str) -> Dict[str, Any]:
        """
        Get application details.
        
        Args:
            application_id: The application ID
            
        Returns:
            Dictionary containing application details
        """
        # In a real implementation, this would query the database
        return {
            "application_id": application_id,
            "status": "submitted",
            "submitted_at": "2024-01-01T00:00:00",
            "message": "Application retrieved successfully"
        }
