"""
Models used to store data in the database via the SQLAlchemy ORM.

FastAPI Tutorial: https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-database-models

'SQLAlchemy uses the term "model" to refer to these classes and instances that interact with the database.
But Pydantic also uses the term "model" to refer to something different, the data validation, conversion,
and documentation classes and instances.'

"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import DateTime

from .database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(150))
    created = Column(String(100))
    start_time = Column(String(100))
    end_time = Column(String(100))
    all_day = Column(Boolean)
    location = Column(String(150))
    organizer_name = Column(String(50))
    organizer_password = Column(String(100))
    description = Column(String(500))
    guests = relationship("Guest", primaryjoin="Event.id == Guest.event_id", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Event({self.name}, {self.date})"


class Guest(Base):
    __tablename__ = "guests"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), nullable=True)
    phone = Column(Integer(), nullable=True)
    status = Column(String(15))
    event_id = Column(String(36), ForeignKey("events.id"), nullable=False)

    def __repr__(self):
        return f"Guest(name='{self.name}', contact='{self.email if self.email else self.phone}')"
