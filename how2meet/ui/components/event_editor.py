import logging
import uuid
from datetime import datetime
from functools import partial

from nicegui import ui

import how2meet.ui.components.elements as elements
from how2meet.ui.pages.urls import URL_EVENT_HOME, URL_EVENTS, URL_NEW_EVENT
from how2meet.utils import APIClient as api

logger = logging.getLogger(__name__)


class RsvpEditor:
    def __init__(self, event_id: str):
        self.event_id = event_id
        self.guest = None

    async def save(self, on_save=None):
        if not self.phone_input.value:
            ui.notification("Phone number is required", timeout=5)
            return

        guest_json_str = self.model_dump()
        status = await api.create_guest(self.event_id, guest_json_str)
        if status.is_success:
            if self.dialog:
                self.dialog.close()
            ui.notify("Saved!")

        if status.is_success:
            if callable(on_save):
                on_save()
        else:
            logger.debug(f"Error: {status}")
            ui.notification(f"Error: {status}", timeout=5)

    async def render(self, floating=True, on_save=None):
        # TODO add method to remove guest
        if floating:
            with elements.dialog(value=True).props("no-route-dismiss") as dialog:
                self.dialog = dialog
                with elements.card():
                    await self.render(floating=False, on_save=on_save)
                    return

        with elements.card().classes("flex-grow position:relative") as card:
            self.card = card
            with ui.column().classes("flex-grow justify-between items-center"):
                self.name_input = elements.input("Name")
                self.email_input = elements.input("Email")
                self.phone_input = elements.input("Phone Number")
                self.status_input = ui.radio(["Yes", "No"])
                self.submit_button = elements.button("Submit", on_click=partial(self.save, on_save=on_save))

    def model_dump(self):
        phone_number = "".join(filter(str.isdigit, self.phone_input.value)) if self.phone_input.value else None
        return {
            "id": str(uuid.uuid4()),
            "name": self.name_input.value,
            "email": self.email_input.value,
            "phone": phone_number,
            "status": self.status_input.value,
            "event_id": self.event_id,
        }


class EventEditor:
    def __init__(self, event_id=None):
        self.event_id = event_id or str(uuid.uuid4())
        self.event = {}
        self.invites = []
        self.dialog = None

    async def load(self):
        if self.event_id is not None:
            self.event = await api.get_event(self.event_id)

    async def save(self, on_save=None):
        try:
            if self.event:
                status = await api.update_event(self.event_id, self.model_dump())
            else:
                status = await api.create_event(self.model_dump())
        except Exception as e:
            logger.debug(e)
            return

        if status.is_success:
            if callable(on_save):
                on_save()
        else:
            logger.debug(f"Error: {status}")
            ui.notification(f"Error: {status}", timeout=5)

    def close(self):
        try:
            self.dialog.close()
        except:
            pass

    async def render(self, floating=False, on_save=None, on_back=None):
        # If floating, enclose in a dialog
        if floating:
            with elements.dialog(value=True).classes("w-7/8").props("no-route-dismiss") as dialog:
                self.dialog = dialog
                with elements.card().style("min-width: 100%"):
                    # Render the event editor (use floating=False to embed in enclosing element)
                    await self.render(on_save=on_save, on_back=on_back)
                    return

        # Load the event data
        await self.load()

        # Render forms
        self.event_name_input = elements.input("Event Name", value=self.event.get("name", ""))
        self.event_location_input = elements.input("Location", value=self.event.get("location", ""))

        with ui.row():
            self.user_input = elements.input("User", value=self.event.get("organizer_name", ""))
            self.password_input = elements.input("Password", password=True, password_toggle_button=True)

        with ui.row():
            with ui.expansion("Start Time"):
                with ui.row().classes("w-full"):
                    start_time = self.event.get("start_time", datetime.now())
                    if isinstance(start_time, str):
                        start_time = datetime.fromisoformat(start_time)
                    self.start_date_input = elements.date(value=start_time.strftime("%Y-%m-%d"))
                    self.start_time_input = elements.time(value=start_time.strftime("%H:%M"))
            with ui.expansion("End Time"):
                with ui.row().classes("w-full"):
                    end_time = self.event.get("end_time", datetime.now())
                    if isinstance(end_time, str):
                        end_time = datetime.fromisoformat(end_time)
                    self.end_date_input = elements.date(value=end_time.strftime("%Y-%m-%d"))
                    self.end_time_input = elements.time(value=end_time.strftime("%H:%M"))
            self.all_day_checkbox = elements.checkbox("All Day", value=self.event.get("all_day", False))

        with ui.row().classes("w-full"):
            self.description_input = elements.textarea("Description", value=self.event.get("description", "")).classes("w-full")

        with ui.row().classes("w-full justify-end"):

            def call_on_back():
                if callable(on_back):
                    on_back()

            elements.button("Back", on_click=call_on_back)
            elements.button("Save", on_click=partial(self.save, on_save=on_save))

    def model_dump(self):
        return {
            "id": self.event_id,
            "name": self.event_name_input.value,
            "created": datetime.now().isoformat(),
            "start_time": f"{self.start_date_input.value}T{self.start_time_input.value}:00",
            "end_time": f"{self.end_date_input.value}T{self.end_time_input.value}:00",
            "all_day": self.all_day_checkbox.value,
            "location": self.event_location_input.value,
            "organizer_name": self.user_input.value,
            "organizer_password": self.password_input.value,
            "description": self.description_input.value,
        }
