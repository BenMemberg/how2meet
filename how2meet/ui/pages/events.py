import uuid
from collections import namedtuple

from nicegui import ui, APIRouter
import httpx

from ..components.frames import frame

router = APIRouter(prefix="/events",
                   tags=["events"])

@router.page("/")
async def events(user: str = None):
    """List page for all events"""
    with frame("Events"):
        # Get the list of events from the API
        # NOTE: This is a blocking call, so we use an async client
        async with httpx.AsyncClient() as client:
            events = await client.get(f"http://localhost:8000/api/events/", timeout=10)
        try:
            events = events.json()
        except:
            events = []

        # Display the list of events
        for event in events:
            with ui.card().classes("w-full"):
                with ui.row().classes("w-full justify-between"):
                    ui.label(f"Event ID: {event['id']}")
                    ui.label(f"Event Name: {event['name']}")
                    ui.button("Details", on_click=lambda event_id=event['id']: ui.open(f"/events/{event_id}"))

        # Add navigation buttons
        with ui.row().classes("w-full justify-center"):
            ui.button("Back", on_click=lambda: ui.open("/"))
            ui.button("New Event", on_click=lambda: ui.open(f"/events/new/{uuid.uuid4()}"))


@router.page("/{event_id}")
async def event_home(event_id: str):
    """Detail page for a specific event"""
    with frame("Event Home"):
        ui.label(f"Event ID: {event_id}")
        ui.button("Back", on_click=lambda: ui.open("/events"))

@router.page("/new/{event_id}")
async def new_event(event_id: str):
    """New event creation page

    Args:
        event_id (str): The unique ID of the event to be created.

    Returns:
        None
    """
    from ...db.schemas import EventCreate
    from ..components.event_model import Event, Guest

    event = Event(event_id)

    def add_guest():
        guest = Guest(uuid.uuid4())
        event.add_guest(guest)
        with ui.row().classes("w-full"):
            ui.input("Name", on_change=lambda text, guest=guest: setattr(guest, 'name', text.value)).classes("w-1/3")
            ui.input("Email", on_change=lambda text, guest=guest: setattr(guest, 'email', text.value)).classes("w-1/3")
            ui.input("Phone Number", on_change=lambda text, guest=guest: setattr(guest, 'phone', text.value)).classes("w-1/3")

    with frame("New Event"):
        with ui.column().classes("w-full"):
            with ui.row().classes("w-1/2"):
                ui.input("Event Name",
                         on_change=lambda text: setattr(event, 'name', text.value)).classes("w-full")
            with ui.row():
                ui.input("Location", on_change=lambda text: setattr(event, 'location', text.value)).classes("w-full")
            with ui.row():
                ui.input("User", on_change=lambda text: setattr(event, 'organizer_name', text.value)).classes("w-1/2")
                ui.input("Password", password=True, password_toggle_button=True,
                         on_change=lambda text: setattr(event, 'organizer_password', text.value)).classes("w-1/2")
            with ui.row():
                with ui.expansion("Start Time"):
                    ui.date(on_change=lambda date: event.set_time_attr('start_time', date=date.value))
                    ui.time(on_change=lambda time: event.set_time_attr('start_time', time=time.value))
                with ui.expansion("End Time"):
                    ui.date(on_change=lambda date: event.set_time_attr('end_time', date=date.value))
                    ui.time(on_change=lambda time: event.set_time_attr('end_time', time=time.value))
            with ui.row():
                # TODO: disable end time and time selects if all day is checked
                ui.checkbox("All Day", on_change=lambda checked: setattr(event, 'all_day', checked.value))
            with ui.row():
                ui.input("Description", on_change=lambda text: setattr(event, 'description', text.value)).classes("w-full")
            with ui.row().classes("w-half"):
                with ui.column():
                    ui.button("Add guest", on_click=add_guest)

        # TODO: use actual url for post request
        # TODO: use details from page to create event
        ui.button("Save", on_click=lambda: event.save(f"http://localhost:8000/events/"))
        ui.button("Back", on_click=lambda: ui.open("/"))
        from pprint import pformat
        ui.button("Test", on_click=lambda: ui.notify(event.__dict__))
