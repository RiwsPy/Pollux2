from . import Works_cross
from works import lamps, trees
from works.cross import impact_of_lamps


class Cross(impact_of_lamps.Cross):
    max_range = 25
    filename = __file__

    def load(self, *teams, **kwargs):
        lamps.Works.filename = 'lamps_with_orientation'
        lamps.Works.file_ext = 'json'
        lamps.Works.fake_request = True
        teams = teams or ([lamps], [trees])
        super().load(*teams, **kwargs)

    def power_impact(self, feature) -> int:
        if not self.lamp_has_orientation(feature):
            return feature.power
        return feature.power*2

    def lamp_without_impact(self, blue_teammate, red_teammate, distance) -> bool:
        blue_orientation = blue_teammate._pollux_values['orientation']
        if self.lamp_has_orientation(blue_teammate):
            return False

        blue_red_alignment = blue_teammate.position.orientation(red_teammate.position)
        blue_and_red_are_aligned = abs(blue_red_alignment - blue_orientation) <= 90 or \
                                   abs(blue_red_alignment - blue_orientation) >= 270

        return super().lamp_without_impact(blue_teammate, red_teammate, distance) and \
               not blue_and_red_are_aligned

    @staticmethod
    def lamp_has_orientation(lamp) -> bool:
        # _pollux_values est un defaultdict(int) par défaut et type(orientation) == float
        # un luminaire sans orientation aura une valeur == 0
        # un luminaire avec une orientation à 0 aura une valeur == 0.0
        return type(lamp._pollux_values['orientation']) is float
