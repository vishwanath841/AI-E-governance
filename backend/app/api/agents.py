from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.core.database import get_db
from app.models.user import User
from app.api.auth import get_current_user
from app.agents.coordinator_agent import CoordinatorAgent
from app.agents.verification_agent import VerificationAgent
from app.agents.document_agent import DocumentAgent
from app.agents.eligibility_agent import EligibilityAgent
from app.agents.submission_agent import SubmissionAgent
from app.agents.notification_agent import NotificationAgent
from app.core.armoriq import armoriq

router = APIRouter()

# Initialize agents
coordinator = CoordinatorAgent()
verification = VerificationAgent()
document = DocumentAgent()
eligibility = EligibilityAgent()
submission = SubmissionAgent()
notification = NotificationAgent()


@router.post("/query")
async def process_user_query(
    query_request: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Process a user query through the Coordinator Agent.
    This is the main entry point for citizen interactions.
    """
    user_query = query_request.get("query", "")
    
    if not user_query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query is required"
        )
    
    # Use Coordinator Agent to process the query
    result = coordinator.execute_action(
        "coordinate_workflow",
        user_request=user_query
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Failed to process query")
        )
    
    return result["data"]


@router.post("/verify")
async def verify_citizen(
    verification_data: dict,
    current_user: User = Depends(get_current_user)
):
    """
    Verify citizen identity using Verification Agent.
    """
    aadhaar = verification_data.get("aadhaar")
    mobile = verification_data.get("mobile")
    
    if not aadhaar or not mobile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aadhaar and mobile are required"
        )
    
    # Use Verification Agent
    result = verification.execute_action(
        "validate_identity",
        aadhaar=aadhaar,
        mobile=mobile
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Verification failed")
        )
    
    return result["data"]


@router.get("/permissions")
async def get_agent_permissions(
    agent_name: str = None,
    current_user: User = Depends(get_current_user)
):
    """
    Get permissions for agents.
    """
    permissions = armoriq.get_agent_permissions(agent_name)
    return {
        "permissions": permissions,
        "agent_name": agent_name
    }


@router.get("/status")
async def get_agent_status(current_user: User = Depends(get_current_user)):
    """
    Get status of all agents.
    """
    agents_status = {
        "coordinator_agent": {
            "status": "active",
            "permissions": coordinator.get_permissions()
        },
        "verification_agent": {
            "status": "active",
            "permissions": verification.get_permissions()
        },
        "document_agent": {
            "status": "active",
            "permissions": document.get_permissions()
        },
        "eligibility_agent": {
            "status": "active",
            "permissions": eligibility.get_permissions()
        },
        "submission_agent": {
            "status": "active",
            "permissions": submission.get_permissions()
        },
        "notification_agent": {
            "status": "active",
            "permissions": notification.get_permissions()
        }
    }
    
    return agents_status
