from .geojson import Geojson
import re
from typing import Pattern
import os
from pollux.works import BASE_DIR

regex_csv_attr = re.compile('(?:^|,)(?=[^"]|(")?)"?((?(1)[^"]*|[^,"]*))"?(?=,|$)')


def convert_to_geojson(directory_file: str, regex: Pattern = regex_csv_attr) -> dict:
    with open(os.path.join(BASE_DIR, directory_file), "r") as file:
        file_lines = file.readlines()
        first_line = file_lines[0].partition("\n")[0]
        if first_line[0] == "\ufeff":
            first_line = first_line[1:]

    columns = regex.findall(first_line)
    ret = Geojson()
    for line in file_lines[1:]:
        line = line.partition("\n")[0]
        line_data = {
            key[1]: value[1] for key, value in zip(columns, regex.findall(line))
        }
        ret.append(line_data)

    return ret
