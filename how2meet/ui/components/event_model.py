from datetime import datetime

class Event:

    @property
    def duration(self):
        if not self.all_day and isinstance(self.start_time, datetime) and isinstance(self.end_time, datetime):
            return self.end_time - self.start_time
        else:
            return None

    def __init__(self, event_id):
        self.id = event_id
        self.name = ""
        self.created = datetime.now()
        self.start_time = None
        self.end_time = None
        self.all_day = False
        self.location = ""
        self.organizer_name = ""
        self.organizer_password = ""
        self.description = ""

        self.guests = []

    def __repr__(self):
        return f"Event({self.name}, {self.date})"

    def set_time_attr(self, attr, date=None, time=None):

        if isinstance(date, str):
            date = datetime.strptime(date, "%Y-%m-%d")
        elif isinstance(date, datetime):
            date = date.date()

        if isinstance(time, str):
            time = datetime.strptime(time, "%H:%M")
        elif isinstance(time, datetime):
            time = time.time()

        if date and time:
            setattr(self, attr, datetime.combine(date, time))
        elif time and isinstance(getattr(self, attr), datetime):
            setattr(self, attr, datetime.combine(getattr(self, attr).date(), time))
        elif time:
            setattr(self, attr, datetime.combine(datetime.now().date(), time))
        elif date and isinstance(getattr(self, attr), datetime):
            setattr(self, attr, datetime.combine(date, getattr(self, attr).time()))
        elif date:
            setattr(self, attr, date)
        else:
            pass

    def add_guest(self, guest):
        guest.event_id = self.id
        self.guests.append(guest)

    async def save(self, url):
        import httpx
        from ...db.schemas import EventCreate

        self.created = datetime.now()
        event = EventCreate(**self.__dict__).model_dump_json()
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=event)
            response.raise_for_status()

class Guest:

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        if isinstance(value, str):
            self._phone = int(value.replace('-', '').replace('(', '').replace(')', ''))
        else:
            self._phone = value

    def __init__(self, id, name = None, email = None, phone = None):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.status = ""
        self.password = None
        self.verified = False
        self.event_id = None

    def __repr__(self):
        return f"Invite(name='{self.name}', contact='{self.email if self.email else self.phone}')"
