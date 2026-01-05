#!/usr/bin/env python3
"""
Test script to verify the FastAPI application.
"""
import sys
import requests
import time
import subprocess
import signal
import os

def test_fastapi_app():
    """Test the FastAPI application endpoints."""
    print("="*80)
    print("Testing Unsafe Platform FastAPI Application")
    print("="*80)
    
    # Start the FastAPI server in the background
    print("\nStarting FastAPI server...")
    env = os.environ.copy()
    env['PYTHONPATH'] = '/home/runner/work/unsafe-platform/unsafe-platform'
    
    process = subprocess.Popen(
        ["python3", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd="/home/runner/work/unsafe-platform/unsafe-platform",
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    time.sleep(3)
    
    base_url = "http://localhost:8000"
    
    try:
        # Test 1: Root endpoint
        print("\n--- Test 1: Root Endpoint ---")
        response = requests.get(f"{base_url}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        assert response.status_code == 200
        
        # Test 2: Health check
        print("\n--- Test 2: Health Check ---")
        response = requests.get(f"{base_url}/health")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Status: {data['status']}")
        print(f"System Health: {data['system']['system_health']}")
        assert response.status_code == 200
        
        # Test 3: Telemetry ingestion - Critical incident
        print("\n--- Test 3: Telemetry Ingestion (Critical) ---")
        telemetry_data = {
            "asset_id": "motor_001",
            "metric_type": "temperature",
            "value": 120.5,
            "threshold": 80.0,
            "timestamp": "2024-01-01T12:00:00Z",
            "metadata": {
                "location": "Building A",
                "device_type": "Industrial Motor"
            }
        }
        response = requests.post(f"{base_url}/api/v1/telemetry", json=telemetry_data)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Status: {data['status']}")
        print(f"Incident ID: {data['incident']['incident_id']}")
        print(f"Severity: {data['incident']['triage']['severity']}")
        print(f"Risk Score: {data['incident']['risk_assessment']['risk_score']:.2f}")
        print(f"Financial Exposure: ${data['incident']['risk_assessment']['financial_exposure']:,.2f}")
        assert response.status_code == 200
        
        # Test 4: Get incidents
        print("\n--- Test 4: Get Incidents ---")
        response = requests.get(f"{base_url}/api/v1/incidents?limit=5")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Incidents Count: {data['count']}")
        assert response.status_code == 200
        
        # Test 5: Get status
        print("\n--- Test 5: Get Status ---")
        response = requests.get(f"{base_url}/api/v1/status")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Supervisor Status: {data['system_status']['supervisor']['status']}")
        print(f"Sentinel Status: {data['system_status']['agents']['sentinel']['status']}")
        assert response.status_code == 200
        
        # Test 6: Get metrics
        print("\n--- Test 6: Get Metrics ---")
        response = requests.get(f"{base_url}/api/v1/metrics")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Total Incidents: {data['metrics']['total_incidents']}")
        print(f"Total Financial Exposure: ${data['metrics']['total_financial_exposure']:,.2f}")
        assert response.status_code == 200
        
        print("\n" + "="*80)
        print("All API tests completed successfully!")
        print("="*80)
        return True
        
    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Terminate the server
        print("\nStopping FastAPI server...")
        process.terminate()
        process.wait(timeout=5)


if __name__ == "__main__":
    try:
        success = test_fastapi_app()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
