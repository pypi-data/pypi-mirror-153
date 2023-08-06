import re


def parse(cprofile_file: str):
    with open(cprofile_file, "r", encoding="utf-16") as in_file:
        with open("cprofile_parser.csv", "w", encoding="utf-16") as out_file:
            for line in in_file:
                parsed_line = "$".join([x for x in line.split(" ") if x])
                out_file.write(parsed_line)
