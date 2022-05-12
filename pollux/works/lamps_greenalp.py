from . import Default_works, BASE_DIR
import os
from pollux.formats.geojson import Geojson
import re


class Works(Default_works):
    filename = "data_patrimoines_EP"
    file_ext = "txt"
    fake_request = True
    model = None

    def load(self, filename: str = '', file_ext: str = '') -> dict:
        filename = filename or self.filename
        file_ext = file_ext or self.file_ext
        with open(os.path.join(BASE_DIR, 'db', f'{filename}.{file_ext}'), 'r') as file:
            ret = Geojson()
            lines = file.readlines()
            columns = lines[0].replace('\n', '').split('\t')
            for line in lines[1:]:
                line_data = {k: v for k, v in zip(columns, line.replace('\n', '').split('\t'))}
                ret.append(line_data)

        return ret

    def _can_be_output(self, feature: 'Model', bound=None, **kwargs) -> bool:
        return super()._can_be_output(feature, bound=bound)

    class Model(Default_works.Model):
        regex_int_only = re.compile(r'(\d+)')

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.code = kwargs['properties']["Code Lampe"]
            try:
                self.irc = int(re.search(self.regex_int_only, kwargs['properties']['IRC'])[0] or -1)
            except (IndexError, TypeError):
                self.irc = -1
            try:
                self.power = int(kwargs['properties']['Puissance'].replace('W', ''))
            except ValueError:
                self.power = int(kwargs['properties']['Puissance foyer (Watt)'])
