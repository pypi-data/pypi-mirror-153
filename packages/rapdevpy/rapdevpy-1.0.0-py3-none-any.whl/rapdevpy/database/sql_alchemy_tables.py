from typing import Dict

from sqlalchemy import MetaData, Table


class SqlAlchemyTables:
    metadata: MetaData
    tables: Dict[str, Table]

    def __init__(self, metadata: MetaData):
        self.metadata = metadata
        self.tables = {}

    def __getitem__(self, key: str) -> Table:
        return self.tables[key]

    def __len__(self) -> int:
        return len(self.tables)

    def add_table(self, table: str, *args) -> None:
        self.tables[table] = Table(table, self.metadata, *args)
