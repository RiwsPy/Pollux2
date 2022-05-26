from pollux.formats.geojson import Geojson, Geo_Feature
from pollux.formats.position import Position
from pollux.models.lamps import Lamps
from pollux.works import MAX_BOUND_LNG_LAT
from .georepartition_in_array import Repartition_point, adjacent_match
from . import Default_cross


class Cross(Default_cross):
    max_range = 25

    def pre_algo(self):
        print('Préparation des luminaires...')
        self.ret_lamps = Repartition_point(Lamps.objects.all(),
                                           bound=MAX_BOUND_LNG_LAT,
                                           max_range=self.max_range)

    def apply_algo(self):
        geo = Geojson()
        for lamp1, lamp2 in adjacent_match(self.ret_lamps.array, self.ret_lamps.array, max_case_range=1):
            distance = Position(lamp1.position).distance(Position(lamp2.position))
            if distance < 25:
                continue
            continuite_value = self.continuite_lum(lamp1, lamp2)
            discontinuite_value = max(0, (1 - continuite_value) / distance * 25)
            if discontinuite_value < 0.4:
                continue
            feat = Geo_Feature()
            feat.position = (Position(lamp1.position) + Position(lamp2.position))/2
            feat.intensity = round(discontinuite_value, 2)
            geo.append(feat)

        geo.dump('db/lamps_incontinuite_lum.json')

    @staticmethod
    def continuite_lum(lamp1, lamp2) -> float:
        min_value = min(lamp1.lux_average_on_ground, lamp2.lux_average_on_ground)
        max_value = max(lamp1.lux_average_on_ground, lamp2.lux_average_on_ground)
        try:
            return min_value / max_value
        except ZeroDivisionError:
            return 1
