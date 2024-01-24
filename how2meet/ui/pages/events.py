"""
Nicegui UI routes for all events pages. Use functions from `utils` to call the API. All routes prefixed with `/events/`
"""
import uuid
from datetime import datetime

from nicegui import APIRouter, ui, app

from how2meet.utils import APIClient as api

from ..components.frames import frame
from ..components.event_editor import EventEditor, InviteEditor
from .urls import URL_EVENTS_PREFIX, URL_EVENTS, URL_NEW_EVENT,\
      URL_EVENT_HOME, ROUTE_EVENTS, ROUTE_NEW_EVENT, ROUTE_EVENT_HOME


router = APIRouter(prefix=URL_EVENTS_PREFIX, tags=["events"])

@router.page(ROUTE_EVENTS)
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
            ui.button("Back", on_click=lambda: ui.open(URL_EVENTS))
            ui.button("New Event", on_click=lambda: ui.open(URL_NEW_EVENT))


@router.page(ROUTE_EVENT_HOME)
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


@router.page(ROUTE_NEW_EVENT)
async def new_event():
    """New event creation page

    Args:
        event_id (str): The unique ID of the event to be created.

    Returns:
        None
    """

    with frame("New Event"):
        event_editor = EventEditor()
        await event_editor.render()
