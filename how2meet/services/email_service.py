"""
GMail service. Boilerplate to arbitrarily send email messages. Uses app password from app.how2meet@gmail.com account

Note: Named "email_service" to avoid conflict with the built-in email module
"""
import smtplib
from email.message import EmailMessage
import os

app_email = "app.how2meet@gmail.com"
app_password = os.getenv("H2M_EMAIL_APP_PASSWORD")
from_email = "events@how2meet.com"


def send_email(to_email: str, subject: str, body: str) -> EmailMessage:
    """
    Send an email message.

    Args:
        to_email: The email address to send the message to.
        subject: The subject of the email message.
        body: The body of the email message.

    Returns:
        EmailMessage: The instance of the sent email.
    """
    # Setting up the email
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = from_email
    message["To"] = to_email
    message.set_content(body)

    # Login and send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(app_email, app_password)
    server.send_message(message)
    server.close()

    return message
