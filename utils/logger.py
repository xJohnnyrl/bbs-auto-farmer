import logging
import os
from datetime import datetime
from utils.resource_manager import get_logs_directory

# Create a timestamped log filename
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
LOG_DIR = get_logs_directory()
log_path = os.path.join(LOG_DIR, f"debug_{timestamp}.log")

# Initialize logging
logging.basicConfig(
    filename=log_path,
    filemode='a',
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def debug(msg):
    logging.debug(msg)

def error(msg):
    logging.error(msg)

def warning(msg):
    logging.warning(msg)