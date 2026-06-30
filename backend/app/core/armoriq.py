from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
import json


class ActionResult(str, Enum):
    """Possible action results."""
    AUTHORIZED = "authorized"
    UNAUTHORIZED = "unauthorized"
    BLOCKED = "blocked"


class ArmorIQ:
    """
    ArmorIQ Security Layer - Multi-Agent Security Middleware
    
    This class provides security control for multi-agent systems by:
    - Capturing and validating execution plans
    - Delegating actions with permission checks
    - Invoking agents with security verification
    - Logging all actions for audit purposes
    """
    
    def __init__(self):
        # Define agent permissions
        self.agent_permissions: Dict[str, List[str]] = {
            "coordinator_agent": [
                "create_plan",
                "delegate_task",
                "coordinate_agents",
                "query_user",
                "get_status"
            ],
            "verification_agent": [
                "verify_aadhaar",
                "verify_mobile",
                "validate_identity",
                "check_user_exists"
            ],
            "document_agent": [
                "upload_document",
                "extract_text",
                "verify_document",
                "delete_document",
                "get_document"
            ],
            "eligibility_agent": [
                "analyze_profile",
                "match_schemes",
                "calculate_score",
                "get_eligibility"
            ],
            "submission_agent": [
                "generate_form",
                "submit_application",
                "update_status",
                "get_application"
            ],
            "notification_agent": [
                "send_notification",
                "get_status",
                "read_user_data"
            ]
        }
        
        # In-memory audit log (in production, use database)
        self.audit_log: List[Dict[str, Any]] = []
        
        # Execution plan storage
        self.current_plan: Optional[Dict[str, Any]] = None
    
    def capture_plan(self, user_request: str) -> Dict[str, Any]:
        """
        Capture and validate the execution plan for a user request.
        
        Args:
            user_request: The user's request/query
            
        Returns:
            Dictionary containing the plan details
        """
        plan = {
            "id": f"plan_{datetime.utcnow().timestamp()}",
            "user_request": user_request,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "captured",
            "steps": []
        }
        
        self.current_plan = plan
        
        # Log the plan capture
        self._log_action(
            agent="armor_iq",
            action="capture_plan",
            result=ActionResult.AUTHORIZED,
            details=f"Plan captured for request: {user_request}"
        )
        
        return plan
    
    def delegate(self, agent_name: str, allowed_actions: List[str]) -> bool:
        """
        Delegate tasks to an agent with specified allowed actions.
        
        Args:
            agent_name: Name of the agent to delegate to
            allowed_actions: List of actions this agent is allowed to perform
            
        Returns:
            True if delegation is successful, False otherwise
        """
        if agent_name not in self.agent_permissions:
            self._log_action(
                agent="armor_iq",
                action="delegate",
                result=ActionResult.UNAUTHORIZED,
                details=f"Unknown agent: {agent_name}"
            )
            return False
        
        # Check if requested actions are within agent's permissions
        agent_perms = self.agent_permissions[agent_name]
        for action in allowed_actions:
            if action not in agent_perms:
                self._log_action(
                    agent="armor_iq",
                    action="delegate",
                    result=ActionResult.UNAUTHORIZED,
                    details=f"Action '{action}' not allowed for {agent_name}"
                )
                return False
        
        self._log_action(
            agent="armor_iq",
            action="delegate",
            result=ActionResult.AUTHORIZED,
            details=f"Delegated to {agent_name} with actions: {allowed_actions}"
        )
        
        return True
    
    def invoke(self, agent_name: str, action: str, **kwargs) -> Dict[str, Any]:
        """
        Invoke an agent to perform an action with security verification.
        
        Args:
            agent_name: Name of the agent to invoke
            action: Action to perform
            **kwargs: Additional parameters for the action
            
        Returns:
            Dictionary containing the result of the action
        """
        # Check if agent exists
        if agent_name not in self.agent_permissions:
            result = {
                "success": False,
                "error": f"Unknown agent: {agent_name}",
                "result": ActionResult.UNAUTHORIZED
            }
            
            self._log_action(
                agent=agent_name,
                action=action,
                result=ActionResult.UNAUTHORIZED,
                details=f"Unknown agent attempted action: {action}"
            )
            
            return result
        
        # Check if action is permitted for this agent
        agent_perms = self.agent_permissions[agent_name]
        if action not in agent_perms:
            result = {
                "success": False,
                "error": f"Action '{action}' not permitted for {agent_name}",
                "result": ActionResult.BLOCKED
            }
            
            self._log_action(
                agent=agent_name,
                action=action,
                result=ActionResult.BLOCKED,
                details=f"Blocked unauthorized action: {action}"
            )
            
            return result
        
        # Action is authorized - log it
        self._log_action(
            agent=agent_name,
            action=action,
            result=ActionResult.AUTHORIZED,
            details=f"Authorized action executed: {action}"
        )
        
        return {
            "success": True,
            "result": ActionResult.AUTHORIZED,
            "message": f"Action '{action}' authorized for {agent_name}"
        }
    
    def _log_action(self, agent: str, action: str, result: ActionResult, details: str):
        """
        Log an action to the audit log.
        
        Args:
            agent: Name of the agent performing the action
            action: Action being performed
            result: Result of the action (authorized/unauthorized/blocked)
            details: Additional details about the action
        """
        log_entry = {
            "id": f"log_{datetime.utcnow().timestamp()}",
            "timestamp": datetime.utcnow().isoformat(),
            "agent": agent,
            "action": action,
            "result": result.value,
            "details": details
        }
        
        self.audit_log.append(log_entry)
    
    def get_audit_log(self) -> List[Dict[str, Any]]:
        """
        Retrieve the complete audit log.
        
        Returns:
            List of all audit log entries
        """
        return self.audit_log
    
    def get_agent_permissions(self, agent_name: Optional[str] = None) -> Dict[str, List[str]]:
        """
        Get permissions for agents.
        
        Args:
            agent_name: Optional specific agent name. If None, returns all permissions.
            
        Returns:
            Dictionary of agent permissions
        """
        if agent_name:
            return {agent_name: self.agent_permissions.get(agent_name, [])}
        return self.agent_permissions
    
    def check_action_permission(self, agent_name: str, action: str) -> bool:
        """
        Check if an agent has permission to perform an action.
        
        Args:
            agent_name: Name of the agent
            action: Action to check
            
        Returns:
            True if action is permitted, False otherwise
        """
        if agent_name not in self.agent_permissions:
            return False
        
        return action in self.agent_permissions[agent_name]


# Global ArmorIQ instance
armoriq = ArmorIQ()
