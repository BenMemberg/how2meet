#!/usr/bin/env python3
"""
Main entrypoint
"""
from fastapi import Depends, FastAPI, HTTPException
from nicegui import ui
from sqlalchemy.orm import Session

from .db import crud, models, schemas
from .db.database import engine, get_db
from .ui import frontend

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/events/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    """
    Create an event.

    Parameters:
        event (schemas.EventCreate): The event to be created.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        schemas.Event: The created event.
    """
    db_event = crud.get_event(db, event_id=event.id)
    if db_event:
        raise HTTPException(status_code=400, detail="Event already registered")
    else:
        db_event = crud.create_event(db, event)
    return db_event


@app.get("/events/", response_model=list[schemas.Event])
def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves a list of events from the database.

    Args:
        skip (int): The number of events to skip. Defaults to 0.
        limit (int): The maximum number of events to retrieve. Defaults to 100.
        db (Session): The database session to use.

    Returns:
        List[Event]: A list of events retrieved from the database.
    """
    events = crud.get_events(db, skip=skip, limit=limit)

    with ui.column():
        ui.label("Events")
    return events


@app.get("/events/{event_id}", response_model=schemas.Event)
def read_event(event_id: int, db: Session = Depends(get_db)):
    """
    Retrieves an event from the database.

    Args:
        event_id (int): The ID of the event to retrieve.
        db (Session): The database session to use.

    Returns:
        Event: The event retrieved from the database.
    """
    db_event = crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@app.post("/events/{event_id}/invites/", response_model=schemas.Invite)
def create_invite_for_event(event_id: int, invite: schemas.InviteCreate, db: Session = Depends(get_db)):
    """
    Create an invite for an event.

    Args:
        event_id (int): The ID of the event to invite to.
        invite (InviteCreate): The invite data to create.
        db (Session): The database session to use.

    Returns:
        Invite: The created invite.
    """
    db_event = crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    db_invite = crud.get_invite(db, user_id=invite.user_id)
    if db_invite:
        raise HTTPException(status_code=400, detail="Invite already registered")
    else:
        db_invite = crud.create_invite(db, invite)  # TODO figure out where logic to handle event_id belongs
    return db_invite


@app.get("/invites/", response_model=list[schemas.Invite])
def read_invites(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves a list of invites from the database.

    Args:
        skip (int): The number of invites to skip. Defaults to 0.
        limit (int): The maximum number of invites to retrieve. Defaults to 100.
        db (Session): The database session to use.

    Returns:
        List[Invite]: A list of invites retrieved from the database.
    """
    invites = crud.get_invites(db, skip=skip, limit=limit)
    return invites


@app.get("/")
def read_root():
    return {"Hello": "World"}

app = FastAPI()

frontend.init(app)


if __name__ == "__main__":
    print('Please start the app with the "uvicorn" command as shown in the start.sh script')
