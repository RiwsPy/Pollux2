from . import Works_cross
from works import lamps, crossings


class Cross(Works_cross):
    max_range = 25
    filename = __file__

    def load(self, *teams, **kwargs):
        lamps.Works.filename = 'lamps_with_orientation'
        lamps.Works.file_ext = 'json'
        lamps.Works.fake_request = True
        teams = teams or ([crossings], [lamps])
        super().load(*teams, **kwargs)

    def dump(self, filename: str = "", features: list = None) -> None:
        super().dump(features=self.teams[0].features)

    def apply_algo(self):
        # en fonction de la distance et de l'IRC du luminaire
        for blue_teammate, red_teammate, distance in self._iter_double_and_range():
            square_distance = red_teammate.height ** 2 + distance ** 2
            if square_distance <= self.max_range ** 2:

                red_orientation = red_teammate._pollux_values['orientation']
                if red_orientation is not None:  # luminaire orienté
                    blue_red_alignment = red_teammate.position.orientation(blue_teammate.position)
                    blue_and_red_are_aligned = abs(red_orientation - blue_red_alignment) <= 90 or \
                                               abs(red_orientation - blue_red_alignment) >= 270
                    if not blue_and_red_are_aligned:
                        continue
                    multicator = 2
                else:
                    multicator = 1

                night_impact = 100 - red_teammate.lowering_night
                intensity_value = multicator * red_teammate.irc / square_distance

                blue_teammate['properties'][self.value_attr]['Jour'] += intensity_value
                blue_teammate['properties'][self.value_attr]['Nuit'] += intensity_value*night_impact/100
                blue_teammate['properties'][self.value_attr]['Différence'] += intensity_value - intensity_value*night_impact/100
