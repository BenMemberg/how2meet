"""
API routes for events. All routes are prefixed with `api/events/` per the router instantiation and mounting the api_app in main.py
"""
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import crud, models, schemas
from ..db.database import get_db

router = APIRouter(prefix="/events", tags=["events"], responses={404: {"description": "Not found"}})

"""
Event routers
"""

@router.post("/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)) -> models.Event:
    """
    API route to create an event.

    Args:
        event: The event to be created.
        db: The database session. Defaults to Depends(get_db).

    Returns:
        models.Event: The created event.
    """
    # event.id = uuid.UUID(event.id)
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
def read_event(event_id: uuid.UUID, db: Session = Depends(get_db)) -> models.Event:
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
def delete_event(event_id: uuid.UUID, db: Session = Depends(get_db)) -> models.Event:
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
def update_event(event_id: uuid.UUID, updated_event: schemas.EventUpdate, db: Session = Depends(get_db)) -> models.Event:
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
    db_event.id = uuid.UUID(db_event.id)
    updated_event = crud.update_event(db, db_event, updated_event)
    return updated_event

"""
Guests routers
"""

@router.get("/{event_id}/guests", response_model=list[schemas.Guest])
def get_guests(event_id: uuid.UUID, db: Session = Depends(get_db)) -> list[schemas.Guest]:
    """
    API route to get all guests for an event.

    Args:
        event_id: The ID of the event.
        db: The database session.

    Returns:
        list[schemas.Guest]: A list of all guests.
    """
    guests = crud.get_guests_from_event(db, event_id)
    return guests


@router.get("/{event_id}/guests/{guest_id}", response_model=schemas.Guest)
def get_guest(event_id: uuid.UUID, guest_id: str, db: Session = Depends(get_db)) -> schemas.Guest:
    """
    API route to get a guest for an event.

    Args:
        event_id: The ID of the event.
        guest_id: The ID of the guest.
        db: The database session.

    Returns:
        schemas.Guest: A guest.
    """
    guest = crud.get_guest_from_event(db, event_id, guest_id)
    return guest


@router.post("/{event_id}/guests", response_model=schemas.Guest)
def create_guest(event_id: uuid.UUID, guest: schemas.GuestCreate, db: Session = Depends(get_db)) -> schemas.Guest:
    """
    API route to create a guest for an event.

    Args:
        event_id: The ID of the event.
        guest: The guest data.
        db: The database session.

    Returns:
        schemas.Guest: The newly created guest.
    """
    guest.event_id = event_id
    db_guest = crud.create_guest(db, guest)
    return db_guest


@router.delete("/{event_id}/guests/{guest_id}", response_model=schemas.Guest)
def delete_guest(event_id: uuid.UUID, guest_id: str, db: Session = Depends(get_db)) -> schemas.Guest:
    """
    API route to delete a guest for an event.

    Args:
        event_id: The ID of the event.
        guest_id: The ID of the guest.
        db: The database session.

    Returns:
        schemas.Guest: The deleted guest. # TODO: Maybe it doesn't make sense to return a deleted object
    """
    db_guest = crud.get_guest_from_event(db, event_id, guest_id)
    if db_guest is None:
        raise HTTPException(status_code=404, detail="Guest not found")
    db.delete(db_guest)
    db.commit()
    return db_guest


@router.put("/{event_id}/guests/{guest_id}", response_model=schemas.Guest)
def update_guest(event_id: uuid.UUID, guest_id: str, guest_update: schemas.GuestUpdate, db: Session = Depends(get_db)) -> schemas.Guest:
    """
    API route to update a guest for an event.

    Args:
        event_id: The ID of the event.
        guest_id: The ID of the guest.
        updated_guest: The new guest data.
        db: The database session.

    Returns:
        schemas.Guest: A guest.
    """
    db_guest = crud.get_guest_from_event(db, event_id, guest_id)
    if db_guest is None:
        raise HTTPException(status_code=404, detail="Guest not found")
    db_guest = crud.update_guest(db, db_guest, guest_update)
    return db_guest
