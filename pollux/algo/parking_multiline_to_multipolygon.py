from . import Default_cross
from ..models.parking_public import Parking_public
from ..formats.geojson import Geojson
from ..utils import linestring_to_polygon


class Cross(Default_cross):
    def pre_algo(self):
        print('Préparation des parkings...')
        self.ret_parkings = Parking_public.objects.all()

    def apply_algo(self):
        geo = Geojson()
        for parking_model, parking_dict in zip(self.ret_parkings,
                                               Parking_public.serialize(self.ret_parkings)['features']
                                               ):
            parking_dict['geometry']['coordinates'] = \
                linestring_to_polygon(
                    parking_dict['geometry']['coordinates'],
                    parking_model.width
                )
            geo.append(parking_dict)
        geo.dump('db/parking_public_2D.json')
