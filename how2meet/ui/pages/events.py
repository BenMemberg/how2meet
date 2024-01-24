"""
Nicegui UI routes for all events pages. Use functions from `utils` to call the API. All routes prefixed with `/events/`
"""
import uuid
from datetime import datetime

from nicegui import APIRouter, ui

from how2meet.utils import APIClient as api

from ..components.frames import frame
from ..components.event_editor import EventEditor, InviteEditor

router = APIRouter(prefix="/events", tags=["events"])


@router.page("/")
async def events() -> None:
    """List page for all events"""
    with frame("Events"):
        # Get the list of events from the API
        events = await api.get_events()

        # Display the list of events
        for event in events:
            with ui.card().classes("w-full") as event_card:
                with ui.row().classes("w-full justify-between"):
                    with ui.column().classes("flex-grow"):
                        ui.label(f"Event ID: {event['id']}")
                        ui.label(f"Event Name: {event['name']}")
                    ui.button("", icon="info", on_click=lambda _id=event["id"]: ui.open(f"/events/{_id}")).classes("w-6 h-6")
                    ui.button("", icon="delete", color="red", on_click=lambda _id=event["id"], card=event_card: api.delete_event(_id, card))

        # Add navigation buttons
        with ui.row().classes("w-full justify-center"):
            ui.button("Back", on_click=lambda: ui.open("/"))
            ui.button("New Event", on_click=lambda: ui.open(f"/events/new_event"))


@router.page("/home/{event_id}")
async def event_home(event_id: str):
    """Detail page for a specific event"""
    # Get the event from the API

    with frame("Event Home"):
        event = await api.get_event(event_id)

        # Display the event details
        with ui.column().classes("w-full justify-between"):
            for key, value in event.items():
                ui.label(f"{key}: {value}")
        ui.button("Back", on_click=lambda: ui.open("/events"))


@router.page("/new_event")
async def new_event():
    """New event creation page

    Args:
        event_id (str): The unique ID of the event to be created.

    Returns:
        None
    """

    with frame("New Event"):
        event_editor = EventEditor()
        await event_editor.load()
        await event_editor.render()
