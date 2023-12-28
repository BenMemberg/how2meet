"""

"""
from fastapi import FastAPI
from nicegui import app, ui

from ..db.crud import get_events
from ..db.database import get_db


@ui.page("/show")
def show():
    ui.label("Hello, FastAPI!")

    # NOTE dark mode will be persistent for each user across tabs and server restarts
    ui.dark_mode().bind_value(app.storage.user, "dark_mode")
    ui.checkbox("dark mode").bind_value(app.storage.user, "dark_mode")


@ui.page("/events_list/")
def show_events():
    # Use `next() as workaround AttributeError: 'generator' object has no attribute 'query'
    # (FastAPI makes initial call to generator object to get Session object using `Depends()`
    db = next(get_db())
    events = get_events(db)
    with ui.column():
        ui.label("Events!")
        ui.label(f"Total events: {len(events)}")


def init(fastapi_app: FastAPI) -> None:
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
        storage_secret="private secret",  # NOTE setting a secret is optional but allows for persistent storage per user
    )
