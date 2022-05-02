from . import Default_works
import re
from typing import TextIO
from formats.geojson import Geojson, Geo_Feature

regex_csv_attr = re.compile(r'"([^"]*)";?')


def convert_to_geojson(_, file: TextIO, regex=regex_csv_attr) -> dict:
    file_content = file.readlines()
    columns = file_content[0].partition('\n')[0]
    if columns[0] == '\ufeff':
        columns = columns[1:]

    columns = regex.findall(columns)
    ret = Geojson()
    for line in file_content[1:]:
        line = line.partition('\n')[0]
        line_data = {
            key: value
            for key, value in zip(columns, regex.findall(line))}
        ret.append(line_data)

    return ret


class Works(Default_works):
    filename = "accidents"
    file_ext = "csv"
    COPYRIGHT_ORIGIN = 'www.data.gouv.fr'
    fake_request = True
    convert_to_geojson_method = convert_to_geojson

    def _can_be_output(self, feature: Geo_Feature, **kwargs) -> bool:
        return super()._can_be_output(feature, **kwargs) and feature.night_and_lightless

    class Model(Default_works.Model):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.date = kwargs['properties']['jour'].zfill(2) + '/' +\
                        kwargs['properties']['mois'].zfill(2) + '/' +\
                        kwargs['properties']['an']
            self.night_and_lightless = kwargs['properties']['lum'] in ('3', '4')


def coord_pos_to_float(value) -> float:
    try:
        return float(value)
    except ValueError:
        if type(value) is str:
            return float(value.replace(',', '.'))
    raise ValueError
