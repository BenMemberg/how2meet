import uuid
from collections import namedtuple

from nicegui import ui, APIRouter
import httpx

from ..components.frames import frame
from ...utils.logging import get_file_logger

logger = get_file_logger(__name__)

router = APIRouter(prefix="/events",
                   tags=["events"])

@router.page("/")
async def events(user: str = None):
    """List page for all events"""
    with frame("Events"):
        async with httpx.AsyncClient() as client:
            events = await client.get(f"http://localhost:8000/api/events/", timeout=10)
        if isinstance(events, httpx.Response):
            events = events.json()
        else:
            events = []
        for event in events:
            with ui.row().classes("w-full"):
                with ui.card().classes("w-full"):
                    ui.label(f"Event ID: {event['id']}")
                    ui.label(f"Event Name: {event['name']}")
                    ui.button("Details", on_click=lambda event_id=event['id']: ui.open(f"/events/{event_id}"))
        with ui.row().classes("w-full justify-center"):
            ui.button("New Event", on_click=lambda: ui.open(f"/events/new/{uuid.uuid4()}"))
            ui.button("Back", on_click=lambda: ui.open("/"))


@router.page("/{event_id}")
def event_home(event_id: str):
    """Detail page for a specific event"""
    with frame("Event Home"):
        ui.label(f"Event ID: {event_id}")
        ui.button("Back", on_click=lambda: ui.open("/events"))

@router.page("/new/{event_id}")
def new_event(event_id: str):
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
        ui.button("Save", on_click=lambda: httpx.post(f"http://localhost:8000/events/{event_id}"))
        ui.button("Back", on_click=lambda: ui.open("/"))
