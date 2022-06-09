from .parking_multiline_to_multipolygon import Cross as SuperCross
from ..models.highways import Highways
from ..utils import linestring_to_polygon
from ..formats.geojson import Geojson, Geo_Feature


class Cross(SuperCross):
    dump_filename = 'db/highways_2D.json'
    model = Highways

    @staticmethod
    def polygon_coordinates(positions, feature):
        if feature.width_car + feature.width_parking == 0:
            return None
        return linestring_to_polygon([list(positions)], feature.width_car + feature.width_parking)
