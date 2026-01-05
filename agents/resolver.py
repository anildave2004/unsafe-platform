"""
Resolver Agent - Action Execution
Takes action based on risk thresholds and incident severity.
"""
from typing import Dict, Any, List
import uuid
from datetime import datetime


class ResolverAgent:
    """Execution agent that takes action based on risk assessment."""
    
    def __init__(self):
        """Initialize the Resolver agent."""
        self.name = "Resolver"
        self.action_history = []
        
        # Risk threshold for automatic action (0.0 to 1.0)
        self.auto_action_threshold = 0.7
    
    def determine_actions(self, risk_assessment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Determine appropriate actions based on risk assessment.
        
        Args:
            risk_assessment: Risk assessment from Actuary
            
        Returns:
            List of action dictionaries
        """
        risk_score = risk_assessment.get("risk_score", 0.0)
        severity = risk_assessment.get("severity", "UNKNOWN")
        recommendation = risk_assessment.get("recommendation", "MONITOR_SITUATION")
        
        actions = []
        
        # Determine actions based on severity and risk score
        if severity == "CRITICAL" or risk_score >= 0.8:
            actions.extend([
                self._create_action("ALERT_EMERGENCY_TEAM", "Immediate notification to emergency response team"),
                self._create_action("SHUTDOWN_SYSTEM", "Initiate emergency shutdown procedure"),
                self._create_action("DISPATCH_TECHNICIAN", "Dispatch on-site technician for immediate inspection")
            ])
        elif severity == "HIGH" or risk_score >= 0.6:
            actions.extend([
                self._create_action("ALERT_MAINTENANCE", "Notify maintenance team of high-priority issue"),
                self._create_action("SCHEDULE_INSPECTION", "Schedule urgent inspection within 4 hours"),
                self._create_action("ENABLE_BACKUP", "Activate backup systems if available")
            ])
        elif severity == "MEDIUM" or risk_score >= 0.4:
            actions.extend([
                self._create_action("CREATE_TICKET", "Create maintenance ticket for review"),
                self._create_action("SCHEDULE_MAINTENANCE", "Schedule preventive maintenance"),
                self._create_action("INCREASE_MONITORING", "Increase monitoring frequency")
            ])
        else:
            actions.extend([
                self._create_action("LOG_INCIDENT", "Log incident for historical analysis"),
                self._create_action("CONTINUE_MONITORING", "Continue standard monitoring")
            ])
        
        return actions
    
    def execute_actions(
        self,
        actions: List[Dict[str, Any]],
        incident_id: str,
        risk_assessment: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute the determined actions (mocked).
        
        Args:
            actions: List of actions to execute
            incident_id: Incident identifier
            risk_assessment: Risk assessment data
            
        Returns:
            Execution results
        """
        risk_score = risk_assessment.get("risk_score", 0.0)
        executed_actions = []
        
        for action in actions:
            # Mock execution - in production, this would trigger actual systems
            action_result = self._mock_execute_action(action, incident_id)
            executed_actions.append(action_result)
            
            # Store in action history
            self.action_history.append({
                "incident_id": incident_id,
                "action": action,
                "result": action_result,
                "timestamp": datetime.utcnow().isoformat()
            })
        
        # Determine if auto-execution was performed
        auto_executed = risk_score >= self.auto_action_threshold
        
        return {
            "incident_id": incident_id,
            "risk_score": risk_score,
            "auto_executed": auto_executed,
            "actions_taken": len(executed_actions),
            "actions": executed_actions,
            "agent": self.name,
            "execution_timestamp": datetime.utcnow().isoformat()
        }
    
    def _create_action(self, action_type: str, description: str) -> Dict[str, Any]:
        """Create an action dictionary.
        
        Args:
            action_type: Type of action
            description: Action description
            
        Returns:
            Action dictionary
        """
        return {
            "action_id": str(uuid.uuid4()),
            "action_type": action_type,
            "description": description,
            "status": "pending"
        }
    
    def _mock_execute_action(self, action: Dict[str, Any], incident_id: str) -> Dict[str, Any]:
        """Mock execution of an action.
        
        Args:
            action: Action to execute
            incident_id: Associated incident ID
            
        Returns:
            Execution result
        """
        action_type = action.get("action_type", "UNKNOWN")
        
        # Simulate execution with mocked results
        mock_results = {
            "ALERT_EMERGENCY_TEAM": "Emergency team alerted successfully via SMS and email",
            "SHUTDOWN_SYSTEM": "System shutdown initiated - estimated 5 minutes to complete",
            "DISPATCH_TECHNICIAN": "Technician dispatched - ETA 30 minutes",
            "ALERT_MAINTENANCE": "Maintenance team notified - ticket created",
            "SCHEDULE_INSPECTION": "Inspection scheduled for next available slot",
            "ENABLE_BACKUP": "Backup systems activated successfully",
            "CREATE_TICKET": "Maintenance ticket #MT-12345 created",
            "SCHEDULE_MAINTENANCE": "Preventive maintenance scheduled for next week",
            "INCREASE_MONITORING": "Monitoring frequency increased to every 5 minutes",
            "LOG_INCIDENT": "Incident logged to database",
            "CONTINUE_MONITORING": "Standard monitoring continues"
        }
        
        result_message = mock_results.get(action_type, "Action executed successfully")
        
        return {
            "action_id": action.get("action_id"),
            "action_type": action_type,
            "incident_id": incident_id,
            "status": "completed",
            "result": result_message,
            "executed_at": datetime.utcnow().isoformat()
        }
    
    def get_action_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent action history.
        
        Args:
            limit: Maximum number of actions to return
            
        Returns:
            List of recent actions
        """
        return self.action_history[-limit:]
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status information.
        
        Returns:
            Status dictionary
        """
        return {
            "agent": self.name,
            "status": "operational",
            "capabilities": ["action_determination", "action_execution"],
            "auto_action_threshold": self.auto_action_threshold,
            "total_actions_executed": len(self.action_history)
        }
