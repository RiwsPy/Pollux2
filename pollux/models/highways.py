from .default import Default_model
from django.contrib.gis.db import models
from django.contrib.gis.geos import LineString


class Highways(Default_model):
    class Meta:
        app_label = "pollux"
        verbose_name = "Voie de circulation"
        verbose_name_plural = "Voies de circulation"

    type = models.CharField('Type', max_length=20, default="")
    position = models.LineStringField(default=LineString([[0, 0], [0, 0]]))
    name = models.CharField('Nom de la voie', max_length=100, default="")
    width = models.FloatField('Largeur', default=0.0)
    lanes = models.IntegerField('Nombre de voies', default=0)
    parking_r = models.CharField('Parking à droite', max_length=15, default='unknown')
    parking_l = models.CharField('Parking à gauche', max_length=15, default='unknown')

    def __str__(self) -> str:
        return f'Voie: {self.type}, {self.name}'

    @property
    def is_footway(self) -> bool:
        return self.name == '' or self.type in ('footway', 'pedestrian', 'path')
