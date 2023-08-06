from pathlib import Path
from typing import List, Dict

import sqlalchemy
from sqlalchemy import text, inspect, MetaData, Table
from sqlalchemy.engine import Result
from sqlalchemy.future import create_engine, Engine
from sqlalchemy.orm import Session


class SqlAlchemyOperator:
    engine: Engine
    session: Session

    def __init__(self, database_url: str, is_echo: bool = True, is_future: bool = True):
        """
        :param database_url "sqlite:///C:\\path\\to\\foo.db" or "sqlite:///:memory:"

        Engine: central source of Connections to a database, most efficient when it is a global object
        Connection: unit of connectivity
        Session: an ORM style Connection
        """
        self.engine = create_engine(database_url, echo=is_echo, future=is_future)
        self.session = Session(self.engine)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def execute_text(self, sql: str, values: List[Dict]) -> Result:
        return self.session.execute(text(sql), values)

    def execute_core(self, alchemy_core, values: List[Dict]) -> Result:
        return self.session.execute(alchemy_core, values)

    def commit(self) -> None:
        self.session.commit()

    def create_all_tables(self, metadata: MetaData):
        metadata.create_all(self.engine)

    def drop_all_tables(self, metadata: MetaData):
        metadata.drop_all(self.engine)

    def get_table_list(self) -> List[str]:
        with self.engine.connect() as connection:
            inspector = inspect(connection)
            return inspector.get_table_names()

    def get_table_column_list(self, table: str) -> List[Dict]:
        with self.engine.connect() as connection:
            inspector = inspect(connection)
            return inspector.get_columns(table)

    def table_to_orm_file(self, table: str, file_path: Path):
        columns = self.get_table_column_list(table)
        with open(file_path, "w") as file:
            file.write("class {}(Base):\n".format(table))
            file.write("    __tablename__ = '{}'\n\n".format(table))
            for column in columns:
                if column["nullable"]:
                    file.write(
                        "    {} = Column({})\n".format(column["name"], column["type"])
                    )
                else:
                    file.write(
                        "    {} = Column({}, nullable={})\n".format(
                            column["name"], column["type"], column["nullable"]
                        )
                    )
            file.write("    def __repr__(self):\n")
            file.write(
                "        return '{}'.format({})\n".format(
                    ", ".join(["{}={{}}".format(column["name"]) for column in columns]),
                    ", ".join(["self.{}".format(column["name"]) for column in columns]),
                )
            )
            file.write("\n")

    def get_table_metadata(self, table: str) -> Table:
        metadata = MetaData()
        return Table(table, metadata, autoload_with=self.engine)

    def get_alchemy_version(self) -> str:
        return sqlalchemy.__version__

    def is_table_exist(self, table: str) -> bool:
        tables = self.get_table_list()
        if table in tables:
            return True
        return False

    def close(self):
        self.session.close()
