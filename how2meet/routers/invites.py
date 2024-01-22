from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import crud, schemas
from ..db.database import get_db

router = APIRouter(prefix="/invites", tags=["invites"], responses={404: {"description": "Not found"}})


@router.get("/", response_model=list[schemas.Invite])
def read_invites(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[schemas.Invite]:
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


@router.post("/", response_model=schemas.Invite)
def create_invite(invite: schemas.InviteCreate, db: Session = Depends(get_db)) -> schemas.Invite:
    """
    Create an invite for an event.

    Args:
        invite (InviteCreate): The invite data to create.
        db (Session): The database session to use.

    Returns:
        Invite: The created invite.
    """
    db_invite = crud.get_invite(db, user_id=invite.user_id)
    if db_invite:
        raise HTTPException(status_code=400, detail="Invite already registered")
    else:
        db_invite = crud.create_invite(db, invite)
    return db_invite
