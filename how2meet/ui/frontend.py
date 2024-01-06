"""

"""
from contextlib import contextmanager
import uuid
from collections import namedtuple

from fastapi import FastAPI
from nicegui import app, ui

from .log_config import get_logger

logger = get_logger(__name__)

@contextmanager
def frame(navtitle: str):
    """Custom page frame to share the same styling and behavior across all pages"""
    with ui.header().classes('justify-between text-white items-center'):
        ui.link('How2Meet', '/').classes('no-underline font-bold text-white')
        ui.label(navtitle)
        ui.button(on_click=lambda: right_drawer.toggle()).props('flat color=white icon=menu')

    with ui.right_drawer().classes('gap-0 m-0 p-0') as right_drawer:
        with ui.row().classes('w-full gap-0'):
            header_links = {
                'Home': '/',
                'Events': '/events',
                'Settings': '/settings',
            }
            for link_text, link_target in header_links.items():
                with ui.card().on("click", lambda link_target=link_target: ui.open(link_target)) \
                              .classes('w-full no-shadow border-b-[1px] rounded-none hover:bg-gray-200') \
                              .style('cursor: pointer'):
                    ui.link(link_text, link_target).classes('w-full text-left no-underline font-bold')

    with ui.footer().classes('justify-between text-white flex items-center'):
        with ui.row().classes('flex-grow'):
            ui.link('Donate', 'https://www.buymeacoffee.com/').classes('text-white mr-4')
            ui.link('GitHub', 'https://www.github.com/BenMemberg/how2meet').classes('text-white mr-4')
        # put a settings icon on the far right of the footer
        ui.button(on_click=lambda: ui.open('/settings')).props('flat color=white icon=settings')

    yield

@ui.page("/settings")
def settings():
    """Settings page"""
    with frame('Settings'):
        with ui.column().classes("absolute-center"):
            # NOTE dark mode will be persistent for each user across tabs and server restarts
            ui.dark_mode().bind_value(app.storage.user, "dark_mode")
            ui.checkbox("dark mode").bind_value(app.storage.user, "dark_mode")

@ui.page("/new_event/{event_id}")
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
    # db = next(get_db())
    # events = get_events(db)
    events = [namedtuple('Event', ['id', 'name'])(uuid.uuid4(), 'Event 1'), namedtuple('Event', ['id', 'name'])(uuid.uuid4(), 'Event 2')]

    with frame('Events'):
        for event in events:
            ui.link(event.name, f"/event/{event.id}")
        ui.button("Back", on_click=lambda: ui.open("/"))

@ui.page("/event/{event_id}")
def event_home(event_id: str):
    """Detail page for a specific event"""
    with frame('Event Home'):
        ui.label(f"Event ID: {event_id}")
        ui.button("Back", on_click=lambda: ui.open("/events"))

@ui.page("/")   # NOTE this is the default page
def home():
    """Home page"""
    with frame('Home'):
        with ui.column().classes("w-full items-center"):
            with ui.row():
                ui.button("New Event", on_click=lambda: ui.open(f"/new_event/{uuid.uuid4()}"))
            with ui.row():
                ui.button("Existing Event", on_click=lambda: ui.open("/events"))


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
