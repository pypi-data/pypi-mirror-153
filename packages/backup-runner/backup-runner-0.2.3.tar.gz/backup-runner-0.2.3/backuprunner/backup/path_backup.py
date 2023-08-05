import tarfile
from glob import glob
from pathlib import Path
from typing import List

import backuprunner.date_helper as date_helper
from colored import attr
from tealprint import TealPrint

from .backup import Backup, BackupParts


class PathBackup(Backup):
    def __init__(self, name: str, paths: List[str]) -> None:
        super().__init__(name)
        self.paths = paths
        self.tar = tarfile.open(self.filepath, "w:gz")

    def run(self) -> None:
        """Add files to tar"""
        TealPrint.info(f"Backing up {self.name}", color=attr("bold"), push_indent=True)

        # Full backup
        if self.part == BackupParts.full:
            TealPrint.info("Doing a full backup", push_indent=True)
            for path_glob in self.paths:
                TealPrint.verbose(f"{path_glob}", push_indent=True)
                for path in glob(path_glob):
                    TealPrint.debug(f"{path}")
                    self.tar.add(path)
                TealPrint.pop_indent()
            TealPrint.pop_indent()

        # Diff backup
        else:
            TealPrint.info("Doing a diff backup", push_indent=True)
            for path_glob in self.paths:
                TealPrint.verbose(f"{path_glob}", push_indent=True)
                for path in glob(path_glob):
                    self._find_diff_files(Path(path))
                TealPrint.pop_indent()
            TealPrint.pop_indent()

        TealPrint.pop_indent()

    def _find_diff_files(self, path: Path):
        # File/Dir has changed
        try:
            TealPrint.debug(f"{path}", push_indent=True)
            if path.is_symlink() or (not path.is_dir() and self.is_modified_within_diff(path)):
                self.tar.add(path)
            # Check children
            else:
                if not path.is_symlink():
                    for child in path.glob("*"):
                        self._find_diff_files(child)
                    for child in path.glob(".*"):
                        self._find_diff_files(child)
            TealPrint.pop_indent()
        except FileNotFoundError:
            # Skip if we didn't find a file
            pass

    @property
    def extension(self) -> str:
        return "tgz"


class WeeklyBackup(PathBackup):
    def __init__(self, name: str, paths: List[str]) -> None:
        super().__init__(name, paths)

    def _get_part(self) -> BackupParts:
        if date_helper.is_today_monday():
            return BackupParts.full
        else:
            return BackupParts.day_diff


class MonthlyBackup(PathBackup):
    def __init__(self, name: str, paths: List[str]) -> None:
        super().__init__(name, paths)

    def _get_part(self) -> BackupParts:
        day = date_helper.day_of_month()

        if day == 1:
            return BackupParts.full
        elif (day - 1) % 7 == 0:
            return BackupParts.week_diff
        else:
            return BackupParts.day_diff
