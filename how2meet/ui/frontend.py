"""

"""
import logging
import uuid

from nicegui import app, ui

from .components.frames import frame
from .pages import events, settings
from .pages.urls import URL_NEW_EVENT, URL_EVENTS
import how2meet.ui.components.elements as elements

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


app.include_router(events.router)
app.include_router(settings.router)


@ui.page("/")  # NOTE this is the default page
def home():
    """Home page"""
    frame("Home")
    with ui.column().classes("w-full items-center"):
        with ui.row():
            elements.button("New Event", on_click=lambda: ui.open(URL_NEW_EVENT))
        with ui.row():
            elements.button("Existing Event", on_click=lambda: ui.open(URL_EVENTS))


def init(fastapi_app) -> None:
    """
    Initializes the FastAPI application with the provided `fastapi_app` instance. This allows for FastAPI to be
    the driving force and NiceGUI to take the backseat.

    Args:
        fastapi_app (FastAPI): The FastAPI application instance to be initialized.

    Returns:
        None
    """

    ui.run_with(
        fastapi_app,
        title="How2Meet",
        storage_secret="private secret",  # NOTE setting a secret is optional but allows for persistent storage per user
    )
