from .parking_multiline_to_multipolygon import Cross as SuperCross
from ..models.highways import Highways
from ..utils import linestring_to_polygon


class Cross(SuperCross):
    """
        Transforme les segments de route et les parkings de voirie en polygone, les sauvegardent dans un fichier de format geojson.
        Le fichier en question peut être importé sur d'autres outils pour finition.
        Le résultat ne prend pas en compte le côté où le parking est situé : le polygone est centré sur la route.
    """
    dump_filename = 'db/highways_2D.json'
    model = Highways

    @staticmethod
    def polygon_coordinates(positions, feature):
        if feature.width_car + feature.width_parking == 0:
            return None
        return linestring_to_polygon([list(positions)], feature.width_car + feature.width_parking)
