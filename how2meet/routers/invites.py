from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import crud, models, schemas
from ..db.database import engine, get_db

router = APIRouter(
    prefix="/invites",
    tags=["invites"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=list[schemas.Invite])
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

# TODO: Add a route to create an invite
