from functools import partial
from datetime import datetime
import logging
import uuid
from enum import Enum

from nicegui import ui, app

from how2meet.utils import APIClient as api
from how2meet.ui.pages.urls import URL_EVENTS, URL_NEW_EVENT, URL_EVENT_HOME
import how2meet.ui.components.elements as elements

logger = logging.getLogger(__name__)

class StatusEnum(Enum):
    GOING = "Going"
    NOT_GOING = "Not Going"
    MAYBE = "Maybe"

    @classmethod
    def choices(cls):
        return [e.value for e in cls]

class TokenDialog:

    def __init__(self, auth_token: str):
        self.dialog = None
        self.auth_token = auth_token

    async def send_email(self):
        ui.notification("Email functionality coming soon!")

    async def render(self, on_next, floating=True):
        if floating:
            with ui.dialog(value=True).props("persistent") as dialog:
                self.dialog = dialog
                with elements.card():
                    await self.render(on_next, floating=False)
                    return

        with ui.column().classes("flex-grow justify-between items-center"):
            elements.label("Your event has been saved!").classes("text-2xl text-center w-full")
            elements.label("We'll try to remember you in this browser, but in case we mess up save the token below to edit your event later.").classes("text-xl w-full text-center")
            with elements.card().classes("flex-grow position:relative") as card:
                card.classes("border-2 border-teal-500 no-wrap")
                with ui.row().classes("w-full items-center justify-between"):
                    self.token_display = elements.label(self.auth_token).classes("text-xl")
                    copy_icon = ui.icon("content_copy").classes("cursor-pointer text-2xl")
                    copy_icon.on("click", lambda: ui.notify("Copied to clipboard!"))
                    copy_icon._props["onclick"] = f"navigator.clipboard.writeText('{self.auth_token}');"
            elements.label("We can also send it to your email if you want.").classes("text-xl text-center w-full")
            with ui.row().classes("w-full items-center justify-between"):
                self.email_input = elements.input("Email").classes("flex-grow")
                self.send_button = elements.button("Send", on_click=self.send_email).classes("max-w-1/3")
            self.next_button = elements.button("Next", on_click=on_next).classes("w-1/3")

class RsvpEditor:

        def __init__(self, event_id: uuid.UUID):
            self.event_id = event_id
            self.guest = None


        async def save(self, on_save=None):
            guest_json_str = self.model_dump()
            status = await api.create_guest(str(self.event_id), guest_json_str)
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
                with elements.dialog(value=True) as dialog:
                    self.dialog = dialog
                    await self.render(floating=False, on_save=on_save)
                    return

            with elements.card().classes("flex-grow") as card:
                self.card = card
                with ui.column().classes("w-full justify-between items-center"):
                    self.name_input = elements.input("Name").classes("w-full")
                    self.email_input = elements.input("Email (Optional)").classes("w-full")
                    self.phone_input = elements.input("Phone Number (Optional)").classes("w-full")
                    with ui.row().classes("w-full"):
                        self.status_input = ui.radio(StatusEnum.choices()).classes("w-full")
                    self.submit_button = elements.button("Submit", on_click=partial(self.save, on_save=on_save))

        def model_dump(self):
            phone_number = "".join(filter(str.isdigit, self.phone_input.value)) if self.phone_input.value else None
            return {
                    "id": str(uuid.uuid4()),
                    "name": self.name_input.value,
                    "email": self.email_input.value,
                    "phone": phone_number,
                    "status": self.status_input.value,
                    "event_id": str(self.event_id),
                    }


class EventEditor:

    def __init__(self, event_id=None):
        self.event_id = event_id or uuid.uuid4()
        self.event = {}
        self.dialog = None

    async def load(self):
        if self.event_id is not None:
            self.event = await api.get_event(self.event_id)

    async def save(self, on_save=None):
        if not app.storage.user.get("auth_token"):
            app.storage.user["auth_token"] = uuid.uuid4()

        model_dump = self.model_dump()

        try:
            if self.event:
                status = await api.update_event(self.event_id, model_dump)
            else:
                status = await api.create_event(model_dump)
        except Exception as e:
            logger.exception(e)
            ui.notification(f"Sorry we ran into an error trying to save your event!")
            return

        if status.is_success:
            if not self.dialog:
                token_dialog = TokenDialog(model_dump["auth_token"])
                await token_dialog.render(on_save)
        else:
            logger.debug(f"Error: {status}")
            ui.notification(f"Sorry we ran into an error!", timeout=5)

    def close(self):
        try:
            self.dialog.close()
        except:
            pass

    async def render(self, floating=False, on_save=None, on_back=None):
        # If floating, enclose in a dialog
        if floating:
            with elements.dialog(value=True).classes("w-7/8") as dialog:
                self.dialog = dialog
                with elements.card().style("min-width: 100%"):
                    # Render the event editor (use floating=False to embed in enclosing element)
                    await self.render(on_save=on_save, on_back=on_back)
                    return

        # Load the event data
        await self.load()

        # Render forms
        self.event_name_input = elements.input("What is your event going to be called?", value=self.event.get("name", "")).classes("w-full")
        self.event_location_input = elements.input("Where is it?", value=self.event.get("location", "")).classes("w-full")

        with ui.column().classes("w-full"):
            with ui.expansion("Start Time").classes("w-full"):
                with ui.row().classes("w-full"):
                    start_time = self.event.get("start_time", datetime.now())
                    if isinstance(start_time, str):
                        start_time = datetime.fromisoformat(start_time)
                    self.start_date_input = elements.date(value=start_time.strftime("%Y-%m-%d"))
                    self.start_time_input = elements.time(value=start_time.strftime("%H:%M"))
            with ui.expansion("End Time").classes("w-full"):
                with ui.row().classes("w-full"):
                    end_time = self.event.get("end_time", datetime.now())
                    if isinstance(end_time, str):
                        end_time = datetime.fromisoformat(end_time)
                    self.end_date_input = elements.date(value=end_time.strftime("%Y-%m-%d"))
                    self.end_time_input = elements.time(value=end_time.strftime("%H:%M"))
            self.all_day_checkbox = elements.checkbox("All Day", value=self.event.get("all_day", False)).classes("w-full")

        with ui.row().classes("w-full"):
            self.description_input = elements.textarea("Description", value=self.event.get("description", "")).classes("w-full")

        with ui.column().classes("w-full justify-between items-center"):
            def call_on_back():
                if callable(on_back):
                    on_back()
            elements.button("Save", on_click=partial(self.save, on_save=on_save)).classes("w-1/3")
            elements.button("Back", on_click=call_on_back).classes("w-1/3")

    def model_dump(self):
        if not app.storage.user.get("auth_token"):
            app.storage.user["auth_token"] = str(uuid.uuid4())

        return {
            "id": str(self.event_id),
            "name": self.event_name_input.value,
            "created": datetime.now().isoformat(),
            "start_time": f"{self.start_date_input.value}T{self.start_time_input.value}:00",
            "end_time": f"{self.end_date_input.value}T{self.end_time_input.value}:00",
            "all_day": self.all_day_checkbox.value,
            "location": self.event_location_input.value,
            "description": self.description_input.value,
            "auth_token": str(app.storage.user.get("auth_token")),
        }
