from . import Default_cross
from pollux.models.lamps import Lamps
from pollux.models.trees import Trees
from .georepartition_in_array import Repartition_point, adjacent_match
from django.contrib.gis.geos import Polygon
from django.db.models import F


class Cross(Default_cross):
    def pre_algo(self, q1=None, q2=None):
        self.q1 = q1 or Lamps.objects.filter(position__within=Polygon.from_bbox(self.bound))
        print('Prise en compte des luminaires')
        Lamps.reset_queryset(self.q1, "day_impact", "night_impact")
        self.q1_array = Repartition_point(self.q1, self.bound, max_range=30).array

        print('Prise en compte des arbres')
        self.q2 = q2 or Trees.objects.filter(position__within=Polygon.from_bbox(self.bound))
        self.q2_array = Repartition_point(self.q2, self.bound, max_range=30).array

    def apply_algo(self) -> None:
        super().apply_algo()
        for lamp, tree in adjacent_match(self.q1_array, self.q2_array, max_case_range=1):
            day_impact = lamp.impact(tree, nb_lux=3, time='day')
            night_impact = lamp.impact(tree, nb_lux=3, time='night')
            if day_impact or night_impact:
                lamp.day_impact = F("day_impact") + day_impact
                lamp.night_impact = F("night_impact") + night_impact
                lamp.save()
