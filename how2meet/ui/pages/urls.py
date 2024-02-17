import os
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
ROUTE_PREFIX_EVENTS = "/events"
ROUTE_BASE = "/"
ROUTE_NEW_EVENT = "/create"
ROUTE_EVENT_HOME = "/home/{event_id}"

URL_EVENTS = ROUTE_PREFIX_EVENTS + ROUTE_BASE
URL_NEW_EVENT = ROUTE_PREFIX_EVENTS + ROUTE_NEW_EVENT
URL_EVENT_HOME = ROUTE_PREFIX_EVENTS + ROUTE_EVENT_HOME
URL_SETTINGS = "/settings"
