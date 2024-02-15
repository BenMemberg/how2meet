from contextlib import contextmanager
from pathlib import Path

from nicegui import ui, context

from how2meet.ui.components import elements
from how2meet.ui.pages.urls import ROUTE_BASE, URL_EVENTS, URL_SETTINGS


def frame():
    """Custom page frame to share the same styling and behavior across all pages"""
    HEADER_HTML = (Path(__file__).parent / ".." / 'static' / 'header.html').read_text()
    STYLE_CSS = (Path(__file__).parent / ".." / 'static' / 'global.css').read_text()
    ui.add_head_html(HEADER_HTML + f'<style>{STYLE_CSS}</style>')

    ui.dark_mode(True)

    with ui.header() \
            .classes('items-center justify-between duration-200 p-0 px-4') \
            .style('box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1)'):
        ui.link("How2Meet", ROUTE_BASE).classes("no-underline font-bold text-teal-500 text-xl")
        elements.button(on_click=lambda: right_drawer.toggle()).props("flat color=white icon=menu")

    with ui.right_drawer().classes("gap-0 m-0 p-0 bg-neutral-900") as right_drawer:
        with ui.row().classes("w-full gap-0"):
            header_links = {
                "Home": ROUTE_BASE,
                # "Events": URL_EVENTS,
                "Settings": URL_SETTINGS,
            }
            for link_text, link_target in header_links.items():
                with elements.card().on("click", lambda link_target=link_target: ui.open(link_target)).classes(
                    "w-full no-shadow border-b-[1px] rounded-none hover:bg-gray-800"
                ).style("cursor: pointer"):
                    ui.link(link_text, link_target).classes("w-full text-left no-underline font-bold")

    with ui.footer(fixed=False).classes("items-center justify-between p-0 px-4") as footer:
        with ui.row().classes("flex-grow"):
            ui.link("Donate", "https://www.buymeacoffee.com/").classes("text-white mr-4")
            ui.link("GitHub", "https://www.github.com/BenMemberg/how2meet").classes("text-white mr-4")
        # put a settings icon on the far right of the footer
        elements.button(on_click=lambda: ui.open(URL_SETTINGS)).props("flat color=white icon=settings")
