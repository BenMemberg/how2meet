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
    organizer_name:str
    organizer_password: str
    duration: int

    class Config:
        orm_mode = True


class Invite(BaseModel):
    id: int
    name: str
    email: str
    phone: int
    status: str
    password: int
    verified: bool

    class Config:
        orm_mode = True
