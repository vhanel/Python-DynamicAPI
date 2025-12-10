import os
import logging
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry._logs import set_logger_provider


def setup_observability(app):
    """Basic observability setup with traces, logs and metrics"""
    
    # Configure service name
    service_name = os.getenv("SERVICE_NAME", "DynamicAPIp")
    
    # Create resource with service name
    resource = Resource.create({"service.name": service_name})
    
    # Configure OTLP endpoint
    otlp_endpoint = os.getenv("OTLP_ENDPOINT", "http://grafana:4317")
    
    # Setup tracer
    trace.set_tracer_provider(TracerProvider(resource=resource))
    trace_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
    trace_processor = BatchSpanProcessor(trace_exporter)
    trace.get_tracer_provider().add_span_processor(trace_processor)
    
    # Setup metrics
    metric_exporter = OTLPMetricExporter(endpoint=otlp_endpoint, insecure=True)
    metric_reader = PeriodicExportingMetricReader(
        exporter=metric_exporter,
        export_interval_millis=5000  # Export every 5 seconds
    )
    metrics.set_meter_provider(MeterProvider(resource=resource, metric_readers=[metric_reader]))
    
    # Setup logs
    log_exporter = OTLPLogExporter(endpoint=otlp_endpoint, insecure=True)
    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)
    log_processor = BatchLogRecordProcessor(log_exporter)
    logger_provider.add_log_record_processor(log_processor)
    
    # Configure logging handler
    otlp_handler = LoggingHandler(level=logging.INFO, logger_provider=logger_provider)
    root_logger = logging.getLogger()
    root_logger.addHandler(otlp_handler)
    root_logger.setLevel(logging.INFO)
    
    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)
    
    logging.info(f"Observability configured - Service: {service_name} | Endpoint: {otlp_endpoint}")
    
    return metrics.get_meter(__name__)