import json, os

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Specify WM SR key
resource = Resource(attributes={
    "service.name": os.getenv("SERVICE_NAME", "SOFTEAM")
})
provider = TracerProvider(resource = resource)

# To publish metrics of the operation after span finishes
console_exporter_processor = BatchSpanProcessor(
    ConsoleSpanExporter(
            formatter=lambda span: json.dumps(json.loads(span.to_json()), separators=(',', ':')) + '\n'
        )
    )
provider.add_span_processor(console_exporter_processor)

# To export metrics of the operation after span finishes
# otlp_exporter = BatchSpanProcessor(
#     OTLPSpanExporter(
#         endpoint= os.getenv("COLLECTOR_ENDPOINT", ""),
#         insecure=True
#     )
# )
# provider.add_span_processor(otlp_exporter)

trace.set_tracer_provider(provider)

# Used to start custom spans
tracer = trace.get_tracer(__name__)
