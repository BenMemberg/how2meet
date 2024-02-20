"""
Collection of How2Meet styled Quasar components
"""

from nicegui import ui

PALETTES = {"dark": "#010B13", "persian-green": "#2A9D8F", "saffron": "#E9C46A", "sandy-brown": "#F4A261", "burnt-sienna": "#E76F51"}


def button(*args, **kwargs) -> ui.button:
    return ui.button(*args, **kwargs).props("outline color=white")


def checkbox(*args, **kwargs) -> ui.checkbox:
    return ui.checkbox(*args, **kwargs).props("flat color=teal")


def input(*args, **kwargs) -> ui.input:
    return ui.input(*args, **kwargs).props("filled color=white")


def label(*args, **kwargs) -> ui.label:
    return ui.label(*args, **kwargs).props("color=white")


def card(*args, **kwargs) -> ui.card:
    return ui.card(*args, **kwargs).props("flat color=dark")


def dialog(*args, **kwargs) -> ui.dialog:
    return ui.dialog(*args, **kwargs).props("color=dark")


def textarea(*args, **kwargs) -> ui.textarea:
    return ui.textarea(*args, **kwargs).props("filled color=white")


def date(*args, **kwargs) -> ui.date:
    return ui.date(*args, **kwargs).props("minimal navigation-min-year-month=1970/01")


def time(*args, **kwargs) -> ui.time:
    return ui.time(*args, **kwargs).props("minimal color=white text-color=black")
