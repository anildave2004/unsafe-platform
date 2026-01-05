"""
Actuary Agent - Risk Assessment and Financial Exposure
Calculates financial risk based on incident classification.
"""
from typing import Dict, Any
from core.llm import get_llm_client


class ActuaryAgent:
    """Risk agent that calculates financial exposure."""
    
    def __init__(self):
        """Initialize the Actuary agent with LLM client."""
        self.llm_client = get_llm_client()
        self.name = "Actuary"
        
        # Risk multipliers by severity
        self.severity_multipliers = {
            "CRITICAL": 5.0,
            "HIGH": 3.0,
            "MEDIUM": 1.5,
            "LOW": 0.5,
            "UNKNOWN": 1.0
        }
        
        # Base costs by metric type
        self.base_costs = {
            "temperature": 10000,
            "vibration": 8000,
            "pressure": 7000,
            "network": 2000,
            "power": 5000,
            "default": 5000
        }
    
    def assess_risk(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess financial risk for an incident.
        
        Args:
            incident_data: Incident data from Sentinel
            
        Returns:
            Risk assessment with financial exposure
        """
        severity = incident_data.get("severity", "UNKNOWN")
        metric_type = incident_data.get("metric_type", "default")
        classification = incident_data.get("classification", "")
        
        # Calculate base financial exposure
        base_cost = self.base_costs.get(metric_type, self.base_costs["default"])
        severity_multiplier = self.severity_multipliers.get(severity, 1.0)
        financial_exposure = base_cost * severity_multiplier
        
        # Calculate risk score (0.0 to 1.0)
        risk_score = self._calculate_risk_score(severity, financial_exposure)
        
        # Estimate mitigation cost
        mitigation_cost = financial_exposure * 0.3  # Assume mitigation costs 30% of exposure
        
        # Get LLM recommendation for additional context
        prompt = f"""Analyze the following incident and provide risk assessment insights:

Severity: {severity}
Metric Type: {metric_type}
Classification: {classification}
Estimated Financial Exposure: ${financial_exposure:,.2f}
Risk Score: {risk_score:.2f}

Provide a brief risk assessment and mitigation recommendations."""
        
        response = self.llm_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        risk_analysis = response.content[0].text
        
        return {
            "incident_id": incident_data.get("asset_id", "unknown"),
            "financial_exposure": financial_exposure,
            "risk_score": risk_score,
            "mitigation_cost": mitigation_cost,
            "risk_analysis": risk_analysis,
            "severity": severity,
            "agent": self.name,
            "recommendation": self._get_recommendation(risk_score)
        }
    
    def _calculate_risk_score(self, severity: str, financial_exposure: float) -> float:
        """Calculate normalized risk score.
        
        Args:
            severity: Incident severity level
            financial_exposure: Estimated financial exposure
            
        Returns:
            Risk score between 0.0 and 1.0
        """
        # Severity contribution (0.6 weight)
        severity_scores = {
            "CRITICAL": 1.0,
            "HIGH": 0.75,
            "MEDIUM": 0.5,
            "LOW": 0.25,
            "UNKNOWN": 0.5
        }
        severity_component = severity_scores.get(severity, 0.5) * 0.6
        
        # Financial exposure contribution (0.4 weight)
        # Normalize to 0-1 scale (assuming max exposure of $100k)
        financial_component = min(financial_exposure / 100000, 1.0) * 0.4
        
        return min(severity_component + financial_component, 1.0)
    
    def _get_recommendation(self, risk_score: float) -> str:
        """Get recommendation based on risk score.
        
        Args:
            risk_score: Calculated risk score
            
        Returns:
            Recommendation string
        """
        if risk_score >= 0.8:
            return "IMMEDIATE_ACTION_REQUIRED"
        elif risk_score >= 0.6:
            return "URGENT_ATTENTION_NEEDED"
        elif risk_score >= 0.4:
            return "SCHEDULE_MAINTENANCE"
        else:
            return "MONITOR_SITUATION"
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status information.
        
        Returns:
            Status dictionary
        """
        return {
            "agent": self.name,
            "status": "operational",
            "capabilities": ["risk_assessment", "financial_analysis"]
        }
