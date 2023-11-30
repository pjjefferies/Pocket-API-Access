import datetime as dt


def datetime_older_than(datetime: dt.datetime, max_days_old: int) -> bool:
    """Determine if datetime is newer than given days old"""
    return datetime < (dt.datetime.now() - dt.timedelta(days=max_days_old))
