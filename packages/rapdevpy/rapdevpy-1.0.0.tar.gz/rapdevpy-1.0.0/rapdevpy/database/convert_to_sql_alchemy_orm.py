import json
from pathlib import Path

data_type_map = {
    "date-time": "DateTime",
    "date": "Date",
    "integer": "Integer",
    "int32": "Integer",
    "int64": "Integer",
    "string": "String",
    "float": "Float",
    "double": "Float",
    "boolean": "Boolean",
    "object": "Object",
    "array": "Array",
}


def swagger_file_to_sql_alchemy_orm_classes(
    file_path: Path,
):  # ToDo test and perhaps publish into a spereate app
    classes = []
    with open(file_path, "r") as file:
        spec = json.load(file)
        for path, value in spec["paths"].items():
            if value.get("get"):
                responses = value["get"]["responses"]
            elif value.get("post"):
                responses = value["post"]["responses"]
            if responses.get("200"):
                schema = responses["200"]["schema"]
                klass = []
                if schema.get("properties"):
                    for name, desc in schema["properties"].items():
                        if desc.get("format"):
                            klass.append(
                                {
                                    "name": name,
                                    "format": desc["format"],
                                    "type": desc["type"],
                                }
                            )
                        else:
                            klass.append(
                                {"name": name, "format": None, "type": desc["type"]}
                            )
                elif schema.get("items"):
                    if schema.get("items").get("properties"):
                        for name, desc in schema["items"]["properties"].items():
                            if desc.get("format"):
                                klass.append(
                                    {
                                        "name": name,
                                        "format": desc["format"],
                                        "type": desc["type"],
                                    }
                                )
                            else:
                                klass.append(
                                    {"name": name, "format": None, "type": desc["type"]}
                                )
                classes.append({"path": path, "klass": klass})

    with open("sample_orms.py", "w") as output:
        for klass in classes:
            output.write("class {}(Base):\n".format(klass["path"]))
            output.write("    __tablename__ = {}\n\n".format(klass["path"]))
            for name_and_type in klass["klass"]:
                output.write("    {} =".format(name_and_type["name"]))
                format_value = name_and_type["format"]
                type_value = name_and_type["type"]
                if data_type_map.get(format_value):
                    output.write(
                        " Column({})\n".format(data_type_map.get(format_value))
                    )
                elif data_type_map.get(type_value):
                    output.write(" Column({})\n".format(data_type_map.get(type_value)))
                else:
                    raise Exception("{} is not a known type.".format(type_value))
            output.write("\n")
            output.write("    def __repr__(self):\n")
            output.write(
                "        return '{}'.format({})\n".format(
                    ", ".join(
                        [
                            "{}={{}}".format(name_and_type["name"])
                            for name_and_type in klass["klass"]
                        ]
                    ),
                    ", ".join(
                        [
                            "self.{}".format(name_and_type["name"])
                            for name_and_type in klass["klass"]
                        ]
                    ),
                )
            )
            output.write("\n")
