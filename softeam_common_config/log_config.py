import logging
import json

from softeam_common_config.tracer_config import *
from opentelemetry.trace import get_current_span

logging.basicConfig(level=logging.WARNING)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        span = get_current_span()
        data = {
            'trace_id': format(span.get_span_context().trace_id, 'x') if span else None,
            'span_id': format(span.get_span_context().span_id, 'x') if span else None,
            'time': self.formatTime(record),
            'process': record.process,
            'file': record.filename,
            'line': record.lineno,
            'level': record.levelname,
            'message': record.getMessage(),
        }
        return json.dumps(data)

def get_logger(name):
    logger = logging.getLogger(name)
    logger.propagate = False
    
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    formatter = JsonFormatter()
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    # Create a file handler to log warnings and errors to a file
    file_handler = logging.FileHandler(f'Logs/WARN_ERR.log')
    file_handler.setLevel(logging.WARNING)  # Set to capture warnings and above

    # Create a formatter for the log messages
    formatter = logging.Formatter('%(asctime)s -  %(process)d - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger