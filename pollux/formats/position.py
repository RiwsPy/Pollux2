from itertools import zip_longest
from typing import List
from math import radians, cos, sin, degrees, acos, asin
from django.contrib.gis.geos import Point
from pyproj import Geod

EARTH_RADIUS = 6371000  # meters
geoid = Geod(ellps='WGS84')


class Position(List[float]):
    default_pos = 0.0

    def __init__(self, value: list = None):
        list.__setitem__(self, slice(None), value or [self.default_pos, self.default_pos])

    @property
    def lat(self) -> float:
        return self[1]

    @property
    def lng(self) -> float:
        return self[0]

    def __add__(self, other) -> 'Position':
        return self.__class__([
            pos1+pos2
            for pos1, pos2 in zip_longest(self, other, fillvalue=self.default_pos)])
    __iadd__ = __add__

    def __truediv__(self, other: float) -> 'Position':
        return self.__class__([
            pos/other for pos in self]
        )

    def force_position(self) -> 'Position':
        if type(self[0]) is list:
            return Relation(self).to_position()
        return self

    def distance(self, other: List[float]) -> float:
        return geoid.inv(*self, *other)[2]

    def distance_x(self, other: List[float]) -> float:
        my_pos = self.force_position()

        dlat_rad = radians(other[1]-my_pos[1])
        dlng_rad = radians(other[0]-my_pos[0])
        lat1_rad = radians(my_pos[1])
        lat2_rad = radians(other[1])

        a = sin(dlat_rad/2)**2 + \
            cos(lat1_rad) * cos(lat2_rad) * sin(dlng_rad/2)**2

        return EARTH_RADIUS * 2 * asin(a**0.5)

    def nearest_point_from_way(self, other1: List[float], other2: List[float]) -> 'Position':
        my_pos = self.force_position()

        try:
            a1 = (other2[1] - other1[1]) / (other2[0] - other1[0])
            # a1 = ((other2[1] - other1[1]) * LAT_1M) / ((other2[0] - other1[0]) * LNG_1M)
        except ZeroDivisionError:
            x = 0
            y = other1[1]
        else:
            try:
                a2 = -1/a1
            except ZeroDivisionError:
                a2 = 0
            b1 = other1[1] - a1*other1[0]
            b2 = my_pos[1] - a2*my_pos[0]
            try:
                x = (b2 - b1) / (a1 - a2)
            except ZeroDivisionError:
                x = 0
            y = a1 * x + b1

        return self.__class__([x, y])

    def distance_from_way(self, other1: List[float], other2: List[float]) -> float:
        # TODO: vrai dans un repère cartésien, à améliorer
        my_pos = self.force_position()

        xM, yM = my_pos
        xB, yB = other1
        xE, yE = other2
        # coordonnées a,b du vecteur EB
        a = xE - xB
        b = yE - yB
        # équation de la perpendiculaire D1 en B à (EB): ax+by+w1
        w1 = -a * xB - b * yB
        # puissance de M par rapport à D1
        PMD1 = a * xM + b * yM + w1
        # puissance de E par rapport à D1
        PED1 = a * xE + b * yE + w1
        # A ce stade encore ni racine ni quotient
        if PMD1 * PED1 < 0:  # M et E de part et d'autre de D1
            return ((xM - xB) * (xM - xB) + (yM - yB) * (yM - yB)) ** 0.5 / MOY_1M

        # équation de la perpendiculaire D2 en E à (EB): ax+by+w2
        w2 = -a * xE - b * yE
        # puissance de M par rapport à D2
        PMD2 = a * xM + b * yM + w2
        # puissance de B par rapport à D2
        PBD2 = a * xB + b * yB + w2
        if PMD2 * PBD2 < 0:  # M et B de part et d'autre de D2
            return ((xM - xE) * (xM - xE) + (yM - yE) * (yM - yE)) ** 0.5 / MOY_1M

        # équation de la droite (EB) : bx-ay+w3
        w3 = a * yB - b * xB
        return abs(b * xM - a * yM + w3) / (a * a + b * b)**0.5 / MOY_1M

    def distance_from_way_old(self, other1: List[float], other2: List[float]) -> float:
        my_pos = self.force_position()

        self_is_in = \
            max(other1[0], other2[0]) > my_pos[0] > min(other1[0], other2[0]) and\
            max(other1[1], other2[1]) > my_pos[1] > min(other1[1], other2[1])
        if not self_is_in:
            return min(my_pos.distance(other1), my_pos.distance(other2))
        # cas où il est "à moitié" dedans

        _nearest_point = self.nearest_point_from_way(other1, other2)

        return my_pos.distance(_nearest_point)

    def in_bound(self, bound: List[float]) -> bool:
        if type(self[0]) is float:
            lat_min, lng_min, lat_max, lng_max = bound
            return lat_min <= self.lat <= lat_max and lng_min <= self.lng <= lng_max
        return Relation(self).in_bound(bound)

    def round(self, number=None) -> 'Position':
        if type(self[0]) is float:
            return self.__class__([round(ax, number) for ax in self])
        return self

    def type_of_pos(self) -> str:
        if isinstance(self[0], list):
            if isinstance(self[0][0], list):
                if isinstance(self[0][0][0], list):
                    return 'MultiPolygon'

                if self[0][0] == self[0][-1]:
                    return 'Polygon'
                return 'MultiLineString'
            return 'LineString'
        return 'Point'

    def projection(self, distance: float, orientation: float) -> 'Position':
        lng_new, lat_new, _ = geoid.fwd(*self, orientation, distance)
        return self.__class__([lng_new, lat_new])

    def orientation(self, other: List[float]) -> float:
        for_az, _, _ = geoid.inv(*self, *other)
        return for_az % 360

    def iter_pos(self) -> tuple:
        type_of_pos = self.type_of_pos()
        if type_of_pos == 'Point':
            yield tuple(self)
        elif type_of_pos == 'LineString':
            for pos1, pos2 in zip(self[:-1], self[1:]):
                yield pos1, pos2
        # TODO: multipolygon ??
        else:
            for line in self:
                for pos1, pos2 in zip(line[:-1], line[1:]):
                    yield pos1, pos2


