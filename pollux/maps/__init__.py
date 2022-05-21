import os
from pathlib import Path
from importlib import import_module
from pollux.works import MAX_BOUND_LNG_LAT
import re
from pollux.utils import update_deep


class Configs(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        file_maps = os.listdir(Path(__file__).parent)
        self.file_maps = file_maps

    def load(self) -> None:
        self.clear()
        for file in sorted(self.file_maps):
            cls, _, ext = file.rpartition('.')
            if ext != 'py' or cls == '__init__':
                continue

            # print('Chargement de', cls, 'réussi.')
            a = import_module(__name__ + '.' + cls).Config()
            self[str(a.ID)] = a.data


class Layer(dict):
    def __init__(self, name: str, style: str, db: str, *args, **kwargs):
        for arg in args:
            self.update(**arg)
        self.update(**kwargs)
        self.update(**{'name': name, 'style': style, 'db': db})


cls_regex = re.compile(r"(\w+)'>$")


class MapAttr(dict):
    attr_name = ''
    DEFAULT = {}

    def __init__(self, conf_name_or_value='DEFAULT', **kwargs):
        if isinstance(conf_name_or_value, str) and hasattr(self, conf_name_or_value):
            value = getattr(self, conf_name_or_value)
        else:
            value = conf_name_or_value

        if type(value) is bool or value is None:
            value = int(value or 0)
        elif isinstance(value, dict):
            value = {**value, **kwargs}

        self[self._attr_name] = value

    @property
    def default_attr_name(self) -> str:
        cls_name = cls_regex.findall(str(self.__class__))[0]
        return cls_name[0].lower() + cls_name[1:]

    @property
    def _attr_name(self) -> str:
        return self.attr_name or self.default_attr_name


class Gradient(MapAttr):
    attr_name = 'gradient'
    DEFAULT = {
        1.0: 'red',
        0.9: 'orange',
        0.75: 'yellow',
        0.5: 'lime',
        0.3: 'blue',
        0.15: 'violet',
    }

    LIGHT_COLORED = {
        1.0: 'red',
        0.89: 'orange',
        0.77: 'yellow',
        0.63: 'lime',
        0.45: 'blue',
        0.31: 'violet',
    }

    V1 = {
        1.0: 'red',
        0.8: 'orange',
        0.6: 'yellow',
        0.4: 'lime',
        0.2: 'blue',
        0.15: 'violet',
    }

    BLUEBELT = {
        1.0: 'red',
        0.89: 'orange',
        0.77: 'yellow',
        0.63: 'lime',
        0.45: 'blue',
        0.31: 'violet',
        0.3: 'blue',
        0.15: 'violet'
    }


class Icon(MapAttr):
    attr_name = 'icon'
    dir = 'markers/'
    DEFAULT = dir + 'default.png'
    ACCIDENT = dir + 'accident.png'
    BIRD = dir + 'bird.png'
    BUSSTOP = dir + 'busstop.png'
    LAMP = dir + 'lamp.png'
    PEDESTRIAN = dir + 'pedestrian.png'
    SHOP = dir + 'shop.png'
    TREE = dir + 'tree.png'


class Zoom(MapAttr):
    attr_name = 'zoom'
    DEFAULT = {
        'min': 16,
        'max': 22,
        'init': 16
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Radius(MapAttr):
    attr_name = 'radius'
    DEFAULT = {
        'unit': 'auto',
        'fix': 25,
    }


class Value(MapAttr):
    """
        fix: int
        min: int
        max: int
    """
    attr_name = 'value'
    DEFAULT = {
        'fix': 1
    }


class Legend(MapAttr):
    attr_name = 'legend'
    DEFAULT = {
        'name': 'Légende'
    }


class IsActive(MapAttr):
    attr_name = 'isActive'
    NOACTIVE = False
    ACTIVE = True
    DEFAULT = NOACTIVE


class Blur(MapAttr):
    attr_name = 'blur'
    DEFAULT = 15


class PxPerZoom(MapAttr):
    attr_name = 'wheelPxPerZoomLevel'
    DOUBLE = 240
    DEFAULT = 120  # 1 niveau de zoom par scroll


class Orientation(MapAttr):
    attr_name = 'orientation'
    DEFAULT = {
        'fix': -1
    }


class Default_Config:
    ID = 0
    _DEFAULT_DATA = {
        'template_name_or_list': 'maps/map.html',
        'mapJSMethod': 'create_map',
        'description': {},
        'options': {},
        'layers': [],
    }

    _DEFAULT_DESCRIPTION = {
        'href': '',
        'title': 'Titre par défaut',
        'accroche': 'Accroche par défaut',
        'intro': 'Introduction par défaut',
        'icon': '',
        'video': '',
        'QR': [],
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

    OPTIONS_DEFAULT = {
        'bbox': MAX_BOUND_LNG_LAT,
        'draw': {'bboxButton': 1},
        'minOpacity': 0.05,
        **PxPerZoom(),
        **Zoom(),
        **Legend(),
        'buttons': _DEFAULT_BUTTONS,
    }

    # Options par défaut pour tous les layers
    LAYER_DEFAULT = Layer('', '', '',
                          Radius(),
                          Value(),
                          Gradient(),
                          IsActive(),
                          Blur(),
                          Orientation(),
                          )
    # Options par défaut pour le layer actuel
    LAYER_BASE = Layer('', '', '')

    no_dict_attr = ('gradient', 'maxValueDefault')

    @staticmethod
    def copy_and_deep_update(source: dict, other: dict, *args) -> dict:
        ret = source.copy()
        update_deep(ret, other, *args)
        return ret

    @property
    def layers(self) -> dict:
        ret = self.DATA['layers'].copy()
        dict_merged = self.copy_and_deep_update(self.LAYER_DEFAULT, self.LAYER_BASE, *self.no_dict_attr)
        for index, layer in enumerate(ret):
            ret[index] = self.copy_and_deep_update(dict_merged, layer, *self.no_dict_attr)
        return ret

    @property
    def options(self) -> dict:
        return self.copy_and_deep_update(self.OPTIONS_DEFAULT, self.DATA.get('options', {}))

    @property
    def data(self) -> dict:
        self.DATA['layers'] = self.layers
        self.DATA['options'] = self.options.copy()
        self.DATA['description'] = self.description
        self.DATA['href'] = self.DATA.get('href', f'/map/{self.ID}')

        return self.copy_and_deep_update(self._DEFAULT_DATA, self.DATA)

    @property
    def description(self) -> dict:
        return self.copy_and_deep_update(self._DEFAULT_DESCRIPTION, self.DATA.get('description', {}))

    @property
    def buttons(self) -> dict:
        can_scan = False
        for layer in self.DATA.get('layers', {}):
            if layer.get('style') == 'heatmap':
                can_scan = True
                break
        buttons = self.DATA.get('options', {}).get('buttons', {})
        if not can_scan:
            buttons['scan'] = 0
        return self.copy_and_deep_update(self._DEFAULT_BUTTONS, buttons)
