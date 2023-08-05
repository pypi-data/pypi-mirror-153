from __future__ import annotations

from typing import List

import backuprunner.mailer as mailer

from .backup.backup import Backup, remove_old
from .backup.mysql_backup import MysqlBackup
from .backup.path_backup import MonthlyBackup, PathBackup, WeeklyBackup
from .config import config
from .utils.arg_parser import get_args
from .utils.config_file_parser import ConfigFileParser


def main():
    config.set_from_cli(get_args())
    config_parser = ConfigFileParser()
    config.set_from_config_file(config_parser.get_args())

    # Remove old backups
    remove_old()

    warnings: List[str] = []

    # MySQL backup
    if config.mysql.username and config.mysql.password:
        run_backup(MysqlBackup(), warnings)

    # Daily
    if len(config.backups.daily) > 0:
        run_backup(PathBackup(config.backups.daily_alias, config.backups.daily), warnings)

    # Weekly
    if len(config.backups.weekly) > 0:
        run_backup(WeeklyBackup(config.backups.weekly_alias, config.backups.weekly), warnings)

    # Monthly
    if len(config.backups.monthly) > 0:
        run_backup(MonthlyBackup(config.backups.monthly_alias, config.backups.monthly), warnings)

    # Send mail
    mailer.send_warnings(warnings)
    mailer.send_if_disk_almost_full()


def run_backup(backup: Backup, warnings: List[str]):
    backup.run()

    if not backup.filepath.exists():
        warnings.append(f"Backup {backup.name} failed! ({backup.filename})")


if __name__ == "__main__":
    main()
