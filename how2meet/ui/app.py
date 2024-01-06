"""

"""

import uuid

from nicegui import ui

# app.add_static_file(local_file="./static/css/global.css")
# ui.add_head_html("""<link rel="stylesheet" type="text/css" href="./static/css/global.css">""")
ui.add_head_html(
    "<meta name='viewport' content='width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no'>"
)
ui.add_head_html("<meta name='apple-mobile-web-app-capable' content='yes'>")
ui.add_head_html("<meta name='apple-mobile-web-app-tatus-bar-style' content='black'>")


@ui.page("/")
def main():
    with ui.header(elevated=True).classes("items-center justify-between"):
        ui.label("how2meet").classes("absolute-center").tailwind.font_size("xl")

    with ui.footer():
        ui.label("This is a footer")

    with ui.column().classes("w-full items-center"):
        with ui.row():
            ui.button("New Event", on_click=lambda: ui.open(f"/new_event/{uuid.uuid4()}"))
        with ui.row():
            ui.button("Existing Event", on_click=lambda: ui.open("/existing_event"))


@ui.page("/new_event/{event_id}")
def new_event(event_id: uuid.UUID):
    """1. Event Name
    2. Event Password
    3. Require event password from guests option [boolean] (public vs. private event)
    4. Date
    5. Number of guests limit [Optional]
    6. Photo [Optional]
    7. Description
    8. Agenda/Itinerary
    9. Guest list"""
    with ui.column().classes("w-full"):
        with ui.row().classes("w-1/2"):
            ui.input("Event Name").classes("w-full")
        with ui.row():
            ui.input("Password", password=True, password_toggle_button=True)
        with ui.row():
            with ui.expansion("Expand"):
                ui.date()
                ui.time()
        with ui.row():
            ui.input("Description")
        with ui.row().classes("w-half"):
            with ui.column():
                ui.button("Add guest", on_click=add_guest)

    ui.button("Save", on_click=lambda: ui.notify("Event details would be written to DB here"))
    ui.button("Back", on_click=lambda: ui.open("/"))


def add_guest():
    with ui.row().classes("w-full"):
        ui.input("Name").classes("w-1/3")
        ui.input("Email").classes("w-1/3")
        ui.input("Phone Number").classes("w-1/3")


@ui.page("/existing_event")
def existing_event():
    ui.input(label="Event link")
    ui.input(label="Event password [optional]")


main()
ui.run(reload=True)
