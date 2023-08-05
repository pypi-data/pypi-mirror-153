import tarfile
from io import BytesIO
from subprocess import DEVNULL, PIPE, run
from typing import List, Optional

from colored import attr, fg
from tealprint import TealPrint

from ..config import config
from .backup import Backup


class MysqlBackup(Backup):
    def __init__(self) -> None:
        super().__init__("MySQL")

    def run(self) -> None:
        # Only run if a MySQL username and password has been supplied
        if not config.mysql.username and not config.mysql.password:
            TealPrint.info(
                "Skipping MySQL backup, no username and password supplied",
                color=fg("yellow"),
            )
            return

        TealPrint.info("Backing up MySQL", color=attr("bold"))
        with tarfile.open(self.filepath, "w:gz") as tar:
            # Multiple database
            if len(config.mysql.databases) > 0:
                for database in config.mysql.databases:
                    dump = self._get_database(database)
                    self._add_to_tar_file(tar, database, dump)
            else:
                dump = self._get_database()
                self._add_to_tar_file(tar, "all-databases", dump)

        TealPrint.info("✔ MySQL backup complete!")

    def _add_to_tar_file(self, tar: tarfile.TarFile, name: str, data: bytes) -> None:
        tar_info = tarfile.TarInfo(name=f"{name}.sql")
        tar_info.size = len(data)
        tar.addfile(tar_info, BytesIO(data))

    def _get_database(self, name: Optional[str] = None) -> bytes:
        cmd = self._get_sqldump_command(name)
        output = run(
            cmd,
            stdout=PIPE,
            stderr=DEVNULL,
        )
        return output.stdout

    def _get_sqldump_command(self, db_name: Optional[str]) -> List[str]:
        """Get the command to dump the sql

        Args:
            db_name (Optional[str]): dump only the specified database. If 'None' it dumps all databases
        """
        args = [
            "mysqldump",
            "-u",
            str(config.mysql.username),
            f"--password={config.mysql.password}",
            f"--host={config.mysql.address}",
            f"--port={config.mysql.port}",
        ]
        if db_name and db_name != "":
            args.append(db_name)
        else:
            args.append(("--all-databases"))

        return args

    @property
    def extension(self) -> str:
        return "tgz"
