"""
Twilio SMS service. Boilerplate and API calls to arbitrarily send SMS messages.
"""

import os

from twilio.rest import Client

# Your Twilio TEST account SID and auth token
test_account_sid = os.getenv("TWILIO_TEST_ACCOUNT_SID")
test_auth_token = os.getenv("TWILIO_TEST_AUTH_TOKEN")

# Your Twilio LIVE account SID and auth token
account_sid = os.getenv("TWILIO_LIVE_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_LIVE_AUTH_TOKEN")

# Your Twilio H2M account SID and auth token
how2meet_sid = os.getenv("TWILIO_H2M_SID")
how2meet_token = os.getenv("TWILIO_H2M_AUTH_TOKEN")

print(f"test: {test_account_sid} | {test_auth_token}")
print(f"live: {account_sid} | {auth_token}")
print(f"h2m: {how2meet_sid} | {how2meet_token}")

# Create a Twilio client
client = Client(account_sid, auth_token)

twilio_number = "+12163409585"
my_number = "+12165541740"

# Send a message
message = client.messages.create(
    body="Hello from Twilio!",
    from_=twilio_number,
    to=my_number,
    messaging_service_sid="MG4e7b8359547821f5859d9c1b1f4814e7",
)  # Send from campaign

# Print the message sid
print(message.sid)
