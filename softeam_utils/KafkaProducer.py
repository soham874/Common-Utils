from confluent_kafka import Producer
from softeam_common_config.log_config import get_logger
import traceback

from datetime import datetime

from opentelemetry.propagate import inject

producer = Producer({'bootstrap.servers': 'kafka:9093'})
log = get_logger(__name__)

def __delivery_report(err, msg):
    if err is not None:
        log.error(f"Message delivery failed: {err}")
    else:
        log.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def publish_message(
    topic,
    payload,
    key = None,
    headers = None
):
    try:

        headers = list(headers.items()) if headers else []

        carrier = {} 
        inject(carrier)
        
        for k, v in carrier.items():
            headers.append((k, v.encode('utf-8')))
        headers.append(('published-ts',datetime.now().isoformat()))

        producer.produce(
            topic, 
            key = key,
            value = payload,
            headers = headers, 
            callback = __delivery_report)
        producer.flush()  # Ensure the message is sent
    except:
        traceback.print_exc()