"""

"""

from nicegui import app, ui

app.add_static_file(local_file="../assets/css/global.css")
ui.add_head_html("""<link rel="stylesheet" type="text/css" href="../assets/css/global.css">""")


@ui.page("/")
def main():
    with ui.header(elevated=True).classes("items-center justify-between"):
        ui.label("how2meet").classes("absolute-center").tailwind.font_size("xl")

    with ui.footer():
        ui.label("This is a footer")

    with ui.column().classes("w-full items-center"):
        with ui.row():
            ui.button("New Event", on_click=lambda: ui.open("/new_event"))
        with ui.row():
            ui.button("Existing Event", on_click=lambda: ui.open("/existing_event"))


@ui.page("/new_event")
def new_event():
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
        with ui.row():
            ui.input("Event Name")
        with ui.row():
            ui.input("Password", password=True, password_toggle_button=True)
        with ui.row():
            ui.date()
            ui.time()
        with ui.row():
            ui.input("Description")
        with ui.row().classes("w-half"):
            global col
            col = ui.column()
            ui.button("Add guest", on_click=add_guest)

    ui.button("Save")


def add_guest():
    with col:
        with ui.row():
            ui.input("Name")
            ui.input("Email")
            ui.input("Phone Number")


@ui.page("/existing_event")
def existing_event():
    ui.input(label="Event link")
    ui.input(label="Event password [optional]")


main()
ui.run(reload=True)
