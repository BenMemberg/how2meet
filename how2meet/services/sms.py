"""
Twilio SMS service. Boilerplate to arbitrarily send SMS messages.
"""

import os

from twilio.rest import Client
from twilio.rest.api.v2010.account.message import MessageInstance

# Your Twilio TEST account SID and auth token
test_account_sid = os.getenv("TWILIO_TEST_ACCOUNT_SID")
test_auth_token = os.getenv("TWILIO_TEST_AUTH_TOKEN")

# Your Twilio LIVE account SID and auth token
account_sid = os.getenv("TWILIO_LIVE_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_LIVE_AUTH_TOKEN")

# Your Twilio H2M account SID and auth token
how2meet_sid = os.getenv("TWILIO_H2M_SID")
how2meet_token = os.getenv("TWILIO_H2M_AUTH_TOKEN")

msg_service_sid = os.getenv("TWILIO_MSG_SERVICE_SID")
twilio_number = "+12163409585"
my_number = "+12165541740"

# Create a Twilio client
client = Client(account_sid, auth_token)


def send_sms(to_number: str, body: str) -> MessageInstance:
    """
    Send an SMS message.

    Args:
        to_number: The number to send the message to in string format, with country code.The phone number to send the SMS to.
        body: The body of the SMS message.

    Returns:
        MessageInstance: The instance of the sent message.
    """
    message_instance = client.messages.create(
        body=body,
        from_=twilio_number,
        to=to_number,
        messaging_service_sid=msg_service_sid,
    )

    return message_instance
