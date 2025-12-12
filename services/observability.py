import os
import logging
import socket
from urllib.parse import urlparse
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


def check_otlp_connection(endpoint: str, timeout: int = 2) -> bool:
    """
    Verifica se o servidor OTLP está acessível

    Args:
        endpoint: URL do endpoint OTLP (ex: http://grafana:4317)
        timeout: Tempo limite para conexão em segundos

    Returns:
        True se conectou com sucesso, False caso contrário
    """
    try:
        # Parse do endpoint para extrair host e porta
        parsed = urlparse(endpoint)
        host = parsed.hostname or parsed.path.split(':')[0]

        # Extrai porta ou usa padrão 4317 (gRPC)
        if parsed.port:
            port = parsed.port
        elif ':' in parsed.path:
            port = int(parsed.path.split(':')[1])
        else:
            port = 4317

        # Tenta conectar ao servidor
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()

        return result == 0
    except Exception as e:
        logging.warning(f"Erro ao verificar conexão OTLP: {e}")
        return False


# Variável global para armazenar o status da observabilidade
_observability_enabled = False


def is_observability_enabled() -> bool:
    """Retorna True se a observabilidade está habilitada e conectada ao servidor OTLP"""
    return _observability_enabled


def setup_observability(app):
    """Basic observability setup with traces, logs and metrics"""
    global _observability_enabled

    # Configure service name
    service_name = os.getenv("SERVICE_NAME", "DynamicAPI")

    # Create resource with service name
    resource = Resource.create({"service.name": service_name})

    # Configure OTLP endpoint
    otlp_endpoint = os.getenv("OTLP_ENDPOINT", "http://grafana:4317")

    # Verifica se o servidor OTLP está disponível
    otlp_available = check_otlp_connection(otlp_endpoint)

    if not otlp_available:
        _observability_enabled = False
        logging.warning(f"⚠️  Servidor OTLP não disponível em {otlp_endpoint}")
        logging.warning("⚠️  Observabilidade desabilitada - logs não serão enviados")

        # Configura providers básicos sem exporters
        trace.set_tracer_provider(TracerProvider(resource=resource))
        metrics.set_meter_provider(MeterProvider(resource=resource))

        # Configura logging apenas local
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)

        # Instrument FastAPI mesmo sem OTLP
        FastAPIInstrumentor.instrument_app(app)

        logging.info(f"✅ Aplicação iniciada SEM observabilidade remota - Service: {service_name}")
        return metrics.get_meter(__name__)

    # Se OTLP está disponível, configura normalmente
    _observability_enabled = True
    logging.info(f"✅ Servidor OTLP disponível em {otlp_endpoint}")

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

    logging.info(f"✅ Observabilidade configurada - Service: {service_name} | Endpoint: {otlp_endpoint}")

    return metrics.get_meter(__name__)

