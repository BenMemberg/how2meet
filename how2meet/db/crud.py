"""

"""
from sqlalchemy.orm import Session

from . import models


def get_event(db: Session, event_id: int) -> models.Event | None:
    """

    Args:
        db:
        event_id:

    Returns:

    """
    return db.query(models.Event).filter(models.Event.id == event_id).first()
