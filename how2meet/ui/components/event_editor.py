from datetime import datetime
import uuid

from nicegui import ui

from how2meet.utils import APIClient as api
from how2meet.ui.pages.urls import URL_EVENTS, URL_NEW_EVENT, URL_EVENT_HOME

class InviteEditor:

        def __init__(self, invite_id: str):
            self.invite_id = invite_id
            self.invite = None

        async def load(self):
            # self.invite = await api.get_invite(self.invite_id)
            pass

        async def delete(self):
            self.card.delete()

        async def render(self):
            # TODO add method to remove guest
            with ui.card().classes("flex-grow position:relative") as card:
                self.card = card
                with ui.row().classes("flex-grow justify-between items-center"):
                    self.name_input = ui.input("Name")
                    self.email_input = ui.input("Email")
                    self.phone_input = ui.input("Phone Number")
                    ui.button("", icon="delete", color="red", on_click=self.delete).classes("w-6 h-6")


        def model_dump(self):
            return {
                "id": self.invite_id,
                "name": self.name_input.value,
                "email": self.email_input.value,
                "phone": self.phone_input.value,
                "status": self.status_input.value,
                "password": self.password_input.value,
                "verified": self.verified_input.value,
                "event_id": self.event_id_input.value,
            }

class EventEditor:

    def __init__(self, event_id=None):
        self.event_id = event_id or str(uuid.uuid4())
        self.event = {}
        self.invites = []

    async def load(self):
        self.event = await api.get_event(self.event_id)

    async def save(self):
        event_dict = await self.model_dump()
        status = await api.create_event(event_dict)
        if status == 200:
            ui.open(URL_EVENT_HOME.format(event_id=self.event_id))
        else:
            ui.notification(f"Error: {status}", timeout=5)

    async def add_guest(self):
        invite_id = uuid.uuid4()
        invite_editor = InviteEditor(invite_id)
        self.invites.append(invite_editor)
        await invite_editor.load()
        await invite_editor.render()

    async def render(self):
        await self.load()
        with ui.row().classes("flex-grow justify-between"):
            self.event_name_input = ui.input("Event Name", value=self.event.get("name", ""))
            self.event_location_input = ui.input("Location", value=self.event.get("location", ""))
            with ui.row():
                self.user_input = ui.input("User", value=self.event.get("organizer_name", ""))
                self.password_input = ui.input("Password", password=True, password_toggle_button=True)
            with ui.row():
                with ui.expansion("Start Time"):

                    self.start_date_input = ui.date(value=self.event.get("start_time", datetime.now().date()).strftime("%Y-%m-%d"))
                    self.start_time_input = ui.time(value=self.event.get("start_time", datetime.now().time()).strftime("%H:%M"))
                with ui.expansion("End Time"):
                    self.end_date_input = ui.date(value=self.event.get("end_time", datetime.now().date()).strftime("%Y-%m-%d"))
                    self.end_time_input = ui.time(value=self.event.get("end_time", datetime.now().time()).strftime("%H:%M"))
                self.all_day_checkbox = ui.checkbox("All Day", value=self.event.get("all_day", False))
            with ui.row().classes("w-full"):
                self.description_input = ui.textarea("Description", value=self.event.get("description", "")).classes("w-full")
            with ui.row().classes("w-full"):
                with ui.column().classes("w-full"):
                    self.add_guest_button = ui.button("Add guest", on_click=self.add_guest)

        # TODO: Post invites to API
        save_button = ui.button("Save", on_click=self.save)
        back_button = ui.button("Back", on_click=lambda: ui.open("/"))

    async def model_dump(self):
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
