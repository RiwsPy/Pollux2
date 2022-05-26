from . import *


class Config(Default_Config):
    ID = 5
    LAYER_BASE = Layer('', '', '',
                       MaxValue(max=1, min=0.4)
                       )
    DATA = {
        'options': Options(
            Zoom(init=17),
            Legend(name='Discontinuité %'),
            bbox=[5.707430, 45.185546, 5.715208, 45.189024],
        ),
        'layers': [
            Layer(
                'Discontinuité lumineuse',
                'heatmap',
                'lamps_incontinuite_lum.json',
                Gradient('LIGHT_COLORED'),
                Radius(fix=10),
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
