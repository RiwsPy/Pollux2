from . import *


class Config(Default_Config):
    ID = 4
    LAYER_BASE = Layer('', '', '',
                       MaxValue(method='part%',
                                fix=80)
                       )
    DATA = {
        'options': Options(
            Zoom(max=19, init=18),
            Legend(name='Dépense €/an'),
            bbox=[5.717633, 45.182596, 5.734348, 45.185410],
        ),
        'layers': [
            Layer(
                'Luminaires (Chaleur)',
                'heatmap',
                'lamps',
                Gradient('BLUEBELT'),
                Radius(field='max_range_night', unit='pixel'),
                IsActive(True),
                Value(field='expense'),
            ),
            Layer(
                'Luminaires',
                'cluster',
                'lamps',
                Icon('LAMP'),
            ),
        ],
        'description': {
            'title': "Carte de dépense",
            'accroche': "Une carte interactive mesurant le coût financier des luminaires de l'espace public.",
            'intro': """Cette carte permet de visualiser où l'argent part mais pas de le faire revenir.""",
            'icon': 'buttons/contradiction.png',
            'href': '/map_desc/4',
        },
    }
