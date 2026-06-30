from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent
from app.core.armoriq import armoriq


class CoordinatorAgent(BaseAgent):
    """
    Coordinator Agent - The main orchestrator of the multi-agent system.
    
    Responsibilities:
    - Receives citizen queries
    - Creates execution plans
    - Calls ArmorIQ capture_plan()
    - Delegates tasks to other agents
    - Coordinates the workflow
    """
    
    def __init__(self):
        super().__init__("coordinator_agent")
    
    def _perform_action(self, action: str, **kwargs) -> Any:
        """Perform coordinator-specific actions."""
        if action == "create_plan":
            return self._create_execution_plan(kwargs.get("user_request", ""))
        elif action == "delegate_task":
            return self._delegate_task(kwargs.get("agent_name"), kwargs.get("task"))
        elif action == "coordinate_agents":
            return self._coordinate_workflow(kwargs.get("user_request"))
        elif action == "query_user":
            return self._query_user(kwargs.get("query"))
        elif action == "get_status":
            return self._get_status(kwargs.get("plan_id"))
        else:
            raise ValueError(f"Unknown action: {action}")
    
    def _create_execution_plan(self, user_request: str) -> Dict[str, Any]:
        """
        Create an execution plan for the user request.
        
        Args:
            user_request: The citizen's query or request
            
        Returns:
            Dictionary containing the execution plan
        """
        # Capture the plan through ArmorIQ
        plan = armoriq.capture_plan(user_request)
        
        # Analyze the request and determine required steps
        steps = self._analyze_request(user_request)
        plan["steps"] = steps
        
        return plan
    
    def _analyze_request(self, user_request: str) -> List[Dict[str, str]]:
        """
        Analyze the user request to determine required steps.
        
        Args:
            user_request: The citizen's query
            
        Returns:
            List of steps in the execution plan
        """
        request_lower = user_request.lower()
        steps = []
        
        # Determine which agents need to be involved based on the request
        if "verify" in request_lower or "check" in request_lower:
            steps.append({
                "agent": "verification_agent",
                "action": "verify_aadhaar",
                "description": "Verify citizen identity"
            })
        
        if "document" in request_lower or "upload" in request_lower:
            steps.append({
                "agent": "document_agent",
                "action": "upload_document",
                "description": "Process document upload"
            })
        
        if "scheme" in request_lower or "eligible" in request_lower or "benefit" in request_lower:
            steps.append({
                "agent": "eligibility_agent",
                "action": "analyze_profile",
                "description": "Check scheme eligibility"
            })
        
        if "apply" in request_lower or "submit" in request_lower:
            steps.extend([
                {
                    "agent": "submission_agent",
                    "action": "generate_form",
                    "description": "Generate application form"
                },
                {
                    "agent": "submission_agent",
                    "action": "submit_application",
                    "description": "Submit application"
                }
            ])
        
        # Always add notification for status updates
        steps.append({
            "agent": "notification_agent",
            "action": "send_notification",
            "description": "Send status notification"
        })
        
        return steps
    
    def _delegate_task(self, agent_name: str, task: Dict[str, Any]) -> bool:
        """
        Delegate a task to a specific agent.
        
        Args:
            agent_name: Name of the agent to delegate to
            task: Task details including required actions
            
        Returns:
            True if delegation successful, False otherwise
        """
        allowed_actions = task.get("allowed_actions", [])
        return armoriq.delegate(agent_name, allowed_actions)
    
    def _coordinate_workflow(self, user_request: str) -> Dict[str, Any]:
        """
        Coordinate the complete workflow for a user request.
        
        Args:
            user_request: The citizen's query
            
        Returns:
            Dictionary containing workflow status and results
        """
        # Create execution plan
        plan = self._create_execution_plan(user_request)
        
        # Execute each step in the plan
        results = []
        for step in plan["steps"]:
            agent_name = step["agent"]
            action = step["action"]
            
            # Delegate and execute through ArmorIQ
            if armoriq.delegate(agent_name, [action]):
                result = armoriq.invoke(agent_name, action)
                results.append({
                    "step": step,
                    "result": result
                })
        
        return {
            "plan_id": plan["id"],
            "status": "completed",
            "results": results
        }
    
    def _query_user(self, query: str) -> Dict[str, Any]:
        """
        Process a user query and provide intelligent response.
        
        Args:
            query: The user's question
            
        Returns:
            Dictionary containing the response
        """
        # This would typically use an LLM to generate intelligent responses
        # For MVP, we'll return a structured response
        return {
            "query": query,
            "response": "I understand your query. Let me help you with that.",
            "suggested_actions": self._analyze_request(query)
        }
    
    def _get_status(self, plan_id: str) -> Dict[str, Any]:
        """
        Get the status of an execution plan.
        
        Args:
            plan_id: The plan identifier
            
        Returns:
            Dictionary containing plan status
        """
        # In a real implementation, this would query a database
        return {
            "plan_id": plan_id,
            "status": "completed",
            "timestamp": "2024-01-01T00:00:00"
        }
