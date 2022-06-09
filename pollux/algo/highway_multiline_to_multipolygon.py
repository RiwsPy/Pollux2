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
        if feature.name == 'Rue Marx Dormoy':
            print(feature.width_car, feature.oneway)
        return linestring_to_polygon([list(positions)], feature.width_car + feature.width_parking)

    def apply_algo(self):
        geo = Geojson()
        for parking_model, parking_dict in zip(self.ret_parkings,
                                               Highways.serialize(self.ret_parkings)['features']
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
