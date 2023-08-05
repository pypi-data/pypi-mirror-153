from datetime import datetime
from enum import Enum
from os import remove
from pathlib import Path

import backuprunner.date_helper as date_helper
from colored import attr
from tealprint import TealPrint

from ..config import config


def remove_old() -> None:
    """Remove all old backups"""
    TealPrint.info("Removing old backups", color=attr("bold"), push_indent=True)
    backup_path = Path(config.general.backup_location)
    for backup in backup_path.glob("*"):
        if backup.is_file() and date_helper.is_backup_old(backup):
            TealPrint.info(f"🔥 {backup}")
            remove(backup)
    TealPrint.pop_indent()


class BackupParts(Enum):
    full = "full"
    day_diff = "day-diff"
    week_diff = "week-diff"


class Backup:
    def __init__(self, name: str) -> None:
        self.name = name
        self._diff_start: datetime
        self._diff_end: datetime
        self._calculate_part_diffs()

    def run(self) -> None:
        """Run the backup"""

    def is_modified_within_diff(self, path: Path) -> bool:
        modified_time = date_helper.get_modified_datetime(path)
        return self._diff_start <= modified_time and modified_time <= self._diff_end

    @property
    def filename(self) -> str:
        """Filename to use for the backup"""
        return f"{self.name}_{date_helper.yesterday_str()}_{self.part.value}.{self.extension}"

    @property
    def filepath(self) -> Path:
        """Full filepath to the backup"""
        return Path(config.general.backup_location).joinpath(self.filename)

    @property
    def part(self) -> BackupParts:
        # Force full backup
        if config.force_full:
            return BackupParts.full
        else:
            return self._get_part()

    @property
    def extension(self) -> str:
        return ""

    def _get_part(self) -> BackupParts:
        return BackupParts.full

    def _calculate_part_diffs(self) -> None:
        # Day diff
        if self.part == BackupParts.day_diff:
            self._diff_start = date_helper.yesterday()

        # Weekly diff
        elif self.part == BackupParts.week_diff:
            self._diff_start = date_helper.last_week()

        else:
            self._diff_start = date_helper.today()

        self._diff_end = date_helper.today()
