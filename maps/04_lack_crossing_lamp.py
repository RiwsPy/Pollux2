from . import Default_Config


class Config(Default_Config):
    ID = "4"
    DATA = {
        'title': 'Eclairage des passages piétons',

        'options': {'draw': 0, 'legend': {
            'name': 'Manque'}},
        'layers': [
            {
                'layerName': 'Jour',
                'layerType': 'heatmap_intensity',
                'filename': 'cross/quality_of_lamps--crossings--lamps_with_orientation--25.json',
            },
            {
                'layerName': 'Nuit',
                'layerType': 'heatmap_intensity',
                'filename': 'cross/quality_of_lamps--crossings--lamps_with_orientation--25.json',
            },
            {
                'layerName': 'Différence',
                'layerType': 'heatmap_intensity',
                'filename': 'cross/quality_of_lamps--crossings--lamps_with_orientation--25.json',
            },
            {
                'layerName': 'Luminaires',
                'layerType': 'cluster',
                'filename': 'lamps_output.json',
                'icon': 'markers/lamp.png',
                'entityType': 'Lamp',
            },
            {
                'layerName': 'Passages piétons',
                'layerType': 'cluster',
                'filename': 'cross/quality_of_lamps--crossings--lamps_with_orientation--25.json',
                'icon': 'markers/pedestrian.png',
                'entityType': 'Crossing',
            },
        ]}
