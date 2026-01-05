#!/usr/bin/env python3
"""
Demonstration script for the Unsafe Platform AI Workforce.
Shows the complete agent swarm in action with realistic scenarios.
"""
import sys
sys.path.insert(0, '/home/runner/work/unsafe-platform/unsafe-platform')

from agents.supervisor import SupervisorAgent
import json


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80 + "\n")


def print_incident_summary(result):
    """Print a formatted incident summary."""
    print(f"Incident ID: {result['incident_id']}")
    print(f"Status: {result['status']}")
    print(f"Processing Time: {result['processing_time_seconds']:.3f}s")
    
    print(f"\n📊 TRIAGE (by {result['triage']['agent']})")
    print(f"  Severity: {result['triage']['severity']}")
    print(f"  Classification: {result['triage']['classification'][:100]}...")
    
    print(f"\n💰 RISK ASSESSMENT (by {result['risk_assessment']['agent']})")
    print(f"  Risk Score: {result['risk_assessment']['risk_score']:.2f}/1.0")
    print(f"  Financial Exposure: ${result['risk_assessment']['financial_exposure']:,.2f}")
    print(f"  Mitigation Cost: ${result['risk_assessment']['mitigation_cost']:,.2f}")
    print(f"  Recommendation: {result['risk_assessment']['recommendation']}")
    
    print(f"\n⚡ ACTIONS (by {result['execution']['agent']})")
    print(f"  Auto-executed: {result['execution']['auto_executed']}")
    print(f"  Actions Taken: {result['execution']['actions_taken']}")
    for i, action in enumerate(result['execution']['actions'], 1):
        print(f"    {i}. {action['action_type']}: {action['result'][:60]}...")


def main():
    print_section("🤖 UNSAFE PLATFORM - AI WORKFORCE DEMONSTRATION")
    
    # Initialize the Supervisor
    print("Initializing Supervisor agent...")
    supervisor = SupervisorAgent()
    print("✓ Supervisor initialized")
    print("✓ Sentinel agent ready")
    print("✓ Actuary agent ready")
    print("✓ Resolver agent ready")
    
    # Scenario 1: Critical Equipment Failure
    print_section("SCENARIO 1: Critical Equipment Overheating")
    
    telemetry_critical = {
        "asset_id": "turbine_generator_01",
        "metric_type": "temperature",
        "value": 145.8,
        "threshold": 85.0,
        "timestamp": "2024-01-05T10:30:00Z",
        "metadata": {
            "location": "Power Plant - Building A",
            "device_type": "Industrial Turbine Generator",
            "capacity": "50MW",
            "criticality": "high"
        }
    }
    
    print("⚠️  ALERT: Temperature reading 145.8°C (threshold: 85.0°C)")
    print("📡 Telemetry received from turbine_generator_01")
    print("\nProcessing incident through agent swarm...")
    
    result1 = supervisor.process_incident(telemetry_critical)
    print_incident_summary(result1)
    
    # Scenario 2: Mechanical Vibration Issue
    print_section("SCENARIO 2: Abnormal Vibration in Hydraulic Pump")
    
    telemetry_vibration = {
        "asset_id": "hydraulic_pump_07",
        "metric_type": "vibration",
        "value": 52.3,
        "threshold": 30.0,
        "timestamp": "2024-01-05T10:45:00Z",
        "metadata": {
            "location": "Manufacturing Floor - Section B",
            "device_type": "High-Pressure Hydraulic Pump",
            "age_years": 8,
            "last_maintenance": "2023-12-15"
        }
    }
    
    print("⚠️  ALERT: Vibration level 52.3 Hz (threshold: 30.0 Hz)")
    print("📡 Telemetry received from hydraulic_pump_07")
    print("\nProcessing incident through agent swarm...")
    
    result2 = supervisor.process_incident(telemetry_vibration)
    print_incident_summary(result2)
    
    # Scenario 3: Network Connectivity Issue
    print_section("SCENARIO 3: Network Gateway Latency")
    
    telemetry_network = {
        "asset_id": "network_gateway_15",
        "metric_type": "network",
        "value": 18.5,
        "threshold": 10.0,
        "timestamp": "2024-01-05T11:00:00Z",
        "metadata": {
            "location": "Data Center - Rack 12",
            "device_type": "Industrial IoT Gateway",
            "connected_devices": 45,
            "latency_ms": 185
        }
    }
    
    print("⚠️  ALERT: Network latency 18.5ms (threshold: 10.0ms)")
    print("📡 Telemetry received from network_gateway_15")
    print("\nProcessing incident through agent swarm...")
    
    result3 = supervisor.process_incident(telemetry_network)
    print_incident_summary(result3)
    
    # System Summary
    print_section("📈 SYSTEM SUMMARY")
    
    metrics = supervisor.get_metrics()
    status = supervisor.get_system_status()
    
    print("System Metrics:")
    print(f"  Total Incidents Processed: {metrics['total_incidents']}")
    print(f"  Average Processing Time: {metrics['average_processing_time_seconds']:.3f}s")
    print(f"  Total Financial Exposure: ${metrics['total_financial_exposure']:,.2f}")
    print(f"\nSeverity Distribution:")
    for severity, count in metrics['severity_distribution'].items():
        print(f"  {severity}: {count}")
    
    print(f"\nAgent Status:")
    for agent_name, agent_status in status['agents'].items():
        print(f"  {agent_name.capitalize()}: {agent_status['status']}")
    
    print(f"\nSystem Health: {status['system_health'].upper()}")
    
    print_section("✅ DEMONSTRATION COMPLETE")
    print("The Unsafe Platform AI workforce successfully processed 3 incidents,")
    print("demonstrating coordinated agent behavior across triage, risk assessment,")
    print("and automated action execution.")
    print("\nTo start the API server: python api/main.py")
    print("To run tests: python test_architecture.py")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemonstration interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
