"""

"""
from contextlib import contextmanager
import uuid

from fastapi import FastAPI
from nicegui import app, ui

from ..db.crud import get_events
from ..db.database import get_db
from .log_config import get_logger

logger = get_logger(__name__)

@contextmanager
def frame(navtitle: str):
    """Custom page frame to share the same styling and behavior across all pages"""
    # ui.colors(primary='#ffa3df', secondary='#c9a3ff', accent='#c9a3ff', positive='#c9a3ff')
    with ui.header().classes('justify-between text-white'):
        ui.label('How2Meet').classes('font-bold')
        ui.label(navtitle)
        with ui.row():
            header_links = {
                'Home': '/',
                'Events': '/events',
                'Settings': '/settings',
            }
            for link_text, link_target in header_links.items():
                if navtitle != link_text:
                    ui.link(link_text, link_target).classes(replace='text-white')

    with ui.footer().classes('justify-start text-white'):
        # with ui.row():
        ui.link('Donate', 'https://www.buymeacoffee.com/').classes('text-white')
        ui.link('GitHub', 'https://www.github.com/BenMemberg/how2meet').classes('text-white')

    yield

@ui.page("/settings")
def settings():
    with frame('Settings'):
        with ui.column().classes("absolute-center"):
            # NOTE dark mode will be persistent for each user across tabs and server restarts
            ui.dark_mode().bind_value(app.storage.user, "dark_mode")
            ui.checkbox("dark mode").bind_value(app.storage.user, "dark_mode")


@ui.page("/new_event/{event_id}")
def new_event(event_id: uuid.UUID):
    """1. Event Name
    2. Event Password
    3. Require event password from guests option [boolean] (public vs. private event)
    4. Date
    5. Number of guests limit [Optional]
    6. Photo [Optional]
    7. Description
    8. Agenda/Itinerary
    9. Guest list"""
    def add_guest():
        with ui.row().classes("w-full"):
            ui.input("Name").classes("w-1/3")
            ui.input("Email").classes("w-1/3")
            ui.input("Phone Number").classes("w-1/3")

    with frame('New Event'):
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

        ui.button("Save", on_click=lambda: ui.notify("Event details would be written to DB here"))
        ui.button("Back", on_click=lambda: ui.open("/"))

@ui.page("/events")
def events():
    db = next(get_db())
    events = get_events(db)
    with frame('Events'):
        for event in events:
            ui.link(event.name, f"/event/{event.id}")
        # ui.button("New Event", on_click=lambda: ui.open(f"/new_event/{uuid.uuid4()}"))
        # ui.button("Existing Event", on_click=lambda: ui.open("/existing_event"))
        ui.button("Back", on_click=lambda: ui.open("/"))

@ui.page("/event/{event_id}")
def event_home(event_id: str):
    with frame('Event Home'):
        ui.label(f"Event ID: {event_id}")
        ui.button("Back", on_click=lambda: ui.open("/"))

@ui.page("/")   # NOTE this is the default page
def home():
    with frame('Home'):
        with ui.column().classes("w-full items-center"):
            with ui.row():
                ui.button("New Event", on_click=lambda: ui.open(f"/new_event/{uuid.uuid4()}"))
            with ui.row():
                ui.button("Existing Event", on_click=lambda: ui.open("/existing_event"))


def init(fastapi_app: FastAPI) -> None:
    """
    Initializes the FastAPI application with the provided
    `fastapi_app` instance. This allows for FastAPI to be
    the driving force and NiceGUI to take the backseat.

    Args:
        fastapi_app (FastAPI): The FastAPI application instance
          to be initialized.

    Returns:
        None
    """
    ui.run_with(
        fastapi_app,
        storage_secret="private secret",  # NOTE setting a secret is optional but allows for persistent storage per user
    )
