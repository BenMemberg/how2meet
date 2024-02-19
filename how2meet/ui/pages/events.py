"""
Nicegui UI routes for all events pages. Use functions from `utils` to call the API. All routes prefixed with `/events/`
"""
import json
import uuid
from datetime import datetime
from functools import partial
from pathlib import Path

from nicegui import APIRouter, ui, app, Client

from how2meet.utils import APIClient as api

from ..components.frames import frame
from ..components.event_editor import EventEditor, RsvpEditor, StatusEnum
from ..components.date_utils import event_dates_to_str, event_times_to_str
from .urls import ROUTE_PREFIX_EVENTS, URL_EVENTS, URL_NEW_EVENT,\
      URL_EVENT_HOME, ROUTE_BASE, ROUTE_NEW_EVENT, ROUTE_EVENT_HOME, BASE_URL
import how2meet.ui.components.elements as elements

router = APIRouter(prefix=ROUTE_PREFIX_EVENTS, tags=["events"])

@router.page(ROUTE_BASE + "/test" )
async def events() -> None:
    frame()
    ui.label("Test")

@router.page(ROUTE_BASE)
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
    frame()
    # Display the list of events in refreshable cards
    @ui.refreshable
    async def render_list():
        events = await api.get_events()
        for event in events:
            with elements.card().classes("w-full") as event_card:
                with ui.row().classes("w-full justify-between items-center"):
                    with ui.column().classes("flex-grow"):
                        ui.label(f"Event ID: {event['id']}")
                        ui.label(f"Event Name: {event['name']}")

                    elements.button(icon="edit",
                                on_click=partial(open_floating_editor, _id=event["id"])
                                ).classes("w-6 h-6")
                    elements.button(icon="info",
                                on_click=lambda _id=event["id"]: ui.open(URL_EVENT_HOME.format(event_id=_id))
                                ).classes("w-6 h-6")

                    elements.button(icon="delete",
                                on_click=lambda _id=event["id"], card=event_card: api.delete_event(_id, card),
                                color="red"
                                ).classes("w-6 h-6")

    await render_list()

    # Add navigation buttons
    with ui.row().classes("w-full justify-center"):
        elements.button("Back", on_click=lambda: ui.open(URL_EVENTS))
        elements.button("New Event", on_click=lambda: ui.open(URL_NEW_EVENT))
        elements.button("Refresh", on_click=render_list.refresh)

@router.page(ROUTE_NEW_EVENT)
async def create():
    """New event creation page

    Args:
        event_id (str): The unique ID of the event to be created.

    Returns:
        None
    """

    frame()

    event_editor = EventEditor()
    # Render the event editor in page and set routing for save and back buttons
    await event_editor.render(
        on_back=partial(ui.open,
                        ROUTE_BASE),
        on_save=partial(ui.open,
                        URL_EVENT_HOME.format(event_id=event_editor.event_id)))

# must come after /create to avoid path order conflict
@router.page(ROUTE_EVENT_HOME)
async def event_home(event_id: uuid.UUID, client: Client):
    """Detail page for a specific event"""
        # Display the list of guests in refreshable cards
    @ui.refreshable
    async def render_guests():
        guests = await api.get_guests_from_event(event_id)
        with ui.column().classes("w-full"):
            # sort guests by name and status
            avatar_colors = [color for color in elements.PALETTES.values() if color != elements.PALETTES["dark"]]
            guests_going = sorted([guest for guest in guests if guest.get("status") == StatusEnum.GOING.value], key=lambda x: x.get("name"))
            guests_not_going = sorted([guest for guest in guests if guest.get("status") != StatusEnum.GOING.value], key=lambda x: x.get("name"))
            i = 0
            for guest in guests_going + guests_not_going:
                with ui.row().classes("w-full justify-left items-center"):
                    ui.avatar(guest.get("name")[0], color=avatar_colors[i], text_color="white", size="5xl")
                    # green check if going, red x if not going
                    icons = {
                        StatusEnum.GOING.value: "check",
                        StatusEnum.NOT_GOING.value: "close",
                        StatusEnum.MAYBE.value: "question_mark"
                    }
                    icon_colors = {
                        StatusEnum.GOING.value: "color=green",
                        StatusEnum.NOT_GOING.value: "color=red",
                        StatusEnum.MAYBE.value: "color=yellow"
                    }
                    ui.icon(icons.get(guest['status']))\
                        .classes("text-2xl")\
                        .props(icon_colors.get(guest['status']))
                    ui.label(f"{guest.get('name')}").classes("text-xl")
                    # increment color index
                    if i < len(avatar_colors) - 1:
                        i += 1
                    else:
                        i = 0

    async def open_floating_editor(_id):
        # Initialize the event editor and render it in a floating dialog
        event_editor = EventEditor(_id)
        await event_editor.render(floating=True,
                                  on_save=event_editor.close,
                                  on_back=event_editor.close)
        event_editor.dialog.on("hide", render_event.refresh)

    frame()
    # Get the event from the API
    @ui.refreshable
    async def render_event():
        event = await api.get_event(event_id)

        with ui.column().classes("w-full justify-center pt-10"):
            ui.label(f"{event.get('name')}").classes("cursor-pointer text-5xl font-bold border-l-8 border-teal-500 pl-4")\
                .on("click", lambda: open_floating_editor(event_id))
            ui.label(f"Host: {event.get('organizer')}").classes("cursor-pointer text-xl border-l-8 border-teal-600 pl-4 pr-4")\
                .on("click", lambda: open_floating_editor(event_id))
            with ui.column().classes("cursor-pointer w-full justify-left border-l-8 border-amber-300 pl-4"):
                ui.label(f"{event_dates_to_str(event)}").classes("cursor-pointer text-xl")\
                    .on("click", lambda: open_floating_editor(event_id))
                ui.label(f"{event_times_to_str(event)}").classes("cursor-pointer text-xl")\
                    .on("click", lambda: open_floating_editor(event_id))
            ui.label(f"{event.get('location')}").classes("cursor-pointer text-xl border-l-8 border-orange-400 pl-4 pr-4")\
                .on("click", lambda: open_floating_editor(event_id))
            ui.label(f"{event.get('description')}").classes("cursor-pointer text-xl border-l-8 border-orange-600 pl-4 pr-4")\
                .on("click", lambda: open_floating_editor(event_id))

        rsvp_editor = RsvpEditor(event_id)
        with ui.row().classes("w-full justify-left items-center"):
            elements.button("RSVP", on_click=partial(rsvp_editor.render, floating=True, on_save=render_guests.refresh))
            # copy url to clipboard
            icon = ui.icon("link").on("click", lambda: ui.notify("Copied link to clipboard")).classes("text-3xl cursor-pointer")
            icon._props["onclick"] = f"navigator.clipboard.writeText('{BASE_URL}{app.url_path_for('event_home', event_id=event_id)}')"

    await render_event()
    # Get the list of guests from the API
    ui.label("Who's Going...").classes("text-xl font-bold")
    await render_guests()
