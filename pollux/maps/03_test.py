from . import Default_Config


class Config(Default_Config):
    ID = 3
    DATA = {
        'href': '/map/3',

        'options': {
            'bbox': [5.717633, 45.182596, 5.734348, 45.185410],
            'legend': {
                'name': 'Impact réaliste'},
            'blur': 15,
        },
        'layers': [
            {
                'name': 'Eclairage (densité)',
                'isActive': 1,
                'layerType': 'heatmap',
                'maxValueMethod': 'zoom_depend',
                'orientation': {
                    'field': 'orientation',
                },
                'maxValueDefault': 3,
                'radius': {
                    'unit': 'meter',
                },
                'filename': 'lamps',
            },
            {
                'name': 'Luminaire (Impact- Jour)',
                'value': {
                    'field': 'day_impact',
                },
                'layerType': 'heatmap',
                'maxValueMethod': 'zoom_depend',
                'orientation': {
                    'field': 'orientation',
                },
                'radius': {
                    'unit': 'meter',
                },
                'filename': 'lamps',
            },
            {
                'name': 'Luminaire (Impact - Nuit)',
                'value': {
                    'field': 'night_impact',
                },
                'maxValueMethod': 'zoom_depend',
                'layerType': 'heatmap',
                'orientation': {
                    'field': 'orientation',
                },
                'filename': 'lamps',
                'radius': {
                    'unit': 'meter',
                },
            },
            {
                'name': 'Luminaires',
                'layerType': 'cluster',
                'filename': 'lamps',
                'icon': 'markers/lamp.png',
            },
            {
                'name': 'Arbre (Impact - Jour)',
                'value': {
                    'field': 'day_impact',
                },
                'maxValueMethod': 'zoom_depend',
                'layerType': 'heatmap',
                'filename': 'trees',
                'radius': {
                    'unit': 'meter',
                    'fix': 10,
                },
            },
            {
                'name': 'Arbre (Impact - Nuit)',
                'value': {
                    'field': 'night_impact',
                },
                'maxValueMethod': 'zoom_depend',
                'layerType': 'heatmap',
                'filename': 'trees',
                'radius': {
                    'unit': 'meter',
                    'fix': 10,
                },
            },
            {
                'name': 'Arbres',
                'layerType': 'cluster',
                'filename': 'trees',
                'icon': 'markers/tree.png',
            },
        ],
        'description': {
            'title': "Carte test",
            'icon': 'buttons/recommandation.png',
        }
    }
