"""
Nicegui UI routes for all events pages. Use functions from `utils` to call the API. All routes prefixed with `/events/`
"""
import uuid
from datetime import datetime
from functools import partial
from pathlib import Path
from PIL import Image as PIL_Image
from nicegui import APIRouter, ui, app, context

from how2meet.utils import APIClient as api

from ..components.frames import frame
from ..components.event_editor import EventEditor, InviteEditor
from ..components.date_utils import event_dates_to_str, event_times_to_str
from .urls import ROUTE_PREFIX_EVENTS, URL_EVENTS, URL_NEW_EVENT,\
      URL_EVENT_HOME, ROUTE_EVENTS_LIST, ROUTE_NEW_EVENT, ROUTE_EVENT_HOME
import how2meet.ui.components.styles as styles

router = APIRouter(prefix=ROUTE_PREFIX_EVENTS, tags=["events"])

@router.page(ROUTE_EVENTS_LIST)
async def events() -> None:
    """List page for all events"""

    # Define a function to open the event editor in a floating dialog
    async def open_floating_editor(_id):

        # Notify and refresh the list when the event is saved
        def on_save():
            ui.notify("Event saved!")
            render_list.refresh()

        # Initialize the event editor and render it in a floating dialog
        event_editor = EventEditor(_id)
        await event_editor.render(floating=True,
                                    on_save=on_save,
                                    on_back=event_editor.close)
        event_editor.dialog.on("hide", render_list.refresh)

    # Define page layout
    frame("Events")
        # Display the list of events in refreshable cards
    @ui.refreshable
    async def render_list():
        events = await api.get_events()
        for event in events:
            with styles.card().classes("w-full") as event_card:
                with ui.row().classes("w-full justify-between items-center"):
                    with ui.column().classes("flex-grow"):
                        ui.label(f"Event ID: {event['id']}")
                        ui.label(f"Event Name: {event['name']}")

                    styles.button(icon="edit",
                                on_click=partial(open_floating_editor, _id=event["id"])
                                ).classes("w-6 h-6").props("outline color=white")

                    styles.button(icon="info",
                                on_click=lambda _id=event["id"]: ui.open(URL_EVENT_HOME.format(event_id=_id))
                                ).classes("w-6 h-6").props("outline color=white")

                    styles.button(icon="delete",
                                on_click=lambda _id=event["id"], card=event_card: api.delete_event(_id, card),
                                color="red"
                                ).classes("w-6 h-6").props("outline color=white")

    await render_list()

    # Add navigation buttons
    with ui.row().classes("w-full justify-center"):
        styles.button("Back", on_click=lambda: ui.open(URL_EVENTS)).props("outline color=white")
        styles.button("New Event", on_click=lambda: ui.open(URL_NEW_EVENT)).props("outline color=white")
        styles.button("Refresh", on_click=render_list.refresh).props("outline color=white")


@router.page(ROUTE_EVENT_HOME)
async def event_home(event_id: str):
    """Detail page for a specific event"""
    # Iphone12 390x844 pt (1170x2532 px @3x)
    frame("Event Home")

    # Get the event from the API
    event = await api.get_event(event_id)

    with ui.column().classes("w-full justify-center pt-10"):
        ui.label(f"{event.get('name')}").classes("text-5xl font-bold border-l-8 border-teal-500 pl-4")
        with ui.column().classes("w-full justify-left border-l-8 border-amber-300 pl-4"):
            ui.label(f"{event_dates_to_str(event)}").classes("text-xl")
            ui.label(f"{event_times_to_str(event)}").classes("text-xl")
        ui.label(f"{event.get('location')}" or "Undetermined Location").classes("text-xl border-l-8 border-orange-400 pl-4 pr-4")
        ui.label(f"{event.get('description')}" or "idk just come").classes("text-xl border-l-8 border-orange-600 pl-4 pr-4")

    styles.button("RSVP", on_click=ui.dialog).props("outline color=white")

    n_guests = range(100)
    guest_names = [f"Guest {i}" for i in n_guests]
    ui.label("Who's Going...").classes("text-xl font-bold")
    with ui.column().classes("w-full"):
        i = 0
        avatar_colors = [color for color in styles.PALETTES.values() if color != styles.PALETTES["dark"]]
        for guest in guest_names:
            with ui.row().classes("w-full justify-left items-center"):
                ui.avatar(guest[0], color=avatar_colors[i], text_color="white", size="5xl")
                ui.label(f"{guest}").classes("text-xl")
                if i < len(avatar_colors) - 1:
                    i += 1
                else:
                    i = 0

@router.page(ROUTE_NEW_EVENT)
async def new_event():
    """New event creation page

    Args:
        event_id (str): The unique ID of the event to be created.

    Returns:
        None
    """

    frame("New Event")

    event_editor = EventEditor()
    # Render the event editor in page and set routing for save and back buttons
    await event_editor.render(
        on_back=partial(ui.open,
                        URL_EVENTS),
        on_save=partial(ui.open,
                            URL_EVENT_HOME.format(event_id=event_editor.event_id)))
