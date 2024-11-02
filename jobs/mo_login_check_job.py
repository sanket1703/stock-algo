from brokers.motilal.login import client_login
from database.dao.client_dao import get_client_list
from notification.email.send_email import send_email
from loguru import logger
import time

def notification_failed(client,message):
    sender = "Keyursanket.com"
    recipient = "sanketyou8@gmail.com"
    cc = "keyurmarolia2@gmail.com"
    subject = f"[{client}] Login Failed for client {client}"
    message = f"message"
    send_email(sender,recipient,cc,subject,message,None)

def notification_success():
    sender = "Keyursanket.com"
    recipient = "sanketyou8@gmail.com"
    cc = "keyurmarolia2@gmail.com"
    subject = f"MO Login Success for All Clients."
    message = "All Clients logged in successfully."
    send_email(sender,recipient,cc,subject,message,None)

def check_login_job():
    clients = get_client_list()
    failures = 0
    for client in clients:
        Mofl = client_login(client)
        login_response = Mofl.GetPosition(client)
        time.sleep(5)
        logger.info(login_response)
        if(login_response['status']!='SUCCESS'):
            logger.info(f"[{client}] Login Failed for client {client}")
            failures+=1
            notification_failed(client,login_response)
    
    if(failures==0):
        notification_success()
    
        
        

        