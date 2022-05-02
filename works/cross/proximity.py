from . import Works_cross
from works import churchs, vending_machines


class Cross(Works_cross):
    max_range = 5000
    multiplier = 100
    filename = __file__

    def load(self, *teams, **kwargs):
        teams = teams or ([churchs], [vending_machines])
        super().load(*teams, **kwargs)

    def dump(self, filename: str = "", features: list = None) -> None:
        super().dump(features=self.teams[0].features)

    def apply_algo(self):
        for blue_teammate, red_teammate, distance in self._iter_double_and_range():
            blue_teammate['properties'][self.value_attr]['Contradiction'] += self.multiplier / distance
