from . import Default_cross
from pollux.models.lamps import Lamps
from pollux.models.trees import Trees
from .georepartition_in_array import Repartition_point, adjacent_match
from django.contrib.gis.geos import Polygon


class Cross(Default_cross):
    def load(self, *args, **kwargs) -> None:
        pass

    def pre_algo(self):
        print('Prise en compte des luminaires')
        lamps_queryset = Lamps.objects.filter(position__within=Polygon.from_bbox(self.bound))
        for lamp in lamps_queryset:
            if lamp.day_impact or lamp.night_impact:
                lamp.day_impact = 0
                lamp.night_impact = 0
                lamp.save()
        self.lamps_array = Repartition_point(Lamps.objects.all(), self.bound, max_range=30).array

        print('Prise en compte des arbres')
        trees_queryset = Trees.objects.filter(position__within=Polygon.from_bbox(self.bound))
        for tree in trees_queryset:
            if tree.day_impact or tree.night_impact:
                tree.day_impact = 0
                tree.night_impact = 0
                tree.save()
        self.trees_array = Repartition_point(Trees.objects.all(), self.bound, max_range=30).array

    def apply_algo(self) -> None:
        super().apply_algo()
        for lamp, tree in adjacent_match(self.lamps_array, self.trees_array, max_case_range=1):
            day_impact = lamp.impact(tree, nb_lux=3, time='day')
            night_impact = lamp.impact(tree, nb_lux=3, time='night')
            if day_impact or night_impact:
                lamp.day_impact = round(lamp.day_impact + day_impact, 2)
                lamp.night_impact = round(lamp.night_impact + night_impact, 2)
                lamp.save()
                tree.day_impact = round(tree.day_impact + day_impact, 2)
                tree.night_impact = round(tree.night_impact + night_impact, 2)
                tree.save()
