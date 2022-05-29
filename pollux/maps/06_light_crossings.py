from . import *


class Config(Default_Config):
    ID = 6
    LAYER_BASE = Layer('', '', '',
                       Gradient('BLUEBELT'),
                       Blur(unit='%', fix=40),
                       MaxValue(method='fix',
                                fix=20),
                       Value(max=20)
                       )
    DATA = {
        'options': Options(
            Zoom(max=20, init=18),
            Legend(name="Manque d'éclairage"),
            bbox=[5.714337, 45.182177, 5.722755, 45.184826],
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
                'node',
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
            'accroche': "Une carte interactive indiquant les passages piétons peu éclairés.",
            'intro': """""",
            'icon': 'buttons/contradiction.png',
            'href': '/map_desc/6',
        },
    }
