# Unsafe Platform - AI Workforce Architecture

An AI-powered incident management and risk assessment platform using hierarchical agent swarm architecture.

## Architecture Overview

The system is composed of a hierarchical agent swarm:

- **Supervisor**: Central orchestrator that manages the lifecycle of an incident.
- **Sentinel**: Triage agent that analyzes raw telemetry and classifies incidents.
- **Actuary**: Risk agent that calculates financial exposure based on Sentinel's classification.
- **Resolver**: Execution agent that takes action (mocked) based on risk thresholds.

## Project Structure

```
unsafe-platform/
├── api/
│   ├── __init__.py
│   └── main.py              # FastAPI entry point for telemetry ingestion
├── agents/
│   ├── __init__.py
│   ├── supervisor.py        # Central orchestrator
│   ├── sentinel.py          # Triage and classification agent
│   ├── actuary.py           # Risk assessment agent
│   └── resolver.py          # Action execution agent
├── core/
│   ├── __init__.py
│   └── llm.py               # Mock Anthropic LLM client
├── db/
│   ├── __init__.py
│   ├── schema.sql           # Database schema definitions
│   └── vector_store.py      # Mock vector store for context retrieval
├── requirements.txt
└── README.md
```

## Features

### 1. API (api/main.py)
FastAPI application that provides endpoints for:
- `/api/v1/telemetry` - Ingest device telemetry and trigger incident processing
- `/api/v1/incidents` - Retrieve incident history
- `/api/v1/status` - Get system and agent status
- `/api/v1/metrics` - Get system metrics and statistics
- `/health` - Health check endpoint

### 2. Database Schema (db/schema.sql)
SQL schema defining:
- **assets**: Device/asset information
- **incidents**: Detected incidents with classification
- **risk_assessments**: Financial exposure calculations
- **actions**: Actions taken by the system

### 3. Agent Swarm

#### Supervisor Agent (agents/supervisor.py)
Orchestrates the complete incident lifecycle:
1. Delegates telemetry analysis to Sentinel
2. Requests risk assessment from Actuary
3. Commands Resolver to execute actions
4. Tracks incident history and system metrics

#### Sentinel Agent (agents/sentinel.py)
Analyzes telemetry data and classifies incidents:
- Uses mock LLM for classification
- Retrieves historical context from vector store
- Classifies severity (CRITICAL, HIGH, MEDIUM, LOW)

#### Actuary Agent (agents/actuary.py)
Calculates financial risk:
- Computes financial exposure based on severity and metric type
- Calculates risk scores (0.0 - 1.0)
- Estimates mitigation costs
- Provides recommendations

#### Resolver Agent (agents/resolver.py)
Executes actions based on risk thresholds:
- Determines appropriate actions based on severity
- Mocks execution (alerts, shutdowns, dispatches, etc.)
- Tracks action history
- Auto-executes for high-risk incidents (risk_score >= 0.7)

### 4. Core Utilities

#### Mock LLM Client (core/llm.py)
Simulates Anthropic Claude API for testing:
- Context-aware mock responses
- Supports classification, risk assessment, and action determination
- No external API calls required

#### Mock Vector Store (db/vector_store.py)
Simulates vector database for context retrieval:
- Stores historical incident data
- Keyword-based similarity search
- Provides contextual information for analysis

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Running the API Server

```bash
cd api
python main.py
```

Or using uvicorn directly:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Testing the System

Test the agent architecture:
```bash
python test_architecture.py
```

Test the API endpoints:
```bash
python test_api.py
```

### Example API Request

Ingest telemetry data:

```bash
curl -X POST "http://localhost:8000/api/v1/telemetry" \
  -H "Content-Type: application/json" \
  -d '{
    "asset_id": "motor_001",
    "metric_type": "temperature",
    "value": 120.5,
    "threshold": 80.0,
    "timestamp": "2024-01-01T12:00:00Z",
    "metadata": {
      "location": "Building A",
      "device_type": "Industrial Motor"
    }
  }'
```

Response:
```json
{
  "status": "success",
  "message": "Telemetry processed successfully",
  "incident": {
    "incident_id": "...",
    "severity": "CRITICAL",
    "risk_score": 0.80,
    "financial_exposure": 50000.0,
    "actions_taken": 3
  }
}
```

## Incident Processing Flow

1. **Telemetry Ingestion**: Device sends telemetry data via API
2. **Triage (Sentinel)**: Analyzes data and classifies severity
3. **Risk Assessment (Actuary)**: Calculates financial exposure and risk score
4. **Action Execution (Resolver)**: Determines and executes appropriate actions
5. **Response**: Complete incident report returned to caller

## Risk Thresholds

- **Risk Score >= 0.8**: CRITICAL - Emergency shutdown and team dispatch
- **Risk Score >= 0.6**: HIGH - Alert maintenance, schedule urgent inspection
- **Risk Score >= 0.4**: MEDIUM - Create ticket, schedule maintenance
- **Risk Score < 0.4**: LOW - Log and monitor

## Development Notes

- All LLM calls are mocked for development/testing
- Vector store uses simple keyword matching
- Action execution is simulated (no actual system integration)
- Ready for integration with real Anthropic API and vector databases

## License

Apache License 2.0
