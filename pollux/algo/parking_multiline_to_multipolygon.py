from . import Default_cross
from ..models.parking_public import Parking_public
from ..formats.geojson import Geojson, Geo_Feature
from ..utils import linestring_to_polygon


class Cross(Default_cross):
    """
        Transforme les segments de parkings de voirie en polygone, les sauvegardent dans un fichier de format geojson.
        Le fichier en question peut être importé sur d'autres outils pour finition.
    """
    dump_filename = 'db/parking_public_2D.json'
    model = Parking_public

    def pre_algo(self):
        print('Préparation des éléments...')
        self.ret_parkings = self.model.objects.all()

    def apply_algo(self):
        geo = Geojson()
        for parking_model, parking_dict in zip(self.ret_parkings,
                                               self.model.serialize(self.ret_parkings)['features']
                                               ):
            parking_dict['properties'] = {}
            for line in parking_dict['geometry']['coordinates']:
                for positions in zip(line[:-1], line[1:]):
                    coordinates_polygon = self.polygon_coordinates(positions, parking_model)
                    if coordinates_polygon:
                        new_geof = Geo_Feature()
                        new_geof.position = coordinates_polygon
                        new_geof['geometry']['type'] = 'Polygon'
                        geo.append(new_geof)

        geo.dump(self.dump_filename)

    @staticmethod
    def polygon_coordinates(positions, feature):
        return linestring_to_polygon([list(positions)], feature.width)
