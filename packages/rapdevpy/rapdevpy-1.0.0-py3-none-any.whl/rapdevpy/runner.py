"""
    rapdevpy.py
    ------------------

    This is a library. It does not have a Runner.

    :copyrgiht: 2019 MislavJaksic
    :license: MIT License
"""
from pathlib import Path

from rapdevpy.database.convert_to_sql_alchemy_orm import (
    swagger_file_to_sql_alchemy_orm_classes,
)

# swagger_file_to_sql_alchemy_orm_classes(Path("swagger.json"))
from rapdevpy.parser import cprofile_parser

cprofile_parser.parse("profile-log.txt")
