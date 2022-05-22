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
            bbox=[5.717633, 45.182596, 5.734348, 45.185410],
        ),
        'layers': [
            Layer(
                'Eclairage (densité)',
                'heatmap',
                'lamps',
                IsActive(True),
                Orientation(field='orientation'),
                MaxValue(method='fix', fix=3),
            ),
            Layer(
                'Luminaire (Impact- Jour)',
                'heatmap',
                'lamps',
                Value(field='day_impact'),
                Orientation(field='orientation'),
            ),
            Layer(
                'Luminaire (Impact - Nuit)',
                'heatmap',
                'lamps',
                Value(field='night_impact'),
                Orientation(field='orientation'),
            ),
            Layer(
                'Luminaires',
                'cluster',
                'lamps',
                Icon('Lamp')
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
