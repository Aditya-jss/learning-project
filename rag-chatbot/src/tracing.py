"""
Tracing Configuration for RAG Chatbot
"""
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.openai import OpenAIInstrumentor

logger = logging.getLogger(__name__)


class TracingManager:
    """Manage OpenTelemetry tracing"""
    
    def __init__(self, otlp_endpoint: str = "http://localhost:4318"):
        self.otlp_endpoint = otlp_endpoint
        self.tracer_provider = None
        self.is_initialized = False
    
    def setup_tracing(self) -> None:
        """Setup OpenTelemetry tracing"""
        if self.is_initialized:
            logger.info("Tracing already initialized")
            return
        
        try:
            # Create tracer provider
            self.tracer_provider = TracerProvider()
            trace.set_tracer_provider(self.tracer_provider)
            
            # Create OTLP exporter
            otlp_exporter = OTLPSpanExporter(
                endpoint=f"{self.otlp_endpoint}/v1/traces"
            )
            
            # Add span processor
            span_processor = BatchSpanProcessor(otlp_exporter)
            self.tracer_provider.add_span_processor(span_processor)
            
            # Instrument OpenAI
            OpenAIInstrumentor().instrument()
            
            self.is_initialized = True
            logger.info(f"Tracing initialized with endpoint: {self.otlp_endpoint}")
            
        except Exception as e:
            logger.error(f"Failed to initialize tracing: {e}")
            logger.info("Continuing without tracing...")
    
    def shutdown(self) -> None:
        """Shutdown tracing"""
        if self.tracer_provider:
            self.tracer_provider.shutdown()
            self.is_initialized = False
            logger.info("Tracing shutdown complete")
