"""
Schemas declarations used for Pydantic/FastAPI to do data validation on API calls. These follow the tables declared
in the models.py file, but don't necessarily have to correspond 1:1. It may be advantageous to remove unused fields
from these schemas depending on how the API is to be used.

FastAPI Tutorial: https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-pydantic-models
"""
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

"""
Events schemas
"""


class Event(BaseModel):
    id: uuid.UUID
    name: str
    organizer: str
    email: str
    created: datetime
    start_time: datetime
    end_time: datetime
    all_day: bool
    location: str
    description: str

    class Config:
        from_attributes = True


class EventCreate(Event):
    id: Optional[uuid.UUID] = Field(default=None, description="The ID of the event")
    event_password: Optional[str] = Field(default=None, description="The password of the event")


class EventUpdate(Event):
    id: Optional[uuid.UUID] = Field(default=None, description="The ID of the event")
    name: Optional[str] = Field(default=None, description="The name of the event")
    organizer: Optional[str] = Field(default=None, description="The organizer of the event")
    email: Optional[str] = Field(default=None, description="The email of the event")
    created: Optional[datetime] = Field(default=None, description="The creation datetime of the event")
    start_time: Optional[datetime] = Field(default=None, description="The start datetime of the event")
    end_time: Optional[datetime] = Field(default=None, description="The end datetime of the event")
    all_day: Optional[bool] = Field(default=None, description="Whether the event lasts all day")
    location: Optional[str] = Field(default=None, description="The location of the event")
    description: Optional[str] = Field(default=None, description="The description of the event")
    event_password: Optional[str] = Field(default=None, description="The password of the event")


class EventDelete(BaseModel):
    event_password: str


"""
Guests schemas
"""


class Guest(BaseModel):
    id: str
    name: str
    email: Optional[str] = Field(default="", description="The email of the guest")
    phone: Optional[str] = Field(default="", description="The phone number of the guest")
    status: str
    event_id: uuid.UUID

    class Config:
        from_attributes = True


class GuestCreate(Guest):
    pass


class GuestUpdate(Guest):
    name: Optional[str] = Field(default=None, description="The name of the guest")
    status: Optional[str] = Field(default=None, description="The status of the guest")
    event_id: Optional[uuid.UUID] = Field(default=None, description="The event ID of the guest")
