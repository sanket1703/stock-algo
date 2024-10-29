from loguru import logger
from datetime import datetime
import sys
from notification.email.send_email import send_email

def email_log_handler(message):
    """Custom handler for sending log messages via email."""
    log_record = message.record
    level = log_record["level"].name
    
    if level in ["ERROR", "CRITICAL"]:
        subject = f"Log Alert: {level} - {log_record['message']}"
        body = f"Time: {log_record['time']}\nLevel: {log_record['level']}\nMessage: {log_record['message']}\n"
        sender = "Keyursanket.com"
        recipient = "sanketyou8@gmail.com"
        cc = "keyurmarolia2@gmail.com"
        today = datetime.now().strftime("%Y-%m-%d")
        log_filename = f"algo_logs/algo_run_{today}.log"
        send_email(sender,recipient,cc,subject, body,log_filename)
    
    # To avoid propagation to other handlers, return False
    return True

def configure_log(level="DEBUG"):
    today = datetime.now().strftime("%Y-%m-%d")
    log_filename = f"algo_logs/algo_run_{today}.log"
    logger.remove()
    logger.add(log_filename, level="INFO")
    logger.add(sys.stdout, level=level)
    logger.add(email_log_handler, level="ERROR")