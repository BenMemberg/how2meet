"""
Schemas declarations used for Pydantic/FastAPI to do data validation on API calls. These follow the tables declared
in the models.py file, but don't necessarily have to correspond 1:1. It may be advantageous to remove unused fields
from these schemas depending on how the API is to be used.

FastAPI Tutorial: https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-pydantic-models
"""
from datetime import datetime

from pydantic import BaseModel


class Event(BaseModel):
    id: str
    name: str
    created: datetime
    start_time: datetime
    end_time: datetime
    all_day: bool
    location: str
    organizer_name: str
    organizer_password: str
    description: str

    class Config:
        from_attributes = True


class EventCreate(Event):
    pass


class Invite(BaseModel):
    id: str
    name: str
    email: str
    phone: int
    status: str
    password: int
    verified: bool
    event_id: int

    class Config:
        from_attributes = True


class InviteCreate(Invite):
    pass
