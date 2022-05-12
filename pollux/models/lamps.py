from django.contrib.gis.db import models
from .default import Default_model
import math
from pollux.formats.position import Position


class Lamps(Default_model):
    class Meta:
        app_label = "pollux"

    code = models.CharField(max_length=20, default="")
    height = models.FloatField(default=8.0)
    irc = models.IntegerField(default=75)
    power = models.IntegerField(default=150)
    colour = models.IntegerField(default=5000)
    on_motion = models.BooleanField(default=False)
    lowering_night = models.IntegerField(default=0)
    orientation = models.FloatField(default=-1.0)
    nearest_way_dist = models.FloatField(default=-1.0)
    day_impact = models.FloatField(default=0.0)
    night_impact = models.FloatField(default=0.0)

    @property
    def way_type(self) -> str:
        if self.height < 5.0 or self.on_motion:
            return 'footway'
        return 'road'

    @property
    def angle_incidence(self) -> float:
        return 70.0

    @property
    def lumens_per_watt(self) -> int:
        return 100

    def distance_with_lux(self, nb_lux: int = 5, time: str = 'day') -> float:
        # distance où le nombre de lux au sol == nb_lux
        hypotenuse = (self.lumens_per_watt * self.power_impact(time) *
                      math.cos(math.radians(self.angle_incidence)) / nb_lux) ** 0.5
        return hypotenuse * math.cos(math.radians(90 - self.angle_incidence))

    @property
    def height_max_range(self) -> float:
        if self.height <= 1:
            return 20.0
        return self.height * math.tan(math.radians(self.angle_incidence))

    def max_range(self, nb_lux: int = 5, time: str = 'day') -> float:
        # considéré comme impact faible si < 5lux
        # distance où lux périphérique == 5
        min_lux_distance = self.distance_with_lux(nb_lux, time=time)
        return min(self.height_max_range, min_lux_distance)

    def illuminated_height_at(self, distance: float) -> float:
        # hauteur du flux lumineux à X mètres
        if self.height <= 1.0:
            return math.tan(math.radians(self.angle_incidence)) * distance
        return max(0.0, self.height * (1 - distance/self.height_max_range))

    def is_without_impact(self, illuminated_object, distance, nb_lux: int = 5, time: str = 'day') -> bool:
        diff_lum_tree_height = max(self.height - illuminated_object.height, 0)
        square_distance = diff_lum_tree_height ** 2 + distance ** 2

        return self.on_motion or square_distance >= self.max_range(nb_lux=nb_lux, time=time) ** 2

    def impact(self, illuminated_object, nb_lux: int, time: str) -> float:
        distance = illuminated_object.distance_from(self)
        if self.is_without_impact(illuminated_object, distance, nb_lux=nb_lux, time=time) or \
                self.illuminated_height_at(distance) <= 0:
            return 0.0

        diff_lum_tree_height = max(self.height - illuminated_object.height, 0)
        square_distance = diff_lum_tree_height ** 2 + distance ** 2

        intensity_value = (self.aligned_power_impact(illuminated_object, time=time) /
                           max(1, square_distance)
                           )

        return intensity_value * illuminated_object.color_impact(self.colour)

    def power_impact(self, time: str = 'day') -> float:
        power_value = self.power
        if time != 'day':
            power_value = power_value * (1 - self.lowering_night / 100)

        return power_value

    def aligned_power_impact(self, other_object, time: str = 'day') -> int:
        power_impact = 0
        if not self.is_oriented:
            power_impact = self.power_impact(time=time)
        elif self.is_aligned_with(other_object):
            power_impact = self.power_impact(time=time) * 2

        return power_impact

    def is_aligned_with(self, other_object) -> bool:
        if not self.is_oriented or self.position == other_object.position:
            return True

        objects_alignment = Position(self.position).orientation(other_object.position)
        return not (90 < abs(objects_alignment - self.orientation) < 270)

    @property
    def is_oriented(self) -> bool:
        return self.orientation != -1.0
