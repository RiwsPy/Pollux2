import os
from pathlib import Path
from importlib import import_module


class Configs(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        file_maps = os.listdir(Path(__name__).resolve())
        file_maps.remove('__init__.py')
        self.file_maps = file_maps

    def load(self) -> None:
        self.clear()
        for file in sorted(self.file_maps):
            cls, _, ext = file.rpartition('.')
            if ext != 'py':
                continue

            parent_dir = os.path.dirname(__file__).rsplit('/', 1)[-1]
            a = import_module(parent_dir + '.' + cls).Config()
            self[str(a.ID)] = a.__dict__


class Default_Config:
    ID = 0
    DATA = {}
    _DEFAULT_DATA = {
        'template_name_or_list': 'maps/map.html',
        'mapJSMethod': 'create_map',
        'href': '',
        'description': {},
        'layers': [],
        'options': {}}

    DESCRIPTION = {}
    _DEFAULT_DESCRIPTION = {
        'href': '',
        'title': 'Titre par défaut',
        'accroche': 'Accroche par defaut',
        'intro': 'Introduction par défaut',
        'icon': '',
        'video': '',
        'QR': [],
    }

    @property
    def data(self) -> dict:
        return {**self._DEFAULT_DATA, **self.DATA, **{'description': self.description}}

    @property
    def description(self) -> dict:
        return {**self._DEFAULT_DESCRIPTION, **self.DATA.get('description', {})}

    @property
    def href(self) -> str:
        return self.data.get('href', f'/map/{self.ID}')

    @property
    def __dict__(self) -> dict:
        return {**self.data, **{'href': self.href}}
