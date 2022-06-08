from . import *


class Config(Default_Config):
    ID = 7
    LAYER_BASE = Layer('', '', '',
                       Filters(position__within=[5.714337, 45.182177, 5.722755, 45.184826])
                       )
    DATA = {
        'options': Options(
            Zoom(max=22, init=18),
            Legend(name="Où ne pas planter des arbres"),
            TileLayer(TileLayer.OSM),
        ),
        'layers': [
            Layer(
                'Arbres',
                'node',
                'trees',
                Icon('TREE'),
                Filters(position__dwithin='parking_public')
            ),
            Layer(
                'Zones éclairées',
                'heatmap',
                'lamps',
                Gradient('BLUEBELT'),
                Radius(field='max_range_day', unit='meter'),
                Value(field='impact_tree_on_ground', max=30),
                Orientation(field='orientation'),
                Blur(unit='%', fix=30),
                MaxValue(method='fix', fix=30),
                HorizontalAngle(field='horizontal_angle'),
                Filters(position__dwithin='parking_public')
            ),
            Layer(
                'Parkings publics',
                'node',
                'parking_public',
                Style(color="#007800", opacity=0.75, weight=5)
            ),
            Layer(
                "Parkings publics absents d'OSM",
                'node',
                'parking_lane_not_in_osm.json',
                Style(color="#007800", opacity=0.75, weight=5)
            ),
        ]
    }
