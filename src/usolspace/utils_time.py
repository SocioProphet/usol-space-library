from datetime import datetime, timezone


def to_utc_iso(ts):
    if isinstance(ts, datetime):
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        else:
            ts = ts.astimezone(timezone.utc)
        return ts.strftime("%Y-%m-%d %H:%M")
    return str(ts)
