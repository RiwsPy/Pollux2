from . import Works_cross
from works import lamps, trees


class Cross(Works_cross):
    max_range = 25
    multiplier = 9
    filename = __file__

    def load(self, *teams, **kwargs):
        teams = teams or ([trees], [lamps])
        super().load(*teams, **kwargs)

    def dump(self, filename: str = "", features: list = None) -> None:
        super().dump(features=self.teams[0].features)

    def apply_algo(self):
        for blue_teammate, red_teammate, distance in self._iter_double_and_range():
            diff_lum_tree_height = max(red_teammate.height - blue_teammate.height, 0)
            square_distance = diff_lum_tree_height ** 2 + distance ** 2
            if square_distance <= self.max_range ** 2:
                intensity_value = self.multiplier / square_distance
                blue_teammate['properties'][self.value_attr]['Base'] += intensity_value

                if red_teammate.colour > 2500 and not red_teammate.on_motion:
                    night_impact = 100 - red_teammate.lowering_night
                    blue_teammate['properties'][self.value_attr]['Jour'] += intensity_value
                    blue_teammate['properties'][self.value_attr]['Nuit'] += intensity_value * night_impact / 100