# [[Position], [Position], ...]
# TODO


class Relation(list):
    default_pos = 0.0

    def __init__(self, value: list = None):
        list.__setitem__(self, slice(None), value or [[self.default_pos, self.default_pos]])

    @property
    def is_multiline(self) -> bool:
        return type(self[0][0]) is list

    def in_bound(self, bound: List[float]) -> bool:
        # TODO: surface
        if self.is_multiline:
            for lines in self:
                for position in lines:
                    if Position(position).in_bound(bound):
                        return True
        else:
            for position in self:
                if Position(position).in_bound(bound):
                    return True

        return False

    def to_position(self) -> Position:
        nb = 0
        cumul_lat = 0
        cumul_lng = 0
        if self.is_multiline:
            for positions in self:
                for position in positions:
                    cumul_lng += position[0]
                    cumul_lat += position[1]
                    nb += 1
        else:
            for nb, position in enumerate(self):
                cumul_lng += position[0]
                cumul_lat += position[1]
            nb += 1
        try:
            return Position([cumul_lng/nb, cumul_lat/nb])
        except ZeroDivisionError:
            return Position()

    def round(self, number=None) -> 'Relation':
        if type(self[0]) is float:
            return self.__class__([round(ax, number) for ax in self])
        return self


# LAT_TO_LNG = 1200 / 1564
LAT_TO_LNG = 787983 / 1112285
LNG_TO_LAT = 1112285 / 787983

LNG_1M = 1 / Position([0, 0]).distance([1, 0]) * LNG_TO_LAT
LAT_1M = 1 / Position([0, 0]).distance([0, 1])  # * LAT_TO_LNG
MOY_1M = (LNG_1M+LAT_1M)/2
