from contextlib import contextmanager

from nicegui import ui


@contextmanager
def frame(navtitle: str):
    """Custom page frame to share the same styling and behavior across all pages"""
    with ui.header().classes("justify-between text-white items-center"):
        ui.link("How2Meet", "/").classes("no-underline font-bold text-white")
        ui.label(navtitle)
        ui.button(on_click=lambda: right_drawer.toggle()).props("flat color=white icon=menu")

    with ui.right_drawer().classes("gap-0 m-0 p-0") as right_drawer:
        with ui.row().classes("w-full gap-0"):
            header_links = {
                "Home": "/",
                "Events": "/events",
                "Settings": "/settings",
            }
            for link_text, link_target in header_links.items():
                with ui.card().on("click", lambda link_target=link_target: ui.open(link_target)).classes(
                    "w-full no-shadow border-b-[1px] rounded-none hover:bg-gray-200"
                ).style("cursor: pointer"):
                    ui.link(link_text, link_target).classes("w-full text-left no-underline font-bold")

    with ui.footer().classes("justify-between text-white flex items-center"):
        with ui.row().classes("flex-grow"):
            ui.link("Donate", "https://www.buymeacoffee.com/").classes("text-white mr-4")
            ui.link("GitHub", "https://www.github.com/BenMemberg/how2meet").classes("text-white mr-4")
        # put a settings icon on the far right of the footer
        ui.button(on_click=lambda: ui.open("/settings")).props("flat color=white icon=settings")

    yield
