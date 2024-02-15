import logging

from nicegui import APIRouter, app, ui

from how2meet.ui.components import elements

from ..components.frames import frame
from .urls import URL_SETTINGS

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter(prefix=URL_SETTINGS, tags=["settings"])


@router.page("/")
def settings():
    """Settings page"""
    frame("Settings")
    # NOTE dark mode will be persistent for each user across tabs and server restarts
    ui.dark_mode().bind_value(app.storage.user, "dark_mode")
    elements.checkbox("dark mode").bind_value(app.storage.user, "dark_mode")
