from datetime import datetime, timedelta
from pathlib import Path

from .config import config


def yesterday_str() -> str:
    """Yesterday date as a string"""
    return yesterday().strftime("%Y-%m-%d")


def yesterday() -> datetime:
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    return today - timedelta(days=1)


def today() -> datetime:
    return datetime.today()


def last_week() -> datetime:
    return today() - timedelta(weeks=1)


def get_modified_datetime(file: Path) -> datetime:
    return datetime.fromtimestamp(file.stat().st_mtime)


def is_today_monday() -> bool:
    return today().weekday() == 0


def day_of_month() -> int:
    return today().day


def is_backup_old(file: Path) -> bool:
    old_date = today() - timedelta(days=config.general.days_to_keep)
    return old_date > datetime.fromtimestamp(file.stat().st_ctime)
