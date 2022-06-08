from .default import Default_model
from django.contrib.gis.db import models
from django.contrib.gis.geos import MultiLineString, GEOSGeometry


class Parking_public(Default_model):
    class Meta:
        app_label = "pollux"
        verbose_name = "Parking public"
        verbose_name_plural = "Parkings public"

    position = models.MultiLineStringField(default=MultiLineString())
    code = models.IntegerField(default=0)
    parking_type = models.CharField('Type de stationnement', max_length=15, default='unknown')
    fee = models.CharField('Payant', max_length=15, default='unknown')
    way = models.CharField('Voie', max_length=100, default='unknown')

    parking_type_to_width = {
        'parallel': 2.3,
        'diagonal': (2.3 + 5.0) / 2,
        'perpendicular': 5.0,
        'mixte': (2.3 * 3 / 2 + 5.0 / 2) / 2
    }

    @property
    def width(self) -> float:
        return self.parking_type_to_width.get(self.parking_type,
                                              self.parking_type_to_width['parallel']
                                              )
