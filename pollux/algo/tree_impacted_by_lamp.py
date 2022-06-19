from django.contrib.gis.geos import Polygon

from pollux.models.lamps import Lamps
from pollux.models.trees import Trees
from .georepartition_in_array import Repartition_point, adjacent_match
from .lamp_impact_tree import Cross as Lamp_cross


class Cross(Lamp_cross):
    def pre_algo(self, q1=None, q2=None):
        print('Prise en compte des arbres')
        self.q1 = q1 or Trees.objects.filter(position__within=Polygon.from_bbox(self.bound))
        self.reset_objects(self.q1)
        self.q1_array = Repartition_point(self.q1, self.bound, max_range=30).array

        self.q2 = q2 or Lamps.objects.filter(position__within=Polygon.from_bbox(self.bound))
        print('Prise en compte des luminaires')
        self.q2_array = Repartition_point(self.q2, self.bound, max_range=30).array

    def apply_algo(self) -> None:
        super().apply_algo()
        for tree, lamp in adjacent_match(self.q1_array, self.q2_array, max_case_range=1):
            day_impact = lamp.impact(tree, nb_lux=3, time='day')
            night_impact = lamp.impact(tree, nb_lux=3, time='night')
            if day_impact or night_impact:
                tree.day_impact = round(tree.day_impact + day_impact, 2)
                tree.night_impact = round(tree.night_impact + night_impact, 2)
                tree.save()
