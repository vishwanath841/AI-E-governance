from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.audit_log import AuditLogResponse, AgentActionLog
from app.models.audit_log import AuditLog
from app.models.user import User
from app.api.auth import get_current_user
from app.core.armoriq import armoriq
from datetime import datetime

router = APIRouter()


@router.get("/", response_model=List[AuditLogResponse])
async def get_audit_logs(
    skip: int = 0,
    limit: int = 100,
    agent_name: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get audit logs with optional filtering by agent.
    """
    query = db.query(AuditLog)
    
    if agent_name:
        query = query.filter(AuditLog.agent == agent_name)
    
    logs = query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
    
    return [AuditLogResponse.model_validate(log) for log in logs]


@router.get("/agent-actions", response_model=List[AgentActionLog])
async def get_agent_action_logs(
    current_user: User = Depends(get_current_user)
):
    """
    Get agent action logs from ArmorIQ.
    """
    # Get logs from ArmorIQ in-memory storage
    armoriq_logs = armoriq.get_audit_log()
    
    # Convert to AgentActionLog format
    action_logs = []
    for log in armoriq_logs:
        action_logs.append(AgentActionLog(
            agent_name=log["agent"],
            action=log["action"],
            allowed=log["result"] == "authorized",
            reason=log.get("details"),
            timestamp=datetime.fromisoformat(log["timestamp"])
        ))
    
    return action_logs


@router.get("/blocked")
async def get_blocked_actions(
    current_user: User = Depends(get_current_user)
):
    """
    Get all blocked actions from the security layer.
    """
    armoriq_logs = armoriq.get_audit_log()
    
    blocked_actions = [
        log for log in armoriq_logs 
        if log["result"] in ["unauthorized", "blocked"]
    ]
    
    return {
        "total_blocked": len(blocked_actions),
        "blocked_actions": blocked_actions
    }


@router.get("/summary")
async def get_audit_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get audit log summary statistics.
    """
    # Get database statistics
    total_logs = db.query(AuditLog).count()
    authorized_count = db.query(AuditLog).filter(AuditLog.result == "authorized").count()
    unauthorized_count = db.query(AuditLog).filter(AuditLog.result == "unauthorized").count()
    blocked_count = db.query(AuditLog).filter(AuditLog.result == "blocked").count()
    
    # Get ArmorIQ statistics
    armoriq_logs = armoriq.get_audit_log()
    armoriq_authorized = len([log for log in armoriq_logs if log["result"] == "authorized"])
    armoriq_blocked = len([log for log in armoriq_logs if log["result"] in ["unauthorized", "blocked"]])
    
    return {
        "database_stats": {
            "total_logs": total_logs,
            "authorized": authorized_count,
            "unauthorized": unauthorized_count,
            "blocked": blocked_count
        },
        "armoriq_stats": {
            "total_actions": len(armoriq_logs),
            "authorized": armoriq_authorized,
            "blocked": armoriq_blocked
        },
        "combined_total": total_logs + len(armoriq_logs)
    }


@router.get("/agent/{agent_name}")
async def get_agent_audit_logs(
    agent_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get audit logs for a specific agent.
    """
    # Get database logs
    db_logs = db.query(AuditLog).filter(
        AuditLog.agent == agent_name
    ).order_by(AuditLog.timestamp.desc()).all()
    
    # Get ArmorIQ logs
    armoriq_logs = [
        log for log in armoriq.get_audit_log()
        if log["agent"] == agent_name
    ]
    
    return {
        "agent_name": agent_name,
        "database_logs": [AuditLogResponse.model_validate(log) for log in db_logs],
        "armoriq_logs": armoriq_logs,
        "total_actions": len(db_logs) + len(armoriq_logs)
    }
