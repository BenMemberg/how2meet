"""

"""
from datetime import date, datetime

from pydantic import BaseModel


class Event(BaseModel):
    """"""

    id: int
    name: str
    date: date
    start_time: datetime
    end_time: datetime
    all_day: bool
    locatiom: str
    host_name: str
    host_password: str
    duration: int

    class Config:
        orm_mode = True


class Invite(BaseModel):
    """"""

    id: int
    name: str
    email: str
    phone: int
    status: str
    password: int
    verified: bool

    class Config:
        orm_mode = True
