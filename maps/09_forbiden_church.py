from . import Default_Config


class Config(Default_Config):
    ID = "hidden"
    DATA = {
        'title': 'Églises mal protégées',

        'options': {'draw': 0, 'radius': 100, 'legend': {
            'name': 'Églises mal protégées'}},
        'layers': [
            {
                'layerName': 'Contradiction',
                'layerType': 'heatmap_intensity',
                'filename': 'cross/proximity--churchs--vending_machine--5000.json',
            },
            {
                'layerName': 'Églises',
                'layerType': 'node',
                'filename': 'cross/proximity--churchs--vending_machine--5000.json',
            },
            {
                'layerName': 'Machines démoniaques',
                'layerType': 'node',
                'filename': 'vending_machine_output.json',
            },
        ]}
