from loguru import logger
from datetime import datetime
import sys

def configure_log(level="DEBUG"):
    today = datetime.now().strftime("%Y-%m-%d")


    log_filename = f"algo_logs/algo_run_{today}.log"
    logger.remove()
    logger.add(log_filename, level="INFO")
    logger.add(sys.stdout, level=level)