"""
Collection of How2Meet styled Quasar components
"""

from nicegui import ui

PALETTES = {
    "dark": "#010B13",
    "persian-green": "#2A9D8F",
    "saffron": "#E9C46A",
    "sandy-brown": "#F4A261",
    "burnt-sienna": "#E76F51"
    }

def button(*args, **kwargs):
    return ui.button(*args, **kwargs).props("outline color=white")

def checkbox(*args, **kwargs):
    return ui.checkbox(*args, **kwargs).props("flat color=white")

def input(*args, **kwargs):
    return ui.input(*args, **kwargs).props("filled color=white")

def label(*args, **kwargs):
    return ui.label(*args, **kwargs).props("color=white")

def card(*args, **kwargs):
    return ui.card(*args, **kwargs).props("flat color=dark")

def dialog(*args, **kwargs):
    return ui.dialog(*args, **kwargs).props("color=dark")

def textarea(*args, **kwargs):
    return ui.textarea(*args, **kwargs).props("filled color=white")

def date(*args, **kwargs):
    return ui.date(*args, **kwargs).props("minimal")

def time(*args, **kwargs):
    return ui.time(*args, **kwargs).props("minimal color=white text-color=black")
