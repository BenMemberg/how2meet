"""
Utility functions
"""
import json
import os
from typing import Coroutine

from httpx import AsyncClient
from nicegui import ui

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

"""Just using simple functions for now. In the future we may want to wrap in
a class. Perhaps if/when we require a token to interact with API?"""


async def get_events_api() -> list:
    # NOTE: This is a blocking call, so we use an async client
    async with AsyncClient() as client:
        events = await client.get(f"{BASE_URL}/api/events/", timeout=10)
    try:
        events = events.json()
    except:
        events = []

    return events


async def get_event_api(event_id: str) -> dict:
    # NOTE: This is a blocking call, so we use an async client
    async with AsyncClient() as client:
        event = await client.get(f"{BASE_URL}/api/events/{event_id}", timeout=10)
    try:
        event = event.json()
    except:
        event = {}

    return event


async def delete_event_api(event_id: str) -> int:
    async with AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}/api/events/{event_id}", timeout=10)
        response.raise_for_status()

    await ui.run_javascript("location.reload();")  # Refresh page to show changes

    return response.status_code


async def post_event_api(event_json) -> int:
    async with AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/api/events/", data=event_json, timeout=10)
        response.raise_for_status()

    return response.status_code
