from . import *
from copy import deepcopy


class Config(Default_Config):
    class Meta:
        abstract = True

    _ID = "greenalp"
    CLONE_ID = "00"
    LAYER_BASE = Layer('', '', '',
                       Gradient('LIGHT_COLORED'),
                       Blur(unit='%', fix=35),
                       Filters(position__within=[5.704337, 45.182177, 5.722755, 45.184826])
                       )
    _DATA = {
        'options': Options(
            Legend(name=""),
        ),
        'layers': [
            Layer(
                'Luminaires (Impact sol)',
                'heatmap',
                'lamps',
                Radius(unit='meter'),
                Orientation(field='orientation'),
                HorizontalAngle(field='horizontal_angle'),
                MaxValue(method='part%', fix=80),
                Value(field='impact_tree_on_ground'),
            ),
            Layer(
                'Luminaires (Impact Arbre - Jour)',
                'heatmap',
                'lamps',
                Radius(unit='pixel'),
                MaxValue(method='part%', fix=80),
                Value(field='day_impact'),
                IsActive(True),
            ),
            Layer(
                'Luminaires (Impact Arbre - Nuit)',
                'heatmap',
                'lamps',
                Radius(unit='pixel'),
                MaxValue(method='part%', fix=80),
                Value(field='night_impact'),
            ),
            Layer(
                'Luminaires (Coût)',
                'heatmap',
                'lamps',
                Gradient('BLUEBELT'),
                Orientation(field='orientation'),
                HorizontalAngle(field='horizontal_angle'),
                Radius(fix=20, unit='auto'),
                MaxValue(method='part%',
                         fix=95),
                Blur(unit='%', fix=30),
                Value(field='expense'),
            ),
            Layer(
                'Luminaires',
                'cluster',
                'lamps',
                Icon('LAMP'),
            ),
            Layer(
                'Arbres',
                'cluster',
                'trees',
                Icon('TREE'),
            ),
        ],
    }

    @property
    def ID(self) -> str:
        return f'{self._ID}{self.CLONE_ID}'

    @property
    def DATA(self) -> dict:
        ret = deepcopy(self._DATA)
        ret['options'] = Options(Legend(name=self.ID.capitalize()))
        for layer in ret['layers']:
            if layer['db'] == 'lamps':
                layer["db"] += f'_{self.ID}'

        return ret
