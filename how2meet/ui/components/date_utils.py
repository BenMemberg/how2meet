from datetime import datetime

from typing import Any, Dict

DATE_FORMAT = "%m/%d/%Y"
TIME_FORMAT = "%I:%M%p"
SAME_DAY_FORMAT = "{start_date} {start_time} - {end_time}"
DIFFERENT_DAY_FORMAT = "{start_date} {start_time} - {end_date} {end_time}"

def event_dates_to_str(event: Dict[str, Any]) -> str:
    """
    Converts the event's start and end dates to a human-readable string.

    Args:
        event: The event to convert.

    Returns:
        str: The human-readable string representing the event's start and end dates.
    """
    if event.get("start_time"):
        start_time = datetime.fromisoformat(event["start_time"])
    if event.get("end_time"):
        end_time = datetime.fromisoformat(event["end_time"])
    else:
        end_time = None

    if event.get("all_day"):
        return start_time.strftime(DATE_FORMAT)

    if start_time and end_time and start_time.date() == end_time.date():
        return SAME_DAY_FORMAT.format(
            start_date=start_time.strftime(DATE_FORMAT),
            start_time=start_time.strftime(TIME_FORMAT),
            end_time=end_time.strftime(TIME_FORMAT)
        )
    elif start_time and end_time:
        return DIFFERENT_DAY_FORMAT.format(
            start_date=start_time.strftime(DATE_FORMAT),
            start_time=start_time.strftime(TIME_FORMAT),
            end_date=end_time.strftime(DATE_FORMAT),
            end_time=end_time.strftime(TIME_FORMAT)
        )
    elif start_time and not end_time:
        end_time_str = "?"
        return SAME_DAY_FORMAT.format(
            start_date=start_time.strftime(DATE_FORMAT),
            start_time=start_time.strftime(TIME_FORMAT),
            end_time=end_time_str
        )
    else:
        return "Figuring it out..."
