"""
Utility functions
"""
import json
import os
from typing import Any

from httpx import AsyncClient, Response
from nicegui import ui

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")  # To be passed around as needed


class APIClient:
    """Client class for encapsulating HTTP requests to API"""

    def __init__(self, base_url: str = BASE_URL) -> None:
        self.base_url = base_url

    @classmethod
    async def get_events(cls) -> dict | list[dict]:
        """
        Get list of all events from API
        TODO: Limit the number of events returned
        TODO: query params?
        """
        # NOTE: This is a blocking call, so we use an async client
        async with AsyncClient() as client:
            events = await client.get(f"{BASE_URL}/api/events/", timeout=10)
        try:
            events = events.json()
        except:
            events = []
        return events

    @classmethod
    async def get_event(cls, event_id: str) -> dict:
        """Get single event from API"""
        # NOTE: This is a blocking call, so we use an async client
        async with AsyncClient() as client:
            event = await client.get(f"{BASE_URL}/api/events/{event_id}", timeout=10)
        if event.is_success:
            event = event.json()
        else:
            event = {}

        return event

    @classmethod
    async def delete_event(cls, event_id: str, card: ui.card | None = None) -> Response:
        """
        Delete single event from API. Optionally, the UI element (card) may be provided (if calling from events page) so that
        it can be deleted visually upon clicking delete. This prevents needing to reload the page to show updates to the user

        Args:
            event_id: The ID of the event to delete
            card: The card to delete

        Returns:
            int: The status code of the response
        """
        async with AsyncClient() as client:
            response = await client.delete(f"{BASE_URL}/api/events/{event_id}", timeout=10)
            response.raise_for_status()

        if card is not None:
            card.delete()
            ui.notification("Event deleted", timeout=1.5)

        return response

    @classmethod
    async def create_event(cls, event_json_str: str | dict) -> Response:
        """
        Create single event using the API using POST HTTP request.

        Args:
            event_json_str: JSON-formatted string of the event to create

        Returns:
            int: The status code of the response
        """
        try:
            event_json_str = event_json_str.json()
        except:
            if isinstance(event_json_str, dict):
                event_json_str = json.dumps(event_json_str)

        async with AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/api/events/", data=event_json_str, timeout=10)
            response.raise_for_status()

        return response

    @classmethod
    async def update_event(cls, event_id: str, event_json_str: dict[str, Any]) -> Response:
        """
        Updates an event by sending a PUT request to the API with the given event ID and JSON data.

        Args:
            event_id: The ID of the event to be updated.
            event_json_str: The JSON data representing the updated event.

        Returns:
            int: The status code of the response from the API.
        """
        try:
            event_json_str = event_json_str.json()
        except:
            if isinstance(event_json_str, dict):
                event_json_str = json.dumps(event_json_str)

        async with AsyncClient() as client:
            response = await client.put(f"{BASE_URL}/api/events/{event_id}", data=event_json_str, timeout=10)
            response.raise_for_status()

        return response

    @classmethod
    async def get_guests_from_event(cls, event_id: str) -> list:
        """
        Get list of all guests from single event
        """

        async with AsyncClient() as client:
            guests = await client.get(f"{BASE_URL}/api/events/{event_id}/guests", timeout=10)
        try:
            guests = guests.json()
        except:
            guests = []
        return guests

    @classmethod
    async def create_guest(cls, event_id: str, guest_json_str: str) -> Response:
        """
        Create single guest using the API using POST HTTP request.
        Args:
            event_id: Event to add guest to
            guest_json_str: JSON-formatted string of the guest data

        Returns: HTTP status code

        """
        try:
            guest_json_str = guest_json_str.json()
        except:
            if isinstance(guest_json_str, dict):
                guest_json_str = json.dumps(guest_json_str)

        async with AsyncClient() as client:
            response = await client.post(f"{BASE_URL}/api/events/{event_id}/guests", data=guest_json_str, timeout=10)
            response.raise_for_status()

        return response

    @classmethod
    async def update_guest(cls, event_id: str, guest_id: str, guest_json_str: str) -> Response:
        """
        Updates an event by sending a PUT request to the API with the given event ID and JSON data.
        Args:
            event_id: The ID of the event to be updated.
            guest_id: The ID of the guest to be updated.
            guest_json_str: The JSON data representing the updated guest.

        Returns: HTTP status code
        """
        async with AsyncClient() as client:
            response = await client.put(f"{BASE_URL}/api/events/{event_id}/guests/{guest_id}", data=guest_json_str, timeout=10)
            response.raise_for_status()

        return response

    @classmethod
    async def delete_guest(cls, event_id: str, guest_id: str, card: ui.card | None = None) -> Response:
        """
        Delete single guest from API. Optionally, the UI element (card) may be provided (if calling from events page) so that
        it can be deleted visually upon clicking delete. This prevents needing to reload the page to show updates to the user

        Args:
            event_id: The ID of the event to delete
            guest_id: The ID of the guest to delete
            card: The ui component card to delete

        Returns:
            int: The status code of the response
        """
        async with AsyncClient() as client:
            response = await client.delete(f"{BASE_URL}/api/events/{event_id}/guests/{guest_id}", timeout=10)
            response.raise_for_status()

        if card is not None:
            card.delete()
            ui.notification("Guest deleted", timeout=1.5)

        return response


### little helpers ###
async def reload_page():
    """
    Asynchronous function to reload the page using JavaScript. Use sparingly--sign of something else wrong.
    """
    await ui.run_javascript("location.reload();")
