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

models.Base.metadata.create_all(bind=engine)

app = FastAPI(prefix="/api")
app.include_router(events.router)
app.include_router(invites.router)
frontend.init(app)

if __name__ == "__main__":
    print('Please start the app with the "uvicorn" command as shown in the start.sh script')
