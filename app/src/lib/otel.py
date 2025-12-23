import os

from opentelemetry import metrics, trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource, ResourceDetector
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
# from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter


def setup_tracer() -> trace.Tracer:
  otel_otlp_endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", None)

  # Resource.create() implicitly calls ResourceDetector.detect()
  # and builds the Resource object from the OTEL_RESOURCE_ATTRIBUTES 
  # environment variable
  resource = Resource.create() 
  traceProvider = TracerProvider(resource=resource)
  exporter = OTLPSpanExporter(otel_otlp_endpoint)
  if otel_otlp_endpoint is None:
      exporter = ConsoleSpanExporter()

  processor = BatchSpanProcessor(exporter)
  traceProvider.add_span_processor(processor)

  # Sets the global default tracer provider
  trace.set_tracer_provider(traceProvider)

  reader = PeriodicExportingMetricReader(
      OTLPMetricExporter(endpoint=otel_otlp_endpoint)
  )

  meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
  metrics.set_meter_provider(meterProvider)

  # Creates a tracer from the global tracer provider
  return trace.get_tracer(__name__)
