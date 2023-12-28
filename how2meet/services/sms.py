"""
Twilio SMS service. Boilerplate and API calls to arbitrarily send SMS messages.
"""

import os

from twilio.rest import Client

# Your Twilio account SID and auth token
account_sid = os.getenv("TWILIO_TEST_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_TEST_AUTH_TOKEN")

# Create a Twilio client
client = Client(account_sid, auth_token)

twilio_number = "+18552824345"
my_number = "+12165541740"

# Send a message
message = client.messages.create(body="Hello from Twilio!", from_=twilio_number, to=my_number)

# Print the message sid
print(message.sid)
