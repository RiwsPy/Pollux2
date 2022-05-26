from . import *


class Config(Default_Config):
    ID = 3

    LAYER_BASE = Layer('', '', '',
                       Radius(unit='meter'),
                       )

    DATA = {
        'href': '/map/3',

        'options': Options(
            Legend(name='Impact réaliste'),
            Zoom(max=19, min=12),
            bbox=[5.717633, 45.182596, 5.734348, 45.185410],
        ),
        'layers': [
            Layer(
                'Eclairage (densité)',
                'heatmap',
                'lamps',
                IsActive(True),
                Radius(field='max_range_day', unit='meter'),
                Orientation(field='orientation'),
                MaxValue(method='fix', fix=3),
            ),
            Layer(
                'Arbres (JSON)',
                'heatmap',
                'lamps_output.json',
                MaxValue(method='part%', fix=80),
                Value(field='irc'),
            ),
            Layer(
                'Luminaire (Impact- Jour)',
                'heatmap',
                'lamps',
                Radius(field='max_range_day', unit='meter'),
                Value(field='day_impact'),
                Orientation(field='orientation'),
            ),
            Layer(
                'Luminaire (Impact - Nuit)',
                'heatmap',
                'lamps',
                Radius(field='max_range_night', unit='meter'),
                Value(field='night_impact'),
                Orientation(field='orientation'),
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
                Radius(fix=10),
            ),
            Layer(
                'Arbre (Impact - Nuit)',
                'heatmap',
                'trees',
                Value(field='night_impact'),
                Radius(fix=10),
            ),
            Layer(
                'Arbres',
                'cluster',
                'trees',
                Icon('TREE')
            ),
        ],
        'description': {
            'title': "Carte test",
            'icon': 'buttons/recommandation.png',
        }
    }
