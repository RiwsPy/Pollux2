from .default import Default_model
from django.contrib.gis.db import models
from django.contrib.gis.geos import LineString


class Highways(Default_model):
    class Meta:
        app_label = "pollux"

    type = models.CharField(max_length=20, default="")
    position = models.LineStringField(default=LineString([[0, 0], [0, 0]]))
    name = models.CharField(max_length=100, default="")
    width = models.FloatField(default=0.0)
    lanes = models.IntegerField(default=0)

    @property
    def is_footway(self) -> bool:
        return self.name == '' or self.type in ('footway', 'pedestrian', 'path')
