"""
FastAPI entry point for Unsafe Platform.
Handles device telemetry ingestion and incident processing.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import uvicorn
from agents.supervisor import SupervisorAgent

# Initialize FastAPI app
app = FastAPI(
    title="Unsafe Platform API",
    description="AI-powered incident management and risk assessment platform",
    version="1.0.0"
)

# Initialize Supervisor agent
supervisor = SupervisorAgent()


class TelemetryRequest(BaseModel):
    """Request model for telemetry data."""
    asset_id: str = Field(..., description="Unique identifier for the asset")
    metric_type: str = Field(..., description="Type of metric (e.g., temperature, vibration)")
    value: float = Field(..., description="Current metric value")
    threshold: Optional[float] = Field(None, description="Normal threshold for the metric")
    timestamp: Optional[str] = Field(None, description="Timestamp of the reading")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "asset_id": "asset_001",
                "metric_type": "temperature",
                "value": 95.5,
                "threshold": 80.0,
                "timestamp": "2024-01-01T12:00:00Z",
                "metadata": {
                    "location": "Building A",
                    "device_type": "Industrial Motor"
                }
            }
        }


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "service": "Unsafe Platform API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "telemetry": "/api/v1/telemetry",
            "incidents": "/api/v1/incidents",
            "status": "/api/v1/status",
            "metrics": "/api/v1/metrics"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    system_status = supervisor.get_system_status()
    return {
        "status": "healthy",
        "system": system_status
    }


@app.post("/api/v1/telemetry")
async def ingest_telemetry(telemetry: TelemetryRequest):
    """
    Ingest device telemetry and process incident.
    
    This endpoint triggers the full incident processing workflow:
    1. Sentinel analyzes and classifies the incident
    2. Actuary assesses risk and financial exposure
    3. Resolver determines and executes actions
    """
    try:
        # Convert Pydantic model to dict
        telemetry_data = telemetry.model_dump()
        
        # Process incident through supervisor
        incident_report = supervisor.process_incident(telemetry_data)
        
        return {
            "status": "success",
            "message": "Telemetry processed successfully",
            "incident": incident_report
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing telemetry: {str(e)}"
        )


@app.get("/api/v1/incidents")
async def get_incidents(limit: int = 10):
    """
    Get recent incident history.
    
    Args:
        limit: Maximum number of incidents to return (default: 10)
    """
    try:
        incidents = supervisor.get_incident_history(limit=limit)
        return {
            "status": "success",
            "count": len(incidents),
            "incidents": incidents
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving incidents: {str(e)}"
        )


@app.get("/api/v1/status")
async def get_status():
    """
    Get system status for all agents.
    """
    try:
        status = supervisor.get_system_status()
        return {
            "status": "success",
            "system_status": status
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving status: {str(e)}"
        )


@app.get("/api/v1/metrics")
async def get_metrics():
    """
    Get system metrics and statistics.
    """
    try:
        metrics = supervisor.get_metrics()
        return {
            "status": "success",
            "metrics": metrics
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving metrics: {str(e)}"
        )


if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
