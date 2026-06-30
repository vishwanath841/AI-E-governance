from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.scheme import SchemeResponse, EligibilityResult
from app.models.scheme import Scheme
from app.models.user import User
from app.api.auth import get_current_user
from app.agents.eligibility_agent import EligibilityAgent

router = APIRouter()
eligibility_agent = EligibilityAgent()


@router.get("/", response_model=List[SchemeResponse])
async def get_schemes(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all available schemes.
    """
    schemes = db.query(Scheme).filter(
        Scheme.is_active == 1
    ).offset(skip).limit(limit).all()
    
    return [SchemeResponse.model_validate(scheme) for scheme in schemes]


@router.get("/{scheme_id}", response_model=SchemeResponse)
async def get_scheme(
    scheme_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific scheme by ID.
    """
    scheme = db.query(Scheme).filter(
        Scheme.id == scheme_id,
        Scheme.is_active == 1
    ).first()
    
    if not scheme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheme not found"
        )
    
    return SchemeResponse.model_validate(scheme)


@router.post("/check-eligibility", response_model=List[EligibilityResult])
async def check_eligibility(
    user_profile: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Check eligibility for schemes based on user profile.
    """
    # Add user_id to profile
    user_profile["user_id"] = current_user.id
    
    # Use Eligibility Agent to match schemes
    result = eligibility_agent.execute_action(
        "match_schemes",
        user_profile=user_profile
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Failed to check eligibility")
        )
    
    matched_schemes = result["data"]["matched_schemes"]
    
    # Convert to EligibilityResult format
    eligibility_results = []
    for match in matched_schemes:
        scheme = match["scheme"]
        eligibility = match["eligibility"]
        
        eligibility_results.append(EligibilityResult(
            scheme_id=scheme["id"],
            scheme_name=scheme["scheme_name"],
            is_eligible=eligibility["is_eligible"],
            eligibility_score=eligibility["score"],
            missing_documents=eligibility["missing_documents"],
            reasons=eligibility["reasons"]
        ))
    
    return eligibility_results


@router.get("/{scheme_id}/eligibility", response_model=EligibilityResult)
async def get_scheme_eligibility(
    scheme_id: int,
    user_profile: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Check eligibility for a specific scheme.
    """
    # Get scheme from database
    scheme = db.query(Scheme).filter(
        Scheme.id == scheme_id,
        Scheme.is_active == 1
    ).first()
    
    if not scheme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheme not found"
        )
    
    # Add user_id to profile
    user_profile["user_id"] = current_user.id
    
    # Use Eligibility Agent to calculate score
    result = eligibility_agent.execute_action(
        "calculate_score",
        user_profile=user_profile,
        scheme={
            "id": scheme.id,
            "scheme_name": scheme.scheme_name,
            "eligibility_rules": scheme.eligibility_rules,
            "required_documents": scheme.required_documents
        }
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result.get("error", "Failed to calculate eligibility")
        )
    
    eligibility_data = result["data"]
    
    return EligibilityResult(
        scheme_id=scheme_id,
        scheme_name=scheme.scheme_name,
        is_eligible=eligibility_data["is_eligible"],
        eligibility_score=eligibility_data["score"],
        missing_documents=eligibility_data["missing_documents"],
        reasons=eligibility_data["reasons"]
    )
