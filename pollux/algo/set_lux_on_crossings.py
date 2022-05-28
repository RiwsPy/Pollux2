from . import Default_cross
from pollux.models.lamps import Lamps
from pollux.models.crossings import Crossings
from .georepartition_in_array import Repartition_point, adjacent_match
from django.contrib.gis.geos import Polygon


class Cross(Default_cross):
    def load(self, *args, **kwargs) -> None:
        pass

    def pre_algo(self):
        print('Prise en compte des luminaires')
        # lamps_queryset = Lamps.objects.filter(position__within=Polygon.from_bbox(self.bound))
        self.lamps_array = Repartition_point(Lamps.objects.all(), self.bound, max_range=30).array

        print('Prise en compte des passages piétons')
        crossings_queryset = Crossings.objects.filter(position__within=Polygon.from_bbox(self.bound))
        for crossing in crossings_queryset:
            crossing.illuminance_day = 0.0
            crossing.illuminance_irc_day = 0.0
            crossing.illuminance_night = 0.0
            crossing.illuminance_irc_night = 0.0
            crossing.save()
        self.crossings_array = Repartition_point(Crossings.objects.all(), self.bound, max_range=30).array

    def apply_algo(self) -> None:
        super().apply_algo()
        for lamp, crossing in adjacent_match(self.lamps_array, self.crossings_array, max_case_range=1):
            if lamp.height <= 1:
                continue
            day_impact = lamp.impact(crossing, nb_lux=5, time='day')
            night_impact = lamp.impact(crossing, nb_lux=5, time='night')
            if day_impact or night_impact:
                day_impact_irc = day_impact * min(100, lamp.irc) / 100
                night_impact_irc = night_impact * min(100, lamp.irc) / 100
                crossing.illuminance_day = round(crossing.illuminance_day + day_impact, 2)
                crossing.illuminance_irc_day = round(crossing.illuminance_irc_day + day_impact_irc, 2)
                crossing.illuminance_night = round(crossing.illuminance_night + night_impact, 2)
                crossing.illuminance_irc_night = round(crossing.illuminance_irc_night + night_impact_irc, 2)
                crossing.save()
