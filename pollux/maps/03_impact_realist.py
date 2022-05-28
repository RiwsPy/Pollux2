from . import *


class Config(Default_Config):
    ID = 3

    LAYER_BASE = Layer('', '', '',
                       Radius(unit='meter'),
                       Blur(fix=45, unit='%'),
                       MaxValue(method='fix', fix=10),
                       )

    DATA = {
        'href': '/map/3',

        'options': Options(
            Legend(name='Impact réaliste'),
            Zoom(max=19),
            bbox=[5.717633, 45.182596, 5.734348, 45.185410],
        ),
        'layers': [
            Layer(
                'Eclairage (densité)',
                'heatmap',
                'lamps',
                Radius(field='max_range_day', unit='meter'),
                Value(fix=10),
                Orientation(field='orientation'),
                HorizontalAngle(field='horizontal_angle'),
            ),
            Layer(
                'Luminaire (Impact- Jour)',
                'heatmap',
                'lamps',
                IsActive(True),
                Radius(field='max_range_day', unit='meter'),
                Value(field='day_impact'),
                Orientation(field='orientation'),
                HorizontalAngle(field='horizontal_angle'),
            ),
            Layer(
                'Luminaire (Impact - Nuit)',
                'heatmap',
                'lamps',
                Radius(field='max_range_night', unit='meter'),
                Value(field='night_impact'),
                Orientation(field='orientation'),
                HorizontalAngle(field='horizontal_angle'),
            ),
            Layer(
                'Luminaires',
                'cluster',
                'lamps',
                Icon('markers/lamp.png')
            ),
            Layer(
                'Arbre (Impact - Jour)',
                'heatmap',
                'trees',
                Value(field='day_impact'),
                Radius(fix=15, unit='meter'),
            ),
            Layer(
                'Arbre (Impact - Nuit)',
                'heatmap',
                'trees',
                Value(field='night_impact'),
                Radius(fix=15, unit='meter'),
            ),
            Layer(
                'Arbres',
                'cluster',
                'trees',
                Icon('TREE')
            ),
        ],
        'description': {
            'title': "Carte Impact réaliste",
            'icon': 'buttons/impact.png',
        }
    }
