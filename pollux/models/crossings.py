from .default import Default_model
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


class Crossings(Default_model):
    class Meta:
        app_label = "pollux"
        verbose_name = "Passage piéton"
        verbose_name_plural = "Passages piéton"

    position = models.PointField(default=Point([0, 0]))
    illuminance_day = models.FloatField('Lux_day', default=0.0)
    illuminance_irc_day = models.FloatField('Lux_day_irc', default=0.0)
    illuminance_night = models.FloatField('Lux_night', default=0.0)
    illuminance_irc_night = models.FloatField('Lux_night_irc', default=0.0)

    def __str__(self) -> str:
        return f'Passage piéton'
