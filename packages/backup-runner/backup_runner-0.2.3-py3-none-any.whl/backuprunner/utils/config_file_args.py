from typing import List


class ConfigFileArgs:
    def __init__(self) -> None:
        self.general = General()
        self.backups = Backups()
        self.mysql = Mysql()
        self.email = Email()


class General:
    def __init__(self) -> None:
        self.backup_location: str = ""
        self.days_to_keep: int = 65


class Backups:
    def __init__(self) -> None:
        self.daily: List[str] = []
        self.daily_alias: str = "daily"
        self.weekly: List[str] = []
        self.weekly_alias: str = "weekly"
        self.monthly: List[str] = []
        self.monthly_alias: str = "monthly"


class Mysql:
    def __init__(self) -> None:
        self.username: str = ""
        self.password: str = ""
        self.address: str = "localhost"
        self.port: int = 3306
        self.databases: List[str] = []


class Email:
    def __init__(self) -> None:
        self.to_address: str = ""
        self.from_address: str = ""
        self.disk_percentage: int = 85
