from . import Works_cross
from works import lamps, trees
import math


class Cross(Works_cross):
    max_range = 25
    multiplier = 0.3
    filename = __file__

    def load(self, *teams, **kwargs):
        teams = teams or ([lamps], [trees])
        super().load(*teams, **kwargs)

    def dump(self, filename: str = "", features: list = None) -> None:
        super().dump(features=self.teams[0].features)

    def apply_algo(self):
        # TODO: ratio impact selon la température de couleur
        # TODO: ratio impact selon % de hauteur de l'arbre éclairé (distance - hauteurS - angle d'incidence)
        for blue_teammate, red_teammate, distance in self._iter_double_and_range():
            intensity_value = self.lamp_impact(blue_teammate, red_teammate, distance)

            blue_teammate['properties'][self.value_attr]['Jour'] += intensity_value
            blue_teammate['properties'][self.value_attr]['Nuit'] += intensity_value * (1 - blue_teammate.lowering_night / 100)
            blue_teammate['properties'][self.value_attr]['Différence'] += intensity_value* (1 - (1 - blue_teammate.lowering_night / 100))

    @staticmethod
    def lamp_max_range(feature) -> float:
        return feature.height * math.atan(20)

    def lamp_illuminated_height(self, lamp, distance) -> float:
        lamp_height = lamp.height
        if lamp_height < 1: # posé au sol
            lamp_height = 12
        try:
            return max(0, lamp_height * (1 - distance / self.lamp_max_range(lamp)))
        except ZeroDivisionError:
            return lamp_height

    def lamp_impact(self, blue_teammate, red_teammate, distance) -> float:
        if self.lamp_without_impact(blue_teammate, red_teammate, distance):
            return 0

        diff_lum_tree_height = max(blue_teammate.height - red_teammate.height, 0)
        square_distance = diff_lum_tree_height ** 2 + distance ** 2
        illuminated_height = self.lamp_illuminated_height(blue_teammate, distance)
        if illuminated_height <= 0:
            return 0

        illuminated_ratio = min(1, illuminated_height / red_teammate.height)
        if illuminated_ratio >= 0.5:  # feuilles
            square_distance = diff_lum_tree_height ** 2 + max(0, distance - 1) ** 2

        intensity_value = (self.power_impact(blue_teammate) *
                                   illuminated_ratio / max(1, square_distance)
                                   ) * self.multiplier

        intensity_value *= self.color_impact(blue_teammate.colour)

        return intensity_value

    def lamp_without_impact(self, blue_teammate, red_teammate, distance) -> bool:
        diff_lum_tree_height = max(blue_teammate.height - red_teammate.height, 0)
        square_distance = diff_lum_tree_height ** 2 + distance ** 2
        return blue_teammate.on_motion or square_distance >= self.lamp_max_range(blue_teammate) ** 2

    @staticmethod
    def color_impact(colour) -> float:
        # impact compris entre 60 (2000K) (ratio 0.75) et 80 (6000K) (ratio 1)
        return (60 + 20 * max(0, min(4000, colour - 2000)) / 4000) / 80

    @staticmethod
    def power_impact(feature) -> int:
        return feature.power
