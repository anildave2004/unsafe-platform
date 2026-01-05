"""
Sentinel Agent - Triage and Classification
Analyzes raw telemetry and classifies incidents by severity.
"""
from typing import Dict, Any
from core.llm import get_llm_client
from db.vector_store import get_vector_store


class SentinelAgent:
    """Triage agent that analyzes and classifies incidents."""
    
    def __init__(self):
        """Initialize the Sentinel agent with LLM and vector store."""
        self.llm_client = get_llm_client()
        self.vector_store = get_vector_store()
        self.name = "Sentinel"
    
    def analyze_telemetry(self, telemetry: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze raw telemetry data and classify the incident.
        
        Args:
            telemetry: Raw telemetry data from device
            
        Returns:
            Classification result with severity and details
        """
        # Extract relevant information from telemetry
        asset_id = telemetry.get("asset_id", "unknown")
        metric_type = telemetry.get("metric_type", "unknown")
        value = telemetry.get("value", 0)
        threshold = telemetry.get("threshold", 100)
        
        # Get historical context from vector store
        context = self.vector_store.get_context(
            incident_type=metric_type,
            severity="unknown"
        )
        
        # Prepare prompt for LLM
        prompt = f"""Analyze the following device telemetry and classify the incident severity:

Asset ID: {asset_id}
Metric Type: {metric_type}
Current Value: {value}
Normal Threshold: {threshold}

Historical Context:
{context}

Please classify this incident and provide a severity level (CRITICAL, HIGH, MEDIUM, or LOW) with a brief explanation."""
        
        # Call LLM for classification
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
        
        # Parse LLM response
        classification_text = response.content[0].text
        severity = self._extract_severity(classification_text)
        
        return {
            "asset_id": asset_id,
            "metric_type": metric_type,
            "severity": severity,
            "classification": classification_text,
            "raw_telemetry": telemetry,
            "agent": self.name
        }
    
    def _extract_severity(self, classification_text: str) -> str:
        """Extract severity level from classification text.
        
        Args:
            classification_text: Full classification response
            
        Returns:
            Severity level (CRITICAL, HIGH, MEDIUM, or LOW)
        """
        text_upper = classification_text.upper()
        
        if "CRITICAL" in text_upper:
            return "CRITICAL"
        elif "HIGH" in text_upper:
            return "HIGH"
        elif "MEDIUM" in text_upper:
            return "MEDIUM"
        elif "LOW" in text_upper:
            return "LOW"
        else:
            return "UNKNOWN"
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status information.
        
        Returns:
            Status dictionary
        """
        return {
            "agent": self.name,
            "status": "operational",
            "capabilities": ["telemetry_analysis", "incident_classification"]
        }
