from .default import Default_model
from django.contrib.gis.db import models
from django.contrib.gis.geos import MultiLineString

pedestrian_lane_width = 0.9
parking_width_default = 2.3
parking_height_default = 5.0
car_lane_width = 3.2
cycle_lane_width = 0.6
line_width = 0.2

convert_parking_type_to_width = {
    'parallel': parking_width_default,
    'diagonal': (parking_width_default + parking_height_default)/2,
    'perpendicular': parking_height_default,
}


class Highways(Default_model):
    class Meta:
        app_label = "pollux"
        verbose_name = "Voie de circulation"
        verbose_name_plural = "Voies de circulation"

    highway = models.CharField('Type', max_length=20, default="")
    position = models.MultiLineStringField(default=MultiLineString())
    name = models.CharField('Nom de la voie', max_length=100, default="")
    width = models.FloatField('Largeur', default=0.0)
    lanes = models.IntegerField('Nombre de voies', default=0)
    maxspeed = models.IntegerField('Vitesse maximale', default=0)
    oneway = models.CharField('Sens unique', max_length=3, default='no')
    parking_r = models.CharField('Parking à droite', max_length=15, default='unknown')
    parking_l = models.CharField('Parking à gauche', max_length=15, default='unknown')

    def __str__(self) -> str:
        return f'Voie: {self.highway}, {self.name}'

    @property
    def is_footway(self) -> bool:
        return self.name == '' or self.highway in ('footway', 'pedestrian', 'path')

    def car_lanes(self) -> int:
        if self.is_footway:
            return 0
        nb_lanes = self.lanes
        if nb_lanes <= 0:
            nb_lanes = 2
            if self.oneway != 'no' and self.maxspeed <= 50 and \
                    self.highway not in ('primary', 'secondary', 'tertiary') or \
                    self.highway in ('service', 'living_street', 'residential') and \
                    self.maxspeed < 30:
                nb_lanes = 1

        return nb_lanes

    def parking_lanes(self) -> int:
        if self.is_footway or self.maxspeed > 50:
            return 0
        nb_lanes = 0
        if self.parking_r not in ('unknown', 'no'):
            nb_lanes += 1
        if self.parking_l not in ('unknown', 'no'):
            nb_lanes += 1

        return nb_lanes

    @property
    def width_car(self) -> float:
        nb_car_lane = self.car_lanes()
        if nb_car_lane <= 0:
            return 0.0

        value = nb_car_lane * car_lane_width
        if self.highway not in ("service", "unclassified"):
            # ajout des largeurs des bandes
            value += (nb_car_lane + 1) * line_width
        elif self.width > 0.0:
            # voies à largeur très variable, plus de sens de se référer à l'attribut width
            value = self.width
        return value

    @property
    def width_parking(self) -> float:
        # pas de ligne ajouté car prise en compte côté route
        width = 0.0
        if self.parking_lanes():
            for side in ('parking_r', 'parking_l'):
                parking_type = getattr(self, side, 'no')
                if parking_type not in ('unknown', 'no'):
                    width += convert_parking_type_to_width.get(parking_type, parking_width_default)
        return width
