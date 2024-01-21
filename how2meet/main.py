#!/usr/bin/env python3
"""
Main entrypoint
"""
import logging
import os

from fastapi import FastAPI

from .db import models
from .db.database import engine
from .routers import events, invites
from .ui import frontend

models.Base.metadata.create_all(bind=engine)

# Create app
app = FastAPI()

# Mount the API at /api and add the routers
api_app = FastAPI(
    openapi_url="/v1/openapi.json",
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
)
api_app.include_router(events.router)
api_app.include_router(invites.router)
app.mount("/api", api_app)

# Mount the frontend at the root path
# NOTE: If this is mounted before the API, the API will not be accessible
frontend.init(app)

if __name__ == "__main__":
    print('Please start the app with the "uvicorn" command as shown in the start.sh script')
