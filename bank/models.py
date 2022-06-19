from django.db import models
from pollux.models.lamps import DefaultLamps


class LampsUpload(DefaultLamps):
    class Meta:
        app_label = "bank"
        verbose_name = "Luminaire importé"
        verbose_name_plural = "Luminaires importés"
        abstract = True

    lng = models.FloatField('Longitude', default=0.0)
    lat = models.FloatField('Latitude', default=0.0)


class LampsMairin00(LampsUpload):
    class Meta:
        app_label = "bank"
        verbose_name = "Luminaire importé_Pascal00"
        verbose_name_plural = "Luminaires importés_Pascal00"


class LampsCoccia00(LampsUpload):
    class Meta:
        app_label = "bank"
        verbose_name = "Luminaire importé_Romain00"
        verbose_name_plural = "Luminaires importés_Romain00"
