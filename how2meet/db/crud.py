"""
Basic CRUD operations for adding, updating, and deleting events and invites.
"""
from sqlalchemy.orm import Session

from . import models, schemas

### EVENT CRUD OPS ###


def get_event(db: Session, event_id: str) -> models.Event | None:
    """
    Get an event by ID.
    Args:
        db: The database session.
        event_id:The ID of the event to retrieve.

    Returns: models.Event | None: The event with the specified ID if found, or None if not found.

    TODO: Use structural pattern matching to make generic get_event() that can take other search parameters
    """
    return db.query(models.Event).filter(models.Event.id == event_id).first()


def get_events(db: Session, skip: int = 0, limit: int = 100) -> list[models.Event]:
    """
    Get a list of events.
    Args:
        db: The database session.
        skip: The number of events to skip.
        limit: The maximum number of events to retrieve.

    Returns: list[models.Event]: A list of events.

    """
    return db.query(models.Event).offset(skip).limit(limit).all()


def create_event(db: Session, event: schemas.EventCreate) -> models.Event:
    """
    Create a new event.
    Args:
        db: Database session
        event: Event data

    Returns:
        Created event

    """
    db_event = models.Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def update_event(db: Session, db_event: models.Event, updated_event: schemas.EventUpdate) -> models.Event:
    """
    Update an event in the database.

    Args:
        db: Database session
        db_event: Event to be updated
        updated_event: Updated event data

    Returns:
        Updated event
    """

    for attr, value in updated_event.model_dump().items():
        # TODO: maybe bug later
        if value is not None:
            setattr(db_event, attr, value)
    db.commit()
    db.refresh(db_event)
    return db_event


### GUEST CRUD OPS ###


def get_guests_from_event(db: Session, event_id: str) -> list[models.Guest] | None:
    """Return all guests for a specific event"""
    return db.query(models.Guest).filter(models.Guest.event_id == event_id).all()


def get_guest_from_event(db: Session, event_id: str, guest_id: str) -> models.Guest | None:
    """Return a specific guest for a specific event"""
    return db.query(models.Guest).filter(models.Guest.event_id == event_id, models.Guest.id == guest_id).first()


def create_guest(db: Session, guest: schemas.GuestCreate) -> models.Guest:
    """Create a new guest. Assumes that the event exists and the guest arg contains the appropriate ID"""
    db_guest = models.Guest(**guest.model_dump())
    db.add(db_guest)
    db.commit()
    db.refresh(db_guest)
    return db_guest


def update_guest(db: Session, db_guest: models.Guest, updated_guest: schemas.GuestUpdate) -> models.Guest:
    """Overwrite guest data if it exists"""
    for attr, value in updated_guest.model_dump().items():
        if value is not None:
            setattr(db_guest, attr, value)
    db.commit()
    db.refresh(db_guest)
    return db_guest


# TODO: remove/rethink how we interact with invites. moving to Guests instead. Leaving here for posterity
# def get_invite(db: Session, user_id: str) -> models.Invite | None:
#     """
#     Retrieve an invite from the database based on the given user ID.
#
#     Parameters:
#         db (Session): The database session object.
#         user_id (int): The ID of the user.
#
#     Returns:
#         models.Invite | None: The invite object if found, None otherwise.
#     """
#     return db.query(models.Invite).filter(models.Invite.id == user_id).first()
#
#
# def create_invite(db: Session, invite: schemas.InviteCreate) -> models.Invite:
#     """
#     Create a new invite.
#     Args:
#         db: Database session
#         invite: Invite data
#
#     Returns:
#         Created invite
#     """
#     db_invite = models.Invite(invite.model_dump())
#     db.add(db_invite)
#     db.commit()
#     db.refresh(db_invite)
#     return db_invite
#
#
# def get_invites(db: Session, skip: int = 0, limit: int = 100) -> list[models.Invite]:
#     """
#     Get a list of invites.
#     Args:
#         db: The database session.
#         skip: The number of invites to skip.
#         limit: The maximum number of invites to retrieve.
#
#     Returns: list[models.Invite]: A list of invites.
#
#     """
#     return db.query(models.Invite).offset(skip).limit(limit).all()
