"""
GMail service. Boilerplate to arbitrarily send email messages. Uses app password from app.how2meet@gmail.com account

Note: Named "email_service" to avoid conflict with the built-in email module
"""
import smtplib
from email.message import EmailMessage
import os

app_email = "app.how2meet@gmail.com"
app_password = os.getenv("H2M_EMAIL_APP_PASSWORD")


def send_email(to_email: str, subject: str, body: str):
    """
    Send an email message.

    Args:
        to_email: The email address to send the message to.
        subject: The subject of the email message.
        body: The body of the email message.

    Returns:
        None
    """
    # Setting up the email
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = "app.how2meet@gmail.com"
    message["To"] = to_email
    message.set_content(body)

    # Login and send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(app_email, app_password)
        server.send_message(message)
        server.close()
    except Exception as e:
        print(e)
