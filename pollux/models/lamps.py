from django.contrib.gis.db import models
from .default import Default_model
import math
from pollux.formats.position import Position


class Lamps(Default_model):
    class Meta:
        app_label = "pollux"
        verbose_name = "Luminaire"

    code = models.CharField(max_length=20, default="")
    height = models.FloatField('Hauteur', default=8.0)
    irc = models.IntegerField('Rendu de couleur', default=75)
    power = models.IntegerField('Puissance', default=150)
    colour = models.IntegerField('Température de couleur', default=5000)
    on_motion = models.BooleanField('Détection de mouvement?', default=False)
    lowering_night = models.IntegerField('Réduction de puissance nocturne', default=0)
    orientation = models.FloatField('Orientation', default=0.0)
    horizontal_angle = models.FloatField('Angle horizontal', default=360.0)
    nearest_way_dist = models.FloatField('Distance voie la plus proche', default=-1.0)
    day_impact = models.FloatField('Impact (jour)', default=0.0)
    night_impact = models.FloatField('Impact (nuit)', default=0.0)

    def __str__(self) -> str:
        return f'Luminaire: {self.code}'

    @property
    def way_type(self) -> str:
        # TODO: Abaisser 150W (=valeur par défaut) lorsque la puissance des luminaires sera connue
        if (self.height < 5.0 or self.on_motion or self.irc < 25) and self.power <= 150:
            return 'footway'
        return 'road'

    @property
    def angle_incidence(self) -> float:
        return 70.0

    @property
    def lumens_per_watt(self) -> int:
        return 100

    @property
    def lux_average_on_ground(self) -> float:
        value = 0
        if self.height >= 1:
            value = (self.lumens_per_watt * self.power) / (math.pi * self.height_max_range**2)
            if self.is_oriented:
                value *= 2

        return value

    def distance_with_lux(self, nb_lux: int = 5, time: str = 'day') -> float:
        # distance où le nombre de lux au sol == nb_lux
        if nb_lux == 0:
            nb_lux = 1
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

        return self.on_motion or \
                square_distance >= self.height_max_range**2 or \
                square_distance >= self.max_range(nb_lux=nb_lux, time=time) ** 2

    def impact(self, illuminated_object, nb_lux: int, time: str) -> float:
        distance = illuminated_object.distance_from(self)
        if self.is_without_impact(illuminated_object, distance, nb_lux=nb_lux, time=time):
            return 0.0

        diff_lum_tree_height = max(self.height - illuminated_object.height, 0)
        square_distance = diff_lum_tree_height ** 2 + distance ** 2

        impact_lux = (self.aligned_power_impact(illuminated_object, time=time) *
                      self.lumens_per_watt *
                      math.cos(math.radians(self.angle_incidence)) /
                      max(1, square_distance)
                      )

        return impact_lux * illuminated_object.color_impact(self.colour)

    def power_impact(self, time: str = 'day') -> float:
        power_value = self.power
        if time != 'day':
            power_value = power_value * (1 - max(0, self.lowering_night) / 100)

        return power_value

    def aligned_power_impact(self, other_object, time: str = 'day') -> int:
        power_impact = 0
        if not self.is_oriented:
            power_impact = self.power_impact(time=time) / 2
        elif self.is_aligned_with(other_object):
            power_impact = self.power_impact(time=time)

        return power_impact

    def is_aligned_with(self, other_object) -> bool:
        if not self.is_oriented or self.position == other_object.position:
            return True

        objects_alignment = Position(self.position).orientation(other_object.position)
        return not (90 < abs(objects_alignment - self.orientation) < 270)

    @property
    def is_oriented(self) -> bool:
        return self.horizontal_angle % 360 != 0

    @property
    def expense(self) -> float:
        # V1
        # TODO:
        #  * Avoir le vrai self.power pour chaque luminaire
        #  * Prendre en compte la puissance de la douille
        #  * Connaître le tarif ville
        #  * Calque Hiver/Eté/Intersaison et faire varier selon HP/HC
        #  * Retravailler la db pour mieux connaître les créneaux des plages horaires
        #  des réductions d'intensité nocturne
        lowering_night = self.lowering_night
        power_day = self.power
        power_night = power_day * (100 - lowering_night) / 100
        return (6 * power_day + 6 * power_night) * 0.1740 / 1000 * 365.25
