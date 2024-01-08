#!/usr/bin/env python3
"""
Main entrypoint
"""
import os, logging

from fastapi import Depends, FastAPI, HTTPException
from nicegui import ui
from sqlalchemy.orm import Session

from .db import crud, models, schemas
from .db.database import engine, get_db
from .ui import frontend
from .routers import events, invites

BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

api_app = FastAPI(openapi_url="/v1/openapi.json",
                  docs_url="/v1/docs",
                  redoc_url="/v1/redoc",
                  )
api_app.include_router(events.router)
api_app.include_router(invites.router)
app.mount("/api", api_app)
frontend.init(app)

if __name__ == "__main__":
    print('Please start the app with the "uvicorn" command as shown in the start.sh script')
