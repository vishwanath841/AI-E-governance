from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from app.core.armoriq import armoriq


class BaseAgent(ABC):
    """Base class for all agents in the system."""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
    
    def execute_action(self, action: str, **kwargs) -> Dict[str, Any]:
        """
        Execute an action through ArmorIQ security layer.
        
        Args:
            action: The action to perform
            **kwargs: Additional parameters for the action
            
        Returns:
            Dictionary containing the action result
        """
        # First, check permission through ArmorIQ
        security_result = armoriq.invoke(self.agent_name, action, **kwargs)
        
        if not security_result["success"]:
            return {
                "success": False,
                "error": security_result["error"],
                "result": security_result["result"]
            }
        
        # If authorized, execute the actual action
        try:
            result = self._perform_action(action, **kwargs)
            return {
                "success": True,
                "data": result,
                "result": security_result["result"]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "result": "error"
            }
    
    @abstractmethod
    def _perform_action(self, action: str, **kwargs) -> Any:
        """
        Perform the actual action. Must be implemented by subclasses.
        
        Args:
            action: The action to perform
            **kwargs: Additional parameters
            
        Returns:
            The result of the action
        """
        pass
    
    def get_permissions(self) -> list:
        """Get the list of permissions for this agent."""
        return armoriq.get_agent_permissions(self.agent_name).get(self.agent_name, [])
