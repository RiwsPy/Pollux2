from . import *


class Config(Default_Config):
    ID = 5
    LAYER_BASE = Layer('', '', '',
                       MaxValue(method='fix', fix=1, min=0.4),
                       Filters(position__within=[5.707430, 45.185546, 5.715208, 45.189024])
                       )
    DATA = {
        'options': Options(
            Zoom(init=17),
            Legend(name='Discontinuité %'),
        ),
        'layers': [
            Layer(
                'Discontinuité lumineuse',
                'heatmap',
                'lamps_incontinuite_lum.json',
                Gradient('LIGHT_COLORED'),
                Radius(fix=10),
                Blur(method='%', fix=10),
                IsActive(True),
                Value(field='intensity'),
            ),
            Layer(
                'Luminaires',
                'cluster',
                'lamps',
                Icon('LAMP'),
            ),
        ],
    }
