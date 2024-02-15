"""

"""
import logging
from functools import partial

from nicegui import app, ui

from .components.frames import frame
from .pages import events, settings
from .pages.urls import URL_NEW_EVENT
import how2meet.ui.components.elements as elements

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


app.include_router(events.router)
app.include_router(settings.router)


@ui.page("/")  # NOTE this is the default page
def home():
    """Home page"""
    frame()

    # @ui.refreshable
    # def show_link_submit(link_input):
    #     if link_input.value:
    #         elements.button("Go", on_click=partial(ui.open, link_input.value)).classes("mt-4")

    with ui.column().classes("w-full absolute-center items-center"):
        elements.label("Welcome to How2Meet").classes("text-3xl font-bold mb-4")
        elements.label("The zero sign up event manager").classes("text-xl mb-4")
        elements.button("New Event", on_click=lambda: ui.open(URL_NEW_EVENT))
        # with ui.row().classes("w-full justify-center items-center"):
        #     link_input = elements.input("I have a link...").classes("mt-4")
        #     link_input.on("keydown.enter", lambda: ui.open(link_input.value))
        #     show_link_submit(link_input)
        #     link_input.on("change", partial(show_link_submit.refresh, link_input))


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
