from .default import Default_model
from django.contrib.gis.db import models
from pollux.formats.position import Position
from pollux.models.lamps import Lamps


class Trees(Default_model):
    class Meta:
        app_label = "pollux"
        verbose_name = "Arbre"

    code = models.CharField(max_length=20, default="")
    taxon = models.CharField(max_length=100, default="")
    planted_date = models.IntegerField('Date de plantation', default=0)
    height = models.FloatField('Hauteur', default=0)
    day_impact = models.FloatField('Impact (jour)', default=0.0)
    night_impact = models.FloatField('Impact (nuit)', default=0.0)

    def __str__(self) -> str:
        return f'Arbre: {self.code} {self.taxon}'

    def distance_from(self, obj) -> float:
        dist = Position(self.position).distance(obj.position)
        if isinstance(obj, Lamps):
            illuminated_height = obj.illuminated_height_at(dist)
            illuminated_ratio = self.illuminated_ratio(illuminated_height)
            if illuminated_ratio >= 0.3:  # 30%, feuilles
                dist -= 1
        return max(0.0, dist)

    def color_impact(self, color: int) -> float:
        # impact compris entre 60 (2000K) (ratio 0.75) et 80 (6000K) (ratio 1)
        return (60 + 20 * max(0, min(4000, color - 2000)) / 4000) / 80
