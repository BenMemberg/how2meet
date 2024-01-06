"""Test Twilio SMS service"""

import time

from twilio.rest.api.v2010.account.message import MessageInstance

from how2meet.services.sms import send_sms


def test_send_sms():
    # Provide the necessary test data
    to_number = "+12165541740"
    body = "Test message from test_sms.py"

    # Call the function under test
    result = send_sms(to_number, body)

    acceptable_statuses = [
        MessageInstance.Status.SENT,
        MessageInstance.Status.DELIVERED,
        MessageInstance.Status.RECEIVED,
        MessageInstance.Status.READ,
        MessageInstance.Status.QUEUED,
    ]

    time.sleep(5)  # Wait for message to process and send via API

    # Assert the expected behavior
    assert result.status in acceptable_statuses
    assert result.body == body
    assert result.to == to_number
