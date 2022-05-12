from . import Default_Config


class Config(Default_Config):
    ID = 2
    DATA = {
        'href': '/map/2',

        'options': {
            'bbox': [5.7200864, 45.1786431, 5.7303789, 45.1889222],
            'radius': {
                # 'fix': 20,
                'unit': 'meter'
            },
            'legend': {
                'name': 'Température de couleur'},
            'blur': 0,
            'gradient': {
                0.3333: '#FF880E',
                0.4166: '#FF9F46',
                0.5: '#FFB16D',
                0.6666: '#FFCDA6',
                0.8333: '#FFE4CD',
                1.0: '#FFF6EC',
            },
        },
        'layers': [
            {
                'name': 'Températeur de couleur',
                'value': {
                    'field': 'colour',
                },
                'isActive': 1,
                'layerType': 'heatmap',
                'filename': 'lamps',
                'maxValueDefault': 6000,
            },
        ],
        'description': {
            'title': "Carte de couleur",
            'icon': 'buttons/contradiction.png',
        }
    }
