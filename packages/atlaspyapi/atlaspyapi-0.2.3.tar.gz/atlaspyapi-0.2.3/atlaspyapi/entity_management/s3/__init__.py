# Set default logging handler to avoid "No handler found" warnings.
import logging

logging.getLogger("atlaspyapi").addHandler(logging.NullHandler())
