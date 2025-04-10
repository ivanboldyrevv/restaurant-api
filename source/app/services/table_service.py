from app.database import Database
from app.models import Table
from app.services.service import BaseService


class TableService(BaseService):
    def __init__(self, database: Database) -> None:
        super().__init__(database, Table)

    def add_table(self, name: str, seats: int, location: str) -> Table:
        return self.add(
            Table(
                name=name,
                seats=seats,
                location=location
            )
        )
