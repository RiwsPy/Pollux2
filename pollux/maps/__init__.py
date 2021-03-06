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
            if a.Meta.abstract is True:
                continue
            self[str(a.ID)] = a.data
            #print(a.ID, a.options)
            #print(a.data)


class Layer(dict):
    def __init__(self, name: str, typ: str, db: str, *args, **kwargs):
        for arg in args:
            if 'preset' in arg:
                self.update(**arg['preset'])
                del arg['preset']
            self.update(**arg)
        self.update(**kwargs)
        self.update(**{'name': name, 'type': typ, 'db': db})


class Options(dict):
    def __init__(self, *args, **kwargs):
        for arg in args:
            self.update(**arg)
        self.update(**kwargs)


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
        0.1: 'black',
    }

    LIGHT_COLORED = {
        1.0: 'red',
        0.89: 'orange',
        0.77: 'yellow',
        0.63: 'lime',
        0.45: 'blue',
        0.31: 'violet',
        0.1: 'black',
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
        0.1: 'black',
    }

    TEMPERATURE_COLOR = {
        0.3333: '#FF880E',
        0.4166: '#FF9F46',
        0.5: '#FFB16D',
        0.6666: '#FFCDA6',
        0.8333: '#FFE4CD',
        1.0: '#FFF6EC',
    }


class Filters(MapAttr):
    attr_name = 'filters'
    DEFAULT = {
        'position__within': [5.718705, 45.187602, 5.727996, 45.189931],
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
        'min': 15,
        'max': 22,
        'init': 16,
        'scroll': 1,
        'button': 1,
    }


class Radius(MapAttr):
    attr_name = 'radius'
    DEFAULT = {
        'unit': 'auto',
        'fix': 25,
        'add': 0,
    }


class Style(MapAttr):
    attr_name = 'style'
    DEFAULT = {}


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


class TileLayer(MapAttr):
    attr_name = 'tile_layer'
    DEFAULT = {
        'url': 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
        'maxZoom': 22,
        'attribution': '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>' +
                       'contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
    }

    NIGHT = {
        'url': 'http://{s}.sm.mapstack.stamen.com/(toner-lite,$fff[difference],$fff[@23],$fff[hsl-saturation@20])/{z}/{x}/{y}.png',
        'maxZoom': 20,
        'attribution': ''
    }

    OSM = {
        'url': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        'maxZoom': 19,
        'attribution': '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
    }


class IsActive(MapAttr):
    attr_name = 'isActive'
    NOACTIVE = False
    ACTIVE = True
    DEFAULT = NOACTIVE


class Blur(MapAttr):
    attr_name = 'blur'
    DEFAULT = {
        'fix': 15,
    }


class Orientation(MapAttr):
    attr_name = 'orientation'
    DEFAULT = {
        'fix': -1
    }


class HorizontalAngle(MapAttr):
    attr_name = 'horizontal_angle'
    DEFAULT = {
        'fix': 360
    }


class MaxValue(MapAttr):
    attr_name = 'maxValue'
    DEFAULT = {
        'method': 'zoom_depend',
        'gradient': {14: 3, 15: 3, 16: 3, 17: 3, 18: 2, 19: 1.5, 20: 1.1},
    }

    DOUBLE = {
        'method': 'zoom_depend',
        'gradient': {k: v*2 for k, v in DEFAULT['gradient'].items()}
    }


class Default_Config:
    class Meta:
        abstract = False

    ID = 0
    abstract = False
    DATA = {}
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

    OPTIONS_DEFAULT = Options(
        TileLayer(),
        Zoom(),
        Legend(),
        draw={'bboxButton': 1},
        minOpacity=0.05,
        buttons=_DEFAULT_BUTTONS,
    )

    # Options par défaut pour tous les layers
    LAYER_DEFAULT = Layer('', '', '',
                          Radius(),
                          Value(),
                          Gradient(),
                          IsActive(),
                          Blur(),
                          Orientation(),
                          HorizontalAngle(),
                          MaxValue(),
                          Filters(),
                          Style(),
                          )
    # Options par défaut pour le layer actuel
    LAYER_BASE = Layer('', '', '')

    no_dict_attr = ('gradient',)

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
        data = self.DATA.copy()
        data['layers'] = self.layers
        data['options'] = self.options.copy()
        data['description'] = self.description
        data['href'] = self.DATA.get('href', f'/map/{self.ID}')
        return self.copy_and_deep_update(self._DEFAULT_DATA, data)

    @property
    def description(self) -> dict:
        return self.copy_and_deep_update(self._DEFAULT_DESCRIPTION, self.DATA.get('description', {}))

    @property
    def buttons(self) -> dict:
        can_scan = False
        for layer in self.DATA.get('layers', {}):
            if layer.get('type') == 'heatmap':
                can_scan = True
                break
        buttons = self.DATA.get('options', {}).get('buttons', {})
        if not can_scan:
            buttons['scan'] = 0
        return self.copy_and_deep_update(self._DEFAULT_BUTTONS, buttons)


class Preset(MapAttr):
    OLD_SCHOOL = Layer('', '', '',
                       Gradient('V1'),
                       MaxValue(),
                       Radius(method='fix', fix=25, unit='pixel'),
                       )
