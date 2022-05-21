from . import *


class Config(Default_Config):
    ID = 2
    DATA = {
        'href': '/map/2',

        'options': {
            'bbox': [5.7200864, 45.1786431, 5.7303789, 45.1889222],
            **Legend(name='Température de couleur'),
            },
        'layers': [
            Layer(
                'Températeur de couleur',
                'heatmap',
                'lamps',
                Value(field='colour'),
                IsActive(True),
                Radius(unit='meter'),
                Blur(0),
                maxValueDefault=6000,
                gradient={
                    0.3333: '#FF880E',
                    0.4166: '#FF9F46',
                    0.5: '#FFB16D',
                    0.6666: '#FFCDA6',
                    0.8333: '#FFE4CD',
                    1.0: '#FFF6EC',
                }
            ),
        ],
        'description': {
            'title': "Carte de couleur",
            'icon': 'buttons/contradiction.png',
        }
    }
