from datetime import datetime, timezone

NOTZ = "%Y-%m-%d %H:%M:%S"
GER = "%Y-%m-%d %H:%M:%S%z"
TZ = "Europe/Berlin"


def convert_dt(now):
    if isinstance(now, str):
        now = datetime.strptime(now, GER)
    elif isinstance(now, int):
        now = datetime.utcfromtimestamp(now)

    if isinstance(now, datetime):
        now = now.astimezone(timezone.utc)
    else:
        raise ValueError(f"Unknown date format: {now} of type {type(now)}")

    return now
