import logging
import sys
from logging.handlers import RotatingFileHandler

# Define the format for the log messages
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Create a logger
logger = logging.getLogger("CodingTechniques")
logger.setLevel(logging.DEBUG)

# Create a console handler and set its level
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(log_format))

# Create a file handler and set its level
# This will rotate logs, keeping 5 files of 5MB each.
file_handler = RotatingFileHandler("coding_techniques.log", maxBytes=5*1024*1024, backupCount=5)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(log_format))

# Add the handlers to the logger, but only if they haven't been added before
if not logger.hasHandlers():
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

def get_logger(name=None):
    """
    Returns the main logger instance. This ensures all modules use the same
    logger and its configured handlers, preventing duplicate logs.
    """
    return logger 