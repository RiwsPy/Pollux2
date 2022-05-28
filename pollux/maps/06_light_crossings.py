from . import *


class Config(Default_Config):
    ID = 6
    LAYER_BASE = Layer('', '', '',
                       Radius(fix=15, unit='auto'),
                       Gradient('BLUEBELT'),
                       Blur(unit='%', fix=40),
                       MaxValue(method='fix',
                                fix=20),
                       Value(max=20)
                       )
    DATA = {
        'options': Options(
            Zoom(max=20, init=16),
            Legend(name="Qualité d'éclairage"),
            bbox=[5.717633, 45.182596, 5.734348, 45.185410],
        ),
        'layers': [
            Layer(
                'Passages piétons (Jour)',
                'heatmap',
                'crossings',
                IsActive(True),
                Value(field='illuminance_day', invert=1),
            ),
            Layer(
                'Passages piétons (Nuit)',
                'heatmap',
                'crossings',
                Value(field='illuminance_night', invert=1),
            ),
            Layer(
                'Passages piétons',
                'cluster',
                'crossings',
                Icon('PEDESTRIAN'),
            ),
            Layer(
                'Luminaires',
                'cluster',
                'lamps',
                Icon('LAMP'),
            ),
            Layer(
                'Zones éclairées',
                'heatmap',
                'lamps',
                Radius(field='max_range_day', unit='meter'),
                Value(field='power', max=0),
                Orientation(field='orientation'),
                MaxValue(method='fix',
                         fix=150),
                HorizontalAngle(field='horizontal_angle'),
            ),
            Layer(
                'Voies',
                'node',
                'highways',
            ),
        ],
        'description': {
            'title': "Carte des passages piétons",
            'accroche': "Une carte interactive indiquant la qualité d'éclairage des passages piétons.",
            'intro': """""",
            'icon': 'buttons/contradiction.png',
            'href': '/map_desc/6',
        },
    }
