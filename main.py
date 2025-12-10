from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from services.dynamic_monitor import DynamicRouteMonitor
from routers import api_routes

from dotenv import load_dotenv
from observability import setup_observability

import asyncio
import logging
import time

# Load environment variables
load_dotenv()

app = FastAPI()

# Configure logging
logging.basicConfig(
    level=logging.INFO
)

# Setup observability and get meter for custom metrics
meter = setup_observability(app)

# Create custom metrics
#request_counter = meter.create_counter(
#    name="http_requests_total",
#    description="Total number of HTTP requests",
#    unit="1"
#)

#response_time_histogram = meter.create_histogram(
#    name="http_request_duration_seconds",
#    description="HTTP request duration in seconds",
#    unit="s"
#)

#@app.middleware("http")
#async def metrics_middleware(request, call_next):
#    """Middleware to collect custom metrics"""
#    start_time = time.time()
    
    # Process request
#    response = await call_next(request)
    
    # Calculate duration
#    duration = time.time() - start_time
    
    # Record metrics
#    request_counter.add(1, {
#        "method": request.method,
#        "endpoint": request.url.path,
#        "status_code": str(response.status_code)
#    })
    
#    response_time_histogram.record(duration, {
#        "method": request.method,
#        "endpoint": request.url.path,
#        "status_code": str(response.status_code)
#    })
    
#    return response


# Routes
app.include_router(api_routes.router)


# Monitor
monitor = DynamicRouteMonitor(app)


@app.on_event("startup")
async def startup():
    asyncio.create_task(monitor.run())    # Start monitor
    logging.info("Application started with observability via OpenTelemetry")


@app.get("/", include_in_schema=False, response_class=RedirectResponse)
def read_root():
    logging.info("Root endpoint accessed - redirecting to /docs")
    return "/docs"

@app.get("/health")
def health():
    logging.info("Health check accessed")
    return {"status": "ok"}

@app.get("/test-logs")
def test_logs():
    logging.info("Info log test")
    logging.warning("Warning log test")
    logging.error("Error log test")
    return {"message": "Logs sent to Grafana"}

@app.get("/test-metrics")
def test_metrics():
    """Endpoint to test custom metrics"""
    
    # Create a custom counter for this endpoint
    test_counter = meter.create_counter(
        name="test_endpoint_calls",
        description="Number of calls to test endpoint"
    )
    
    test_counter.add(1, {"endpoint": "test-metrics"})
    
    logging.info("Custom metrics test executed")
    return {"message": "Custom metrics sent to Grafana"}