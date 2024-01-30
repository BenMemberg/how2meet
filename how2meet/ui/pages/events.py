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
from .urls import ROUTE_PREFIX_EVENTS, URL_EVENTS, URL_NEW_EVENT,\
      URL_EVENT_HOME, ROUTE_EVENTS_LIST, ROUTE_NEW_EVENT, ROUTE_EVENT_HOME
from ..components.date_utils import event_dates_to_str


router = APIRouter(prefix=ROUTE_PREFIX_EVENTS, tags=["events"])

@router.page(ROUTE_EVENTS_LIST)
async def events() -> None:
    """List page for all events"""
    with frame("Events"):
        # Get the list of events from the API
        async def open_floating_editor(_id):
            event_editor = EventEditor(_id)
            await event_editor.render(floating=True,
                                      on_save=partial(ui.notify, "Event saved!"),
                                      on_back=event_editor.close)
            event_editor.dialog.on("hide", render_list.refresh)
        # Display the list of events
        @ui.refreshable
        async def render_list():
            events = await api.get_events()
            for event in events:
                with ui.card().classes("w-full") as event_card:
                    with ui.row().classes("w-full justify-between"):
                        with ui.column().classes("flex-grow"):
                            ui.label(f"Event ID: {event['id']}")
                            ui.label(f"Event Name: {event['name']}")
                        ui.button("", icon="edit", on_click=partial(open_floating_editor, _id=event["id"])).classes("w-6 h-6")
                        ui.button("", icon="info", on_click=lambda _id=event["id"]: ui.open(URL_EVENT_HOME.format(event_id=_id))).classes("w-6 h-6")
                        ui.button("", icon="delete", color="red", on_click=lambda _id=event["id"], card=event_card: api.delete_event(_id, card))
        await render_list()

        # Add navigation buttons
        with ui.row().classes("w-full justify-center"):
            ui.button("Back", on_click=lambda: ui.open(URL_EVENTS))
            ui.button("New Event", on_click=lambda: ui.open(URL_NEW_EVENT))
            ui.button("Refresh", on_click=render_list.refresh)


@router.page(ROUTE_EVENT_HOME)
async def event_home(event_id: str):
    """Detail page for a specific event"""
    # Get the event from the API

    with frame("Event Home"):
        # set the padding of top level content div to 0
        context.get_client().content.classes("m-0 p-0 gap-0")
        event = await api.get_event(event_id)
        ui.image(event.get('image', './how2meet/ui/assets/default-image.jpeg')).classes(
            "w-full h-64 m-0 p-0 object-cover")
        with ui.column().classes("w-full justify-left space-y-0 p-4"):
            ui.label(f"{event['name']}").classes("text-2xl font-bold")
            ui.label(f"{event_dates_to_str(event)}").classes("text-xl")
            ui.label(f"{event['location'] or 'Unknown'}").classes("text-base text-gray-800")
        with ui.card().classes("w-full-m-4 p-4"):
            ui.label("Details").classes("text-xl font-bold")
            with ui.row().classes("w-full justify-left items-center"):
                ui.icon("person").classes("text-xl")
                ui.label(f"{len(event.get('invites', []))} Invites")
            ui.label(f"{event['description']}").classes("text-base text-gray-800")
        ui.button("Back", on_click=lambda: ui.open("/events"))


@router.page(ROUTE_NEW_EVENT)
async def new_event():
    """New event creation page

    Args:
        event_id (str): The unique ID of the event to be created.

    Returns:
        None
    """

    with frame("New Event"):
        event_editor = EventEditor()
        await event_editor.render(
            on_back=partial(ui.open,
                            URL_EVENTS),
            on_save=partial(ui.open,
                             URL_EVENT_HOME.format(event_id=event_editor.event_id)))
