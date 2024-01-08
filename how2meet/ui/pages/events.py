import logging
import requests
import uuid
from collections import namedtuple

from nicegui import ui, APIRouter

from ..components.frames import frame

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter(prefix="/events",
                   tags=["events"])

@router.page("/")
def events(user: str = None):
    """List page for all events"""

    try:
        events = requests.get("http://localhost:8000/events/").json()
    except:
        events = [
            namedtuple("Event", ["id", "name"])(uuid.uuid4(), "Event 1"),
            namedtuple("Event", ["id", "name"])(uuid.uuid4(), "Event 2"),
        ]

    with frame("Events"):
        for event in events:
            ui.label(event.name)
        ui.button("Back", on_click=lambda: ui.open("/"))


@router.page("/{event_id}")
def event_home(event_id: uuid.UUID):
    """Detail page for a specific event"""
    with frame("Event Home"):
        ui.label(f"Event ID: {event_id}")
        ui.button("Back", on_click=lambda: ui.open("/events"))

@router.page("/new/{event_id}")
def new_event(event_id: uuid.UUID):
    """New event creation page

    Args:
        event_id (uuid.UUID): The unique ID of the event to be created.

    Returns:
        None
    """

    def add_guest():
        with ui.row().classes("w-full"):
            ui.input("Name").classes("w-1/3")
            ui.input("Email").classes("w-1/3")
            ui.input("Phone Number").classes("w-1/3")

    with frame("New Event"):
        with ui.column().classes("w-full"):
            with ui.row().classes("w-1/2"):
                ui.input("Event Name").classes("w-full")
            with ui.row():
                ui.input("Password", password=True, password_toggle_button=True)
            with ui.row():
                with ui.expansion("Expand"):
                    ui.date()
                    ui.time()
            with ui.row():
                ui.input("Description")
            with ui.row().classes("w-half"):
                with ui.column():
                    ui.button("Add guest", on_click=add_guest)

        # TODO: use actual url for post request
        ui.button("Save", on_click=lambda: requests.post(f"http://localhost:8000/events/{event_id}"))
        ui.button("Back", on_click=lambda: ui.open("/"))
