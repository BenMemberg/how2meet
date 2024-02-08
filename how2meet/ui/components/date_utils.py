from datetime import datetime
from typing import Any, Dict

UNK_DATE = "Someday"
UNK_TIME = "Sometime"
UNK_All = "Figuring it out..."
DATE_FORMAT = "%A, %B %d{ord}, %Y"
TIME_FORMAT = "%I:%M"
TIME_FORMAT_W_AMPM = TIME_FORMAT + " %p"
SAME_DAY_FORMAT = "{start_date}"
DIFFERENT_DAY_FORMAT = "{start_date} - {end_date}"

def ordinal(n):
    return "%s" % ("tsnrhtdd"[((n//10%10!=1)*(n%10<4)*n%10)::4])

def event_dates_to_str(event: Dict[str, Any]) -> str:
    if event.get("start_time"):
        start_time = datetime.fromisoformat(event["start_time"])
    if event.get("end_time"):
        end_time = datetime.fromisoformat(event["end_time"])
    else:
        end_time = None

    if event.get("all_day"):
        return start_time.strftime(DATE_FORMAT.format(ord=ordinal(int(start_time.strftime("%d")))))

    #Wednesday, January 24th, 2024th
    if start_time and end_time and start_time.date() == end_time.date():
        return SAME_DAY_FORMAT.format(
            start_date=start_time.strftime(DATE_FORMAT.format(ord=ordinal(int(start_time.strftime("%d")))))
        )
    elif start_time and end_time:
        return DIFFERENT_DAY_FORMAT.format(
            start_date=start_time.strftime(DATE_FORMAT).replace(start_time.strftime("%d"), ordinal(int(start_time.strftime("%d")))),
            end_date=end_time.strftime(DATE_FORMAT).replace(end_time.strftime("%d"), ordinal(int(end_time.strftime("%d"))))
        )
    elif start_time and not end_time:
        return SAME_DAY_FORMAT.format(
            start_date=start_time.strftime(DATE_FORMAT).replace(start_time.strftime("%d"), ordinal(int(start_time.strftime("%d")))),
            end_date=UNK_DATE
        )
    else:
        return UNK_All

def event_times_to_str(event: Dict[str, Any]) -> str:
    if event.get("start_time"):
        start_time = datetime.fromisoformat(event["start_time"])
    if event.get("end_time"):
        end_time = datetime.fromisoformat(event["end_time"])
    else:
        end_time = None

    if event.get("all_day"):
        return "All Day"

    if start_time and end_time and start_time.date() == end_time.date():
        return f"{start_time.strftime(TIME_FORMAT)} - {end_time.strftime(TIME_FORMAT_W_AMPM)}"
    elif start_time and end_time:
        return f"{start_time.strftime(TIME_FORMAT_W_AMPM)} - {end_time.strftime(TIME_FORMAT_W_AMPM)}"
    elif start_time and not end_time:
        return f"{start_time.strftime(TIME_FORMAT)} - {UNK_TIME}"
    else:
        return "Figuring it out..."
