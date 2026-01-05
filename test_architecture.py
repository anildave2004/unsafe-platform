#!/usr/bin/env python3
"""
Test script to verify the Unsafe Platform implementation.
"""
import sys
sys.path.insert(0, '/home/runner/work/unsafe-platform/unsafe-platform')

from agents.supervisor import SupervisorAgent


def test_agent_architecture():
    """Test the agent architecture with sample telemetry."""
    print("="*80)
    print("Testing Unsafe Platform AI Workforce Architecture")
    print("="*80)
    
    # Initialize supervisor
    supervisor = SupervisorAgent()
    
    # Test 1: Critical temperature incident
    print("\n\n--- Test 1: Critical Temperature Incident ---")
    telemetry1 = {
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
    
    result1 = supervisor.process_incident(telemetry1)
    print(f"\nIncident ID: {result1['incident_id']}")
    print(f"Severity: {result1['triage']['severity']}")
    print(f"Risk Score: {result1['risk_assessment']['risk_score']:.2f}")
    print(f"Financial Exposure: ${result1['risk_assessment']['financial_exposure']:,.2f}")
    print(f"Actions Taken: {result1['execution']['actions_taken']}")
    print(f"Auto-executed: {result1['execution']['auto_executed']}")
    
    # Test 2: Medium vibration incident
    print("\n\n--- Test 2: Medium Vibration Incident ---")
    telemetry2 = {
        "asset_id": "pump_005",
        "metric_type": "vibration",
        "value": 45.0,
        "threshold": 30.0,
        "timestamp": "2024-01-01T12:05:00Z",
        "metadata": {
            "location": "Building B",
            "device_type": "Hydraulic Pump"
        }
    }
    
    result2 = supervisor.process_incident(telemetry2)
    print(f"\nIncident ID: {result2['incident_id']}")
    print(f"Severity: {result2['triage']['severity']}")
    print(f"Risk Score: {result2['risk_assessment']['risk_score']:.2f}")
    print(f"Financial Exposure: ${result2['risk_assessment']['financial_exposure']:,.2f}")
    print(f"Actions Taken: {result2['execution']['actions_taken']}")
    
    # Test 3: Low network incident
    print("\n\n--- Test 3: Low Network Incident ---")
    telemetry3 = {
        "asset_id": "gateway_003",
        "metric_type": "network",
        "value": 15.0,
        "threshold": 10.0,
        "timestamp": "2024-01-01T12:10:00Z",
        "metadata": {
            "location": "Building C",
            "device_type": "Network Gateway"
        }
    }
    
    result3 = supervisor.process_incident(telemetry3)
    print(f"\nIncident ID: {result3['incident_id']}")
    print(f"Severity: {result3['triage']['severity']}")
    print(f"Risk Score: {result3['risk_assessment']['risk_score']:.2f}")
    print(f"Financial Exposure: ${result3['risk_assessment']['financial_exposure']:,.2f}")
    print(f"Actions Taken: {result3['execution']['actions_taken']}")
    
    # Test system status
    print("\n\n--- System Status ---")
    status = supervisor.get_system_status()
    print(f"Supervisor Status: {status['supervisor']['status']}")
    print(f"Incidents Processed: {status['supervisor']['incidents_processed']}")
    print(f"Sentinel Status: {status['agents']['sentinel']['status']}")
    print(f"Actuary Status: {status['agents']['actuary']['status']}")
    print(f"Resolver Status: {status['agents']['resolver']['status']}")
    
    # Test metrics
    print("\n\n--- System Metrics ---")
    metrics = supervisor.get_metrics()
    print(f"Total Incidents: {metrics['total_incidents']}")
    print(f"Average Processing Time: {metrics['average_processing_time_seconds']:.2f}s")
    print(f"Total Financial Exposure: ${metrics['total_financial_exposure']:,.2f}")
    print(f"Severity Distribution: {metrics['severity_distribution']}")
    
    print("\n" + "="*80)
    print("All tests completed successfully!")
    print("="*80)
    return True


if __name__ == "__main__":
    try:
        success = test_agent_architecture()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
