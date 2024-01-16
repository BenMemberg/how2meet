from datetime import datetime
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

        async def delete_event(event_id: str):
            async with httpx.AsyncClient() as client:
                response = await client.delete(f"http://localhost:8000/api/events/{event_id}", timeout=10)
                response.raise_for_status()
            ui.open("/events")

        # Display the list of events
        for event in events:
            with ui.card().classes("w-full"):
                with ui.row().classes("w-full justify-between"):
                    with ui.column().classes("flex-grow"):
                        ui.label(f"Event ID: {event['id']}")
                        ui.label(f"Event Name: {event['name']}")
                    ui.button("", icon="info", on_click=lambda event_id=event['id']: ui.open(f"/events/{event_id}")).classes("w-6 h-6")
                    ui.button("", icon="delete", color="red", on_click=lambda event_id=event['id']: delete_event(event_id)).classes("w-6 h-6")

        # Add navigation buttons
        with ui.row().classes("w-full justify-center"):
            ui.button("Back", on_click=lambda: ui.open("/"))
            ui.button("New Event", on_click=lambda: ui.open(f"/events/new/{uuid.uuid4()}"))


@router.page("/{event_id}")
async def event_home(event_id: str):
    """Detail page for a specific event"""
    # Get the event from the API
    # NOTE: This is a blocking call, so we use an async client

    with frame("Event Home"):
        async with httpx.AsyncClient() as client:
            event = await client.get(f"http://localhost:8000/api/events/{event_id}", timeout=10)
        try:
            event = event.json()
        except:
            event = {}

        # Display the event details
        with ui.column().classes("w-full justify-between"):
            for key, value in event.items():
                ui.label(f"{key}: {value}")
        ui.button("Back", on_click=lambda: ui.open("/events"))

@router.page("/new/{event_id}")
async def new_event(event_id: str):
    """New event creation page

    Args:
        event_id (str): The unique ID of the event to be created.

    Returns:
        None
    """


    async def add_guest():
        invite_uuid = str(uuid.uuid4())
        # TODO add method to remove guest
        with ui.card().classes("flex-grow position:relative") as card:
            async def delete(invite_uuid=invite_uuid):
                card.delete()
            with ui.row().classes("flex-grow justify-between items-center"):
                name_input = ui.input("Name")
                email_input = ui.input("Email")
                phone_input = ui.input("Phone Number")
                ui.button("", icon="delete", color="red", on_click=lambda invite_uuid=invite_uuid: delete(invite_uuid)).classes("w-6 h-6")


    with frame("New Event"):
        with ui.row().classes("flex-grow justify-between"):
            event_name_input = ui.input("Event Name")
            event_location_input = ui.input("Location")
        with ui.row():
            user_input = ui.input("User")
            password_input = ui.input("Password", password=True, password_toggle_button=True)
        with ui.row():
            with ui.expansion("Start Time"):
                start_date_input = ui.date(value=datetime.now().date().strftime("%Y-%m-%d"))
                start_time_input = ui.time(value=datetime.now().time().strftime("%H:%M"))
            with ui.expansion("End Time"):
                end_date_input = ui.date(value=datetime.now().date().strftime("%Y-%m-%d"))
                end_time_input = ui.time(value=datetime.now().time().strftime("%H:%M"))
            all_day_checkbox = ui.checkbox("All Day")
        with ui.row().classes("w-full"):
            description_input = ui.textarea("Description").classes("w-full")
        with ui.row().classes("w-full"):
            with ui.column().classes("w-full"):
                add_guest_button = ui.button("Add guest", on_click=add_guest)

        async def get_event_json():
            import json
            event_json = json.dumps({
                "id": event_id,
                "name": event_name_input.value,
                "created": datetime.now().isoformat(),
                "location": event_location_input.value,
                "organizer_name": user_input.value,
                "organizer_password": password_input.value,
                "description": description_input.value,
                "start_time": f"{start_date_input.value}T{start_time_input.value}:00",
                "end_time": f"{end_date_input.value}T{end_time_input.value}:00",
                "all_day": all_day_checkbox.value
            })
            return event_json

        async def post_event():
            event_json = await get_event_json()
            async with httpx.AsyncClient() as client:
                response = await client.post("http://localhost:8000/api/events/", data=event_json)
                response.raise_for_status()
            ui.open(f"/events/{event_id}")

        # TODO: Post invites to API

        save_button = ui.button("Save", on_click=post_event)
        back_button = ui.button("Back", on_click=lambda: ui.open("/"))
