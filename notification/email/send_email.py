from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
from loguru import logger
import mimetypes
import os
from google.oauth2.credentials import *
from notification.email.credentials.gmail_auth import authenticate_gmail

def create_message(sender, to,cc, subject, message_text,file_path):
    """Create a message for an email."""
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    message['cc'] = cc
    # Attach the main email text content
    msg = MIMEText(message_text)
    message.attach(msg)
    
    if file_path:
        content_type, encoding = mimetypes.guess_type(file_path)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)

        with open(file_path, 'rb') as file:
            file_attachment = MIMEBase(main_type, sub_type)
            file_attachment.set_payload(file.read())
            encoders.encode_base64(file_attachment)
            file_attachment.add_header(
                'Content-Disposition', 
                'attachment', 
                filename=os.path.basename(file_path)
            )
            message.attach(file_attachment)
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw}

def send_email(sender, to,cc, subject, message_text,file_path):
    
    service = authenticate_gmail()
    """Send an email using the Gmail API."""
    message = create_message(sender, to,cc, subject, message_text,file_path)
    try:
        message = service.users().messages().send(userId="me", body=message).execute()
        logger.debug(f"Email sent. Email Message Id: {message['id']}")
    except Exception as error:
        logger.info(f"An error occurred: {error}")

if __name__ == '__main__':
        # Email details
    sender = "Keyursanket.com"
    recipient = "sanketyou8@gmail.com"
    subject = "Test Subject"
    body = "This is a test email sent via Gmail API."

    # Send the email
    send_email(sender, recipient, subject, body)
