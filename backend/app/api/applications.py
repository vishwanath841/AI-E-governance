from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.application import ApplicationResponse, ApplicationStatusResponse, ApplicationCreate
from app.models.application import Application, ApplicationStatus
from app.models.scheme import Scheme
from app.models.user import User
from app.api.auth import get_current_user
from app.agents.submission_agent import SubmissionAgent
from app.agents.notification_agent import NotificationAgent

router = APIRouter()
submission_agent = SubmissionAgent()
notification_agent = NotificationAgent()


@router.post("/", response_model=ApplicationResponse)
async def create_application(
    application_data: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new application for a scheme.
    """
    # Check if scheme exists
    scheme = db.query(Scheme).filter(
        Scheme.id == application_data.scheme_id,
        Scheme.is_active == 1
    ).first()
    
    if not scheme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheme not found"
        )
    
    # Check if user already has an active application for this scheme
    existing_application = db.query(Application).filter(
        Application.user_id == current_user.id,
        Application.scheme_id == application_data.scheme_id,
        Application.status.in_([ApplicationStatus.DRAFT, ApplicationStatus.SUBMITTED, ApplicationStatus.UNDER_REVIEW])
    ).first()
    
    if existing_application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have an active application for this scheme"
        )
    
    # Create new application
    new_application = Application(
        user_id=current_user.id,
        scheme_id=application_data.scheme_id,
        status=ApplicationStatus.DRAFT,
        application_data=application_data.application_data
    )
    
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    
    return ApplicationResponse.model_validate(new_application)


@router.get("/", response_model=List[ApplicationResponse])
async def get_user_applications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all applications for current user.
    """
    applications = db.query(Application).filter(
        Application.user_id == current_user.id
    ).all()
    
    return [ApplicationResponse.model_validate(app) for app in applications]


@router.get("/{application_id}", response_model=ApplicationStatusResponse)
async def get_application_status(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get application status with scheme details.
    """
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    scheme = db.query(Scheme).filter(Scheme.id == application.scheme_id).first()
    
    return ApplicationStatusResponse(
        application_id=application.id,
        scheme_name=scheme.scheme_name if scheme else "Unknown Scheme",
        status=application.status,
        eligibility_score=application.eligibility_score,
        rejection_reason=application.rejection_reason,
        submitted_at=application.submitted_at,
        last_updated=application.updated_at
    )


@router.post("/{application_id}/submit", response_model=ApplicationResponse)
async def submit_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit an application for review.
    """
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    if application.status != ApplicationStatus.DRAFT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only draft applications can be submitted"
        )
    
    # Use Submission Agent to submit
    result = submission_agent.execute_action(
        "submit_application",
        user_id=current_user.id,
        scheme_id=application.scheme_id,
        application_data=application.application_data or "{}"
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Failed to submit application")
        )
    
    # Update application status
    application.status = ApplicationStatus.SUBMITTED
    application.submitted_at = result["data"]["submitted_at"]
    
    db.commit()
    db.refresh(application)
    
    # Send notification
    notification_agent.send_application_status_notification(
        user_id=current_user.id,
        application_id=str(application_id),
        status="submitted"
    )
    
    return ApplicationResponse.model_validate(application)


@router.post("/{application_id}/generate-form")
async def generate_application_form(
    application_id: int,
    user_profile: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate application form for a scheme.
    """
    application = db.query(Application).filter(
        Application.id == application_id,
        Application.user_id == current_user.id
    ).first()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    # Use Submission Agent to generate form
    result = submission_agent.execute_action(
        "generate_form",
        scheme_id=application.scheme_id,
        user_profile=user_profile
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Failed to generate form")
        )
    
    return result["data"]
