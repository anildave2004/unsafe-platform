"""
Supervisor Agent - Central Orchestrator
Manages the lifecycle of incidents by coordinating Sentinel, Actuary, and Resolver.
"""
from typing import Dict, Any
import uuid
from datetime import datetime
from agents.sentinel import SentinelAgent
from agents.actuary import ActuaryAgent
from agents.resolver import ResolverAgent


class SupervisorAgent:
    """Central orchestrator that manages the incident lifecycle."""
    
    def __init__(self):
        """Initialize the Supervisor with all sub-agents."""
        self.name = "Supervisor"
        self.sentinel = SentinelAgent()
        self.actuary = ActuaryAgent()
        self.resolver = ResolverAgent()
        self.incident_log = []
    
    def process_incident(self, telemetry: Dict[str, Any]) -> Dict[str, Any]:
        """Process a complete incident lifecycle.
        
        This method orchestrates the full workflow:
        1. Sentinel analyzes and classifies the incident
        2. Actuary assesses risk and financial exposure
        3. Resolver determines and executes actions
        
        Args:
            telemetry: Raw telemetry data from device
            
        Returns:
            Complete incident processing result
        """
        incident_id = str(uuid.uuid4())
        start_time = datetime.utcnow()
        
        print(f"\n[{self.name}] Starting incident processing: {incident_id}")
        
        # Step 1: Triage with Sentinel
        print(f"[{self.name}] Delegating to Sentinel for triage...")
        sentinel_result = self.sentinel.analyze_telemetry(telemetry)
        print(f"[{self.name}] Sentinel classified as: {sentinel_result.get('severity')}")
        
        # Step 2: Risk assessment with Actuary
        print(f"[{self.name}] Delegating to Actuary for risk assessment...")
        risk_assessment = self.actuary.assess_risk(sentinel_result)
        print(f"[{self.name}] Actuary calculated risk score: {risk_assessment.get('risk_score'):.2f}")
        print(f"[{self.name}] Financial exposure: ${risk_assessment.get('financial_exposure'):,.2f}")
        
        # Step 3: Action determination and execution with Resolver
        print(f"[{self.name}] Delegating to Resolver for action execution...")
        actions = self.resolver.determine_actions(risk_assessment)
        execution_result = self.resolver.execute_actions(
            actions=actions,
            incident_id=incident_id,
            risk_assessment=risk_assessment
        )
        print(f"[{self.name}] Resolver executed {execution_result.get('actions_taken')} actions")
        
        # Compile complete incident report
        end_time = datetime.utcnow()
        processing_time = (end_time - start_time).total_seconds()
        
        incident_report = {
            "incident_id": incident_id,
            "status": "processed",
            "processing_time_seconds": processing_time,
            "timestamp": start_time.isoformat(),
            "completed_at": end_time.isoformat(),
            "telemetry": telemetry,
            "triage": {
                "agent": sentinel_result.get("agent"),
                "severity": sentinel_result.get("severity"),
                "classification": sentinel_result.get("classification")
            },
            "risk_assessment": {
                "agent": risk_assessment.get("agent"),
                "risk_score": risk_assessment.get("risk_score"),
                "financial_exposure": risk_assessment.get("financial_exposure"),
                "mitigation_cost": risk_assessment.get("mitigation_cost"),
                "recommendation": risk_assessment.get("recommendation")
            },
            "execution": {
                "agent": execution_result.get("agent"),
                "auto_executed": execution_result.get("auto_executed"),
                "actions_taken": execution_result.get("actions_taken"),
                "actions": execution_result.get("actions")
            },
            "orchestrator": self.name
        }
        
        # Log incident
        self.incident_log.append(incident_report)
        
        print(f"[{self.name}] Incident processing complete: {incident_id}")
        
        return incident_report
    
    def get_incident_history(self, limit: int = 10) -> list:
        """Get recent incident history.
        
        Args:
            limit: Maximum number of incidents to return
            
        Returns:
            List of recent incidents
        """
        return self.incident_log[-limit:]
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status.
        
        Returns:
            Status of all agents and the system
        """
        return {
            "supervisor": {
                "agent": self.name,
                "status": "operational",
                "incidents_processed": len(self.incident_log)
            },
            "agents": {
                "sentinel": self.sentinel.get_status(),
                "actuary": self.actuary.get_status(),
                "resolver": self.resolver.get_status()
            },
            "system_health": "operational"
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get system metrics and statistics.
        
        Returns:
            System metrics dictionary
        """
        if not self.incident_log:
            return {
                "total_incidents": 0,
                "average_processing_time": 0,
                "severity_distribution": {},
                "total_financial_exposure": 0
            }
        
        # Calculate metrics
        total_incidents = len(self.incident_log)
        avg_processing_time = sum(
            inc.get("processing_time_seconds", 0)
            for inc in self.incident_log
        ) / total_incidents
        
        # Severity distribution
        severity_counts = {}
        for incident in self.incident_log:
            severity = incident.get("triage", {}).get("severity", "UNKNOWN")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Total financial exposure
        total_exposure = sum(
            inc.get("risk_assessment", {}).get("financial_exposure", 0)
            for inc in self.incident_log
        )
        
        return {
            "total_incidents": total_incidents,
            "average_processing_time_seconds": round(avg_processing_time, 2),
            "severity_distribution": severity_counts,
            "total_financial_exposure": round(total_exposure, 2),
            "agents_active": 3
        }
