import sqlite3
from pathlib import Path
from typing import List, Tuple


class SqliteOperator:
    def __init__(self, database_path: Path):
        self.connection = sqlite3.connect(database_path)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def execute(self, sql: str, non_column_non_table_placeholders: dict) -> List[Tuple]:
        self.cursor.execute(sql, non_column_non_table_placeholders)
        return self.cursor.fetchall()

    def get_tables(self) -> List[str]:
        tuples = self.execute(
            """
        SELECT name FROM sqlite_master 
        WHERE type = 'table' 
        AND name NOT LIKE 'sqlite_%'
        ORDER BY 1;""",
            {},
        )
        return [x[0] for x in tuples]

    def get_table_info(self, table: str) -> List[Tuple]:
        return self.execute("PRAGMA table_info({});".format(table), {})

    def close(self):
        self.cursor.close()
        self.connection.close()
