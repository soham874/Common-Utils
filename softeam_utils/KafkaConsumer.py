from flask_apscheduler import APScheduler

from softeam_common_config.log_config import get_logger
from softeam_common_config.tracer_config import *

from confluent_kafka import Consumer, KafkaError
import os

log = get_logger(__name__)

scheduler = APScheduler()
conf = {
    'bootstrap.servers': 'kafka:9093',
    'auto.offset.reset': 'earliest'
}

class KafkaConsumer():
    
    def __init__(self, app, group_id, topic_name):
        global scheduler
        self.app = app
        conf['group.id'] = group_id

        if not scheduler.running:
            scheduler.init_app(self.app)
            scheduler.start()

        self.consumer = Consumer(conf)
        self.consumer.subscribe([topic_name])

        log.info(f"Consumer subscribed in topic {topic_name} from group {group_id}")

        self.topic_name = topic_name

        self.func = None

    def _schedule_task(self):
        log.debug(f"Intitating Kafka consumer for topic {self.topic_name} under group-id {conf['group.id']}, to be passed through {self.func.__name__}")
        #self.func("Hello 1")
        @scheduler.task(
                'interval', 
                id=f'{self.func.__name__}_consumer_{os.getpid()}', 
                seconds=1, 
                max_instances=8,
                misfire_grace_time = 5
        )
        def execute_consumer_function():
            new_message = self.__consume_messages()
            if new_message:
                with tracer.start_as_current_span(f'{self.func.__name__}_consumer_{os.getpid()}') as span:
                    log.debug(f"Sending {new_message} to {self.func.__name__}")
                    self.func(new_message)
            else:
                log.debug("Nothing found yet")

    def __call__(self, func):
        self.func = func
        self._schedule_task()
        return func

    def __consume_messages(self):
        msg = self.consumer.poll(timeout=1.0)
        if msg:
            if msg.error() and msg.error().code() != KafkaError._PARTITION_EOF:
                log.error(f"Kafka error: {msg.error()}")
            else:
                log.debug(f"Received message: {msg.value().decode('utf-8')}")
                return {
                    "key" : msg.key().decode('utf-8') if msg.key() else None,
                    "headers" : dict(msg.headers()) if msg.headers() else None,
                    "payload" : msg.value().decode('utf-8')
                }
        else:
            log.debug(f"No message to poll from {self.topic_name}")
            return None