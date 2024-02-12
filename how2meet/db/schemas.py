"""
Schemas declarations used for Pydantic/FastAPI to do data validation on API calls. These follow the tables declared
in the models.py file, but don't necessarily have to correspond 1:1. It may be advantageous to remove unused fields
from these schemas depending on how the API is to be used.

FastAPI Tutorial: https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-pydantic-models
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


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


class EventUpdate(Event):
    id: Optional[str] = Field(default=None, description="The ID of the event")
    name: Optional[str] = Field(default=None, description="The name of the event")
    created: Optional[datetime] = Field(default=None, description="The creation datetime of the event")
    start_time: Optional[datetime] = Field(default=None, description="The start datetime of the event")
    end_time: Optional[datetime] = Field(default=None, description="The end datetime of the event")
    all_day: Optional[bool] = Field(default=None, description="Whether the event lasts all day")
    location: Optional[str] = Field(default=None, description="The location of the event")
    organizer_name: Optional[str] = Field(default=None, description="The name of the event organizer")
    organizer_password: Optional[str] = Field(default=None, description="The password of the event organizer")
    description: Optional[str] = Field(default=None, description="The description of the event")


class Guest(BaseModel):
    id: str
    name: str
    email: str
    phone: int
    status: str
    event_id: str

    class Config:
        from_attributes = True


class GuestCreate(Guest):
    pass


class GuestUpdate(Guest):
    id: Optional[str] = Field(default=None, description="The ID of the guest")
    name: Optional[str] = Field(default=None, description="The name of the guest")
    email: Optional[str] = Field(default=None, description="The email of the guest")
    phone: Optional[int] = Field(default=None, description="The phone number of the guest")
    status: Optional[str] = Field(default=None, description="The status of the guest")
    event_id: Optional[str] = Field(default=None, description="The event ID of the guest")
