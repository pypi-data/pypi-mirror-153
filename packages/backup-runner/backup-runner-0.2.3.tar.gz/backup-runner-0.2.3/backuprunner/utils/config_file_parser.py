from enum import Enum
from pathlib import Path

from blulib.config_parser import ConfigParser
from blulib.config_parser.config_parser import SectionNotFoundError
from colored import attr
from tealprint import TealPrint

from ..config import config
from .config_file_args import ConfigFileArgs


class Sections(Enum):
    general = "General"
    backups = "Backups"
    mysql = "MySQL"
    email = "Email"


class ConfigFileParser:
    def __init__(self) -> None:
        self.path = Path.home().joinpath(f".{config.app_name}.cfg")

    def get_args(self) -> ConfigFileArgs:
        args = ConfigFileArgs()

        if not self.path.exists():
            TealPrint.warning(f"Could not find config file {self.path}. Please add!", exit=True)
            return args

        config = ConfigParser()
        config.read(self.path)

        TealPrint.verbose(f"Reading configuration {self.path}", color=attr("bold"), push_indent=True)

        try:
            config.to_object(
                args.general,
                "General",
                "backup_location",
                "int:days_to_keep",
            )
        except SectionNotFoundError:
            ConfigFileParser._print_section_not_found("General")

        try:
            config.to_object(
                args.backups,
                "Backups",
                "daily_alias",
                "weekly_alias",
                "monthly_alias",
                "str_list:daily",
                "str_list:weekly",
                "str_list:monthly",
            )
        except SectionNotFoundError:
            ConfigFileParser._print_section_not_found("Backups")

        try:
            config.to_object(
                args.mysql,
                "MySQL",
                "username",
                "password",
                "address",
                "int:port",
                "str_list:databases",
            )
        except SectionNotFoundError:
            ConfigFileParser._print_section_not_found("MySQL")

        try:
            config.to_object(
                args.email,
                "Email",
                "to->to_address",
                "from->from_address",
                "int:disk_percentage",
            )
        except SectionNotFoundError:
            ConfigFileParser._print_section_not_found("Email")

        self._check_required(args)
        TealPrint.pop_indent()

        return args

    @staticmethod
    def _print_section_not_found(section: str) -> None:
        TealPrint.warning(f"⚠ [{section}] section not found!")

    def _check_required(self, args: ConfigFileArgs) -> None:
        if len(args.general.backup_location) == 0:
            self._print_missing("General", "backup_location")

    def _print_missing(self, section: str, varname: str) -> None:
        TealPrint.warning(
            f"Missing {varname} under section {section}. " + f"Please add it to your configuration file {self.path}",
            exit=True,
        )
