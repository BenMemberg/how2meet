"""
Models used to store data in the database via the SQLAlchemy ORM.

FastAPI Tutorial: https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-database-models

'SQLAlchemy uses the term "model" to refer to these classes and instances that interact with the database.
But Pydantic also uses the term "model" to refer to something different, the data validation, conversion,
and documentation classes and instances.'

"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date, DateTime

from .database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(String(32), primary_key=True, index=True)
    name = Column(String(150))
    created = Column(DateTime)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    all_day = Column(Boolean)
    location = Column(String(150))
    organizer_name = Column(String(50))
    organizer_password = Column(String(100))
    invites = relationship("Invite", primaryjoin="Event.id == Invite.event_id", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Event({self.name}, {self.date})"


class Invite(Base):
    __tablename__ = "invites"

    id = Column(String(32), primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), nullable=True)
    phone = Column(Integer(), nullable=True)
    status = Column(String(15))
    password = Column(Integer, nullable=True)
    verified = Column(Boolean, nullable=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    def __repr__(self):
        return f"Invite(name='{self.name}', contact='{self.email if self.email else self.phone}')"
