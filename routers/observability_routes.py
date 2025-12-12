from fastapi import APIRouter
from services.observability import is_observability_enabled
import logging

router = APIRouter(prefix="/observability", tags=["Observability"])


@router.get("/test-logs")
def test_logs():
    """
    Endpoint to test log generation and verify if logs are being sent to Grafana.
    
    Returns different messages based on observability status:
    - If enabled: Logs are sent to Grafana
    - If disabled: Logs are generated locally only
    """
    logging.info("Info log test")
    logging.warning("Warning log test")
    logging.error("Error log test")
    
    if is_observability_enabled():
        return {
            "status": "success",
            "message": "Logs sent to Grafana",
            "observability": "enabled"
        }
    else:
        return {
            "status": "warning",
            "message": "Logs generated locally only (Grafana not available)",
            "observability": "disabled"
        }


@router.get("/test-metrics")
def test_metrics():
    """
    Endpoint to test custom metrics generation and verify if metrics are being sent to Grafana.
    
    Creates a custom counter metric and returns different messages based on observability status:
    - If enabled: Metrics are sent to Grafana
    - If disabled: Metrics are generated locally only
    """
    # Import meter from main to avoid circular imports
    from main import meter
    
    # Create a custom counter for this endpoint
    test_counter = meter.create_counter(
        name="test_endpoint_calls",
        description="Number of calls to test endpoint"
    )
    
    test_counter.add(1, {"endpoint": "test-metrics"})
    
    logging.info("Custom metrics test executed")
    
    if is_observability_enabled():
        return {
            "status": "success",
            "message": "Custom metrics sent to Grafana",
            "observability": "enabled"
        }
    else:
        return {
            "status": "warning",
            "message": "Metrics generated locally only (Grafana not available)",
            "observability": "disabled"
        }


@router.get("/status")
def observability_status():
    """
    Returns the current status of the observability system.
    
    Useful for health checks and monitoring the connection to Grafana/OTLP endpoint.
    """
    enabled = is_observability_enabled()
    
    return {
        "observability_enabled": enabled,
        "status": "connected" if enabled else "disconnected",
        "message": "Observability is active and sending data to Grafana" if enabled 
                   else "Observability is disabled - OTLP endpoint not available"
    }

