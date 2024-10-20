import smtplib

my_email = "Keyursanket@yahoo.com"
password = "Kajalmiss@123"
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email():
    # Your Yahoo email credentials
    sender_email = "Keyursanket@yahoo.com"
    sender_password = "your_app_password"  # Use the app password here
    receiver_email = "recipient@example.com"

    # Set up the email content
    subject = "Test Email from Yahoo"
    body = "This is a test email sent from Python using Yahoo SMTP."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the Yahoo SMTP server
        with smtplib.SMTP('smtp.mail.yahoo.com', 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

# Call the function to send the email
send_email()
