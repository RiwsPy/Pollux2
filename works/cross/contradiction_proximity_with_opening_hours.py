from . import Works_cross
from works import crossings, shops, trees
from formats.geojson import Geojson, Geo_Feature
from collections import defaultdict


class Cross(Works_cross):
    max_range = 25
    multiplier = 16
    filename = __file__

    def load(self, *teams, **kwargs):
        teams = teams or ([crossings, shops], [trees])
        super().load(*teams, **kwargs)

    def dump(self, filename: str = "", features: list = None) -> None:
        super().dump(features=self.new_features.features)

    def apply_algo(self):
        for blue_teammate, red_teammate, distance in self._iter_double_and_range():
            contradiction_node = Geo_Feature()

            item_intensity = defaultdict(int)
            intensity_value = self.multiplier / distance ** 2
            item_intensity['Jour'] += intensity_value
            if not blue_teammate['properties'].get('opening_hours'):
                item_intensity['Nuit'] += intensity_value
            item_intensity['Différence'] = item_intensity['Jour'] - item_intensity['Nuit']

            contradiction_node.position = ((blue_teammate.position + red_teammate.position) / 2).round(8)
            contradiction_node['properties'][self.value_attr] = item_intensity
            self.new_features.append(contradiction_node)
