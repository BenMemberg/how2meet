from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date, DateTime

from .database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150))
    date = Column(Date)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    all_day = Column(bool)
    locatiom = Column(String(150))
    host_name = Column(String(50))
    host_password = Column(String(100))
    duration = Column(Integer)
    invites = relationship("Invite", primaryjoin="Event.id == Invite.store_id", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Event({self.name}, {self.date})"


class Invite(Base):
    __tablename__ = "invites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), nullable=True)
    phone = Column(Integer(10), nullable=True)
    status = Column(String(15))
    password = Column(Integer, nullable=True)
    verified = Column(bool, nullable=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    def __repr__(self):
        return f"Invite(name='{self.name}', contact='{self.email if self.email else self.phone}')"
