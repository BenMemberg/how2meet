"""
Models used to store data in the database via the SQLAlchemy ORM.

FastAPI Tutorial: https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-database-models

'SQLAlchemy uses the term "model" to refer to these classes and instances that interact with the database.
But Pydantic also uses the term "model" to refer to something different, the data validation, conversion,
and documentation classes and instances.'

"""
from uuid import uuid4

from sqlalchemy import Boolean, Column, ForeignKey, String, Uuid
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.types import DateTime

Base = declarative_base()


class Event(Base):
    __tablename__ = "events"

    id = Column(Uuid, primary_key=True, index=True, default=uuid4)
    name = Column(String(150), nullable=False)
    organizer = Column(String(100))
    email = Column(String(100))  # TODO: Add email validation?
    created = Column(DateTime)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    all_day = Column(Boolean)
    location = Column(String(150))
    description = Column(String(500))
    event_password = Column(String(100))
    guests = relationship("Guest", primaryjoin="Event.id == Guest.event_id", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Event({self.name}, {self.date})"


class Guest(Base):
    __tablename__ = "guests"

    id = Column(Uuid, primary_key=True, index=True, default=uuid4)
    name = Column(String(100))
    email = Column(String(100), nullable=True)
    phone = Column(String(15), nullable=True)
    status = Column(String(16), nullable=False)
    event_id = Column(Uuid, ForeignKey("events.id"), nullable=False)

    def __repr__(self):
        return f"Guest(name='{self.name}', contact='{self.email if self.email else self.phone}')"
