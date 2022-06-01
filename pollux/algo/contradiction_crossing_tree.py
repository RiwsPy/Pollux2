from pollux.formats.geojson import Geojson, Geo_Feature
from pollux.formats.position import Position
from pollux.models.crossings import Crossings
from pollux.models.trees import Trees
from pollux.works import MAX_BOUND_LNG_LAT
from .georepartition_in_array import Repartition_point, adjacent_match
from . import Default_cross


class Cross(Default_cross):
    max_range = 25

    def pre_algo(self):
        print('Préparation des passages piéton...')
        self.ret_crossings = Repartition_point(Crossings.objects.all(),
                                           bound=MAX_BOUND_LNG_LAT,
                                           max_range=self.max_range)

        print('Préparation des arbres...')
        self.ret_trees = Repartition_point(Trees.objects.all(),
                                           bound=MAX_BOUND_LNG_LAT,
                                           max_range=self.max_range)

    def apply_algo(self):
        geo = Geojson()
        for cross, tree in adjacent_match(self.ret_crossings.array, self.ret_trees.array, max_case_range=1):
            distance = Position(cross.position).distance(Position(tree.position))
            contradiction = 16 / distance**2
            feat = Geo_Feature()
            feat.position = (Position(cross.position) + Position(tree.position))/2
            feat.intensity = round(contradiction, 2)
            geo.append(feat)

        geo.dump('db/contradiction_crossing_tree.json')
