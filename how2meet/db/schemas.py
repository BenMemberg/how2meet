"""
Schemas declarations used for Pydantic/FastAPI to do data validation on API calls. These follow the tables declared
in the models.py file, but don't necessarily have to correspond 1:1. It may be advantageous to remove unused fields
from these schemas depending on how the API is to be used.

FastAPI Tutorial: https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-pydantic-models
"""
from datetime import date, datetime

from pydantic import BaseModel


class Event(BaseModel):
    id: int
    name: str
    date: date
    start_time: datetime
    end_time: datetime
    all_day: bool
    location: str
    organizer_name: str
    organizer_password: str
    duration: int

    class Config:
        orm_mode = True


class EventCreate(Event):
    pass


class Invite(BaseModel):
    id: int
    name: str
    email: str
    phone: int
    status: str
    password: int
    verified: bool
    event_id: int

    class Config:
        orm_mode = True


class InviteCreate(Invite):
    pass
