from django.contrib.gis.db import models
import json
from django.core import serializers
from django.contrib.gis.geos import Point, MultiLineString, LineString
from pollux.formats.position import Position
from django.contrib.gis.gdal.error import GDALException


class Default_model(models.Model):
    class Meta:
        abstract = True
        app_label = "pollux"

    position = models.PointField(default=Point(0, 0))

    @classmethod
    def reset_queryset(cls, queryset, *attrs):
        queryset.update(**{attr: getattr(cls, attr).field.default for attr in attrs})

    @staticmethod
    def serialize(queryset, file_format: str = "geojson") -> dict:
        ret = json.loads(serializers.serialize(file_format, queryset))
        del ret["crs"]
        return ret

    @property
    def length(self) -> float:
        if isinstance(self.position, (LineString, MultiLineString)):
            self.position.srid = 4326
            try:
                self.position.transform(3857)
            except GDALException:
                pass
        return self.position.length

    def illuminated_height_at(self, distance: float) -> float:
        return 0.0

    def illuminated_ratio(self, illuminated_height: float) -> float:
        if illuminated_height <= 0:
            return 0.0
        try:
            return min(1.0, illuminated_height / self.height)
        except ZeroDivisionError:
            return 1.0

    def color_impact(self, color: int) -> float:
        """
        :param color: Colour Tempepature (Kelvins)
        :return: float
        """
        return 1.0

    def irc_impact(self, irc: int) -> int:
        """
        :param irc: Lamps irc (%)
        :return: float
        """
        return irc

    @property
    def height(self) -> float:
        return 0.0

    def distance_from(self, obj) -> float:
        return Position(self.position).distance(obj.position)
