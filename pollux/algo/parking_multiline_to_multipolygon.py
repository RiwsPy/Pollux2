from . import Default_cross
from ..models.parking_public import Parking_public
from ..formats.geojson import Geojson
from ..utils import linestring_to_polygon


class Cross(Default_cross):
    dump_filename = 'db/parking_public_2D.json'
    model = Parking_public

    def pre_algo(self):
        print('Préparation des éléments...')
        self.ret_parkings = self.model.objects.all()

    def apply_algo(self):
        geo = Geojson()
        for parking_model, parking_dict in zip(self.ret_parkings,
                                               Parking_public.serialize(self.ret_parkings)['features']
                                               ):

            ret = []
            for line in parking_dict['geometry']['coordinates']:
                for positions in zip(line[:-1], line[1:]):
                    coordinates_polygon = self.polygon_coordinates(positions, parking_model)
                    if coordinates_polygon:
                        ret.append(coordinates_polygon)
            parking_dict['geometry']['coordinates'] = ret
            geo.append(parking_dict)
        geo.dump(self.dump_filename)

    @staticmethod
    def polygon_coordinates(positions, feature):
        return linestring_to_polygon([list(positions)], feature.width)
