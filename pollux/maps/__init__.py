import os
from pathlib import Path
from importlib import import_module
from pollux.works import MAX_BOUND_LNG_LAT

# TODO: icon.TREE, ...


class Configs(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        file_maps = os.listdir(Path(__file__).parent)
        try:
            file_maps.remove('__init__.py')
        except ValueError:
            pass
        self.file_maps = file_maps

    def load(self) -> None:
        self.clear()
        for file in sorted(self.file_maps):
            cls, _, ext = file.rpartition('.')
            if ext != 'py':
                continue

            # print('Chargement de', cls, 'réussi.')
            a = import_module(__name__ + '.' + cls).Config()
            self[str(a.ID)] = a.__dict__


class Gradient:
    LIGHT_COLORED = {
        1.0: 'red',
        0.89: 'orange',
        0.77: 'yellow',
        0.63: 'lime',
        0.45: 'blue',
        0.31: 'violet',
    }

    DEFAULT = {
        1.0: 'red',
        0.9: 'orange',
        0.75: 'yellow',
        0.5: 'lime',
        0.3: 'blue',
        0.15: 'violet',
    }

    V1 = {
        1.0: 'red',
        0.8: 'orange',
        0.6: 'yellow',
        0.4: 'lime',
        0.2: 'blue',
        0.15: 'violet',
    }


class Default_Config:
    ID = 0
    DATA = {}
    _DEFAULT_DATA = {
        'template_name_or_list': 'maps/map.html',
        'mapJSMethod': 'create_map',
        'description': {},
        'layers': [],
        'options': {}
    }

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
    _DEFAULT_OPTIONS = {
        'bbox': MAX_BOUND_LNG_LAT,
        'draw': {'bboxButton': 1},
        'minOpacity': 0.05,
        'isActive': 0,
        'maxValueDefault': 0,
        'blur': 15,
        'wheelPxPerZoomLevel': 120,  # 1 niveau de zoom par scroll
        'gradient': Gradient.DEFAULT,
    }
    _DEFAULT_BUTTONS = {
        'fullScreen': 1,
        'scan':
            {
                'title': {"true": "Scanner la zone"},
                'href': "_click",
                'awesomeIcon': "fa fa-thumbs-up fa-lg",
            },
        'description':
            {
                'title': {"true": "Ouvrir la description"},
                'href': "/map_desc/%ID%",
                'awesomeIcon': "fa fa-book fa-lg",
            },
        'home':
            {
                'title': {"true": "Retour à l'accueil"},
                'href': '/',
                'awesomeIcon': 'fas fa-door-open',
            },
    }
    _DEFAULT_RADIUS = {
        'fix': 25,
        'unit': 'auto',  # auto / meter / pixel /
    }
    _DEFAULT_ZOOM = {
        'max': 22,
        'min': 16,
        'init': 16,
    }
    _DEFAULT_ORIENTATION = {
        'fix': -1,
    }
    _DEFAULT_VALUE = {
        'fix': 1,
    }
    _DEFAULT_LEGEND = {
        'name': 'Legend',
    }

    @property
    def data(self) -> dict:
        return {**self._DEFAULT_DATA,
                **self.DATA,
                **{'description': self.description},
                **{'options': {**self.options,
                               **{'legend': self.legend},
                               **{'buttons': self.buttons},
                               **{'zoom': self.zoom},
                               **{'value': self.value},
                               **{'orientation': self.orientation},
                               **{'radius': self.radius}}},
                }

    @property
    def description(self) -> dict:
        return {**self._DEFAULT_DESCRIPTION, **self.DATA.get('description', {})}

    @property
    def legend(self) -> dict:
        return {**self._DEFAULT_LEGEND, **self.DATA.get('legend', {})}

    @property
    def options(self) -> dict:
        return {**self._DEFAULT_OPTIONS, **self.DATA.get('options', {})}

    @property
    def radius(self) -> dict:
        return {**self._DEFAULT_RADIUS, **self.options.get('radius', {})}

    @property
    def orientation(self) -> dict:
        return {**self._DEFAULT_ORIENTATION, **self.options.get('orientation', {})}

    @property
    def value(self) -> dict:
        return {**self._DEFAULT_VALUE, **self.options.get('value', {})}

    @property
    def zoom(self) -> dict:
        return {**self._DEFAULT_ZOOM, **self.options.get('zoom', {})}

    @property
    def buttons(self) -> dict:
        can_scan = False
        for layer in self.DATA.get('layers', {}):
            if layer.get('layerType') == 'heatmap':
                can_scan = True
                break
        buttons = self.DATA.get('options', {}).get('buttons', {})
        if not can_scan:
            buttons['scan'] = 0
        return {**self._DEFAULT_BUTTONS, **buttons}

    @property
    def href(self) -> str:
        return self.data.get('href', f'/map/{self.ID}')

    @property
    def __dict__(self) -> dict:
        return {**self.data, **{'href': self.href}}
