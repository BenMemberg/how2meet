"""
API routes for events. All routes are prefixed with `api/events/` per the router instantiation and mounting the api_app in main.py
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import crud, models, schemas
from ..db.database import get_db

router = APIRouter(prefix="/events", tags=["events"], responses={404: {"description": "Not found"}})


@router.post("/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)) -> models.Event:
    """
    API route to create an event.

    Parameters:
        event: The event to be created.
        db: The database session. Defaults to Depends(get_db).

    Returns:
        models.Event: The created event.
    """
    db_event = crud.get_event(db, event_id=event.id)
    if db_event:
        raise HTTPException(status_code=400, detail="Event already registered")
    else:
        db_event = crud.create_event(db, event)
    return db_event


@router.get("/", response_model=list[schemas.Event])
def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[models.Event]:
    """
    API route to retrieve a list of events from the database.

    Args:
        skip: The number of events to skip. Defaults to 0.
        limit: The maximum number of events to retrieve. Defaults to 100.
        db: The database session to use.

    Returns:
        List[models.Event]: A list of events retrieved from the database.
    """
    events = crud.get_events(db, skip=skip, limit=limit)
    return events


@router.get("/{event_id}", response_model=schemas.Event)
def read_event(event_id: str, db: Session = Depends(get_db)) -> models.Event:
    """
    API route to retrieve an event from the database.

    Args:
        event_id: The ID of the event to retrieve.
        db: The database session to use.

    Returns:
        models.Event: The event retrieved from the database.
    """
    db_event = crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@router.delete("/{event_id}", response_model=schemas.Event)
def delete_event(event_id: str, db: Session = Depends(get_db)) -> models.Event:
    """
    API route to delete an event from the database

    Args:
        event_id: The ID of the event to delete.
        db: The database session to use.

    Returns:
        models.Event: The event that was deleted.
    """
    db_event = crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    db.delete(db_event)
    db.commit()
    return db_event


@router.put("/{event_id}", response_model=schemas.Event)
def update_event(event_id: str, updated_event: schemas.EventUpdate, db: Session = Depends(get_db)) -> models.Event:
    """
    API router to update an existing event in the database.

    Args:
        event_id: The ID of the event to update.
        updated_event: The updated event data
        db: The database session.

    Returns:
        models.Event: The updated event.
    """
    db_event = crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    updated_event = crud.update_event(db, db_event, updated_event)
    return updated_event
