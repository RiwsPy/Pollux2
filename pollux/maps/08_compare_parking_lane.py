from . import *
from django.db.models import Q


class Config(Default_Config):
    ID = 8
    LAYER_BASE = Layer('', '', '',
                       Filters(position__within=[5.714337, 45.182177, 5.722755, 45.184826])
                       )
    DATA = {
        'options': Options(
            Zoom(max=22, init=18),
            Legend(name=""),
            TileLayer(TileLayer.OSM),
        ),
        'layers': [
            Layer(
                'Parkings publics',
                'node',
                'parking_public',
                Style(color="#007800", opacity=0.75, weight=5)
            ),
            Layer(
                "Parkings publics d'OSM",
                'node',
                'highways',
                Style(color="#780000", opacity=0.75, weight=5),
                Q=~Q(parking_r='no') & ~Q(parking_r='unknown') & ~Q(parking_r='yes') |
                  ~Q(parking_l='no') & ~Q(parking_l='unknown') & ~Q(parking_l='yes')
            ),
        ]
    }
