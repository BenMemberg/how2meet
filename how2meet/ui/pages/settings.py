import logging

from nicegui import APIRouter, app, ui

from ..components.frames import frame

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter(prefix="/settings", tags=["settings"])


@router.page("/")
def settings():
    """Settings page"""
    with frame("Settings"):
        with ui.column().classes("absolute-center"):
            # NOTE dark mode will be persistent for each user across tabs and server restarts
            ui.dark_mode().bind_value(app.storage.user, "dark_mode")
            ui.checkbox("dark mode").bind_value(app.storage.user, "dark_mode")
