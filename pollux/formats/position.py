from itertools import zip_longest
from typing import List
from math import radians, cos, sin, degrees, acos, asin
from django.contrib.gis.geos import Point

EARTH_RADIUS = 6371000  # meters


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

    def distance3(self, other: List[float]) -> float:
        # method 2
        my_pos = self.force_position()
        lat_a = radians(my_pos.lat)
        lat_b = radians(other[1])
        long_diff = radians(my_pos.lng - other[0])
        distance = (sin(lat_a) * sin(lat_b) +
                    cos(lat_a) * cos(lat_b) * cos(long_diff))
        resToMile = degrees(acos(distance)) * 69.09
        resToMt = resToMile / 0.00062137119223733
        return resToMt

    def distance(self, other: List[float]) -> float:
        my_pos = self.force_position()

        dlat_rad = radians(other[1]-my_pos[1])
        dlng_rad = radians(other[0]-my_pos[0])
        lat1_rad = radians(my_pos[1])
        lat2_rad = radians(other[1])

        a = sin(dlat_rad/2)**2 + \
            cos(lat1_rad) * cos(lat2_rad) * sin(dlng_rad/2)**2

        return EARTH_RADIUS * 2 * asin(a**0.5)

    def distance_cartesian(self, other) -> float:
        my_pos = self.force_position()
        diff_lng = (other[0] - my_pos[0]) / LNG_1M
        diff_lat = (other[1] - my_pos[1]) / LAT_1M
        return (diff_lat**2 + diff_lng**2)**0.5

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
        my_pos = self.force_position()

        self_is_in = \
            max(other1[0], other2[0]) > my_pos[0] > min(other1[0], other2[0]) or\
            max(other1[1], other2[1]) > my_pos[1] > min(other1[1], other2[1])
        if not self_is_in:
            return min(my_pos.distance(other1), my_pos.distance(other2))

        _nearest_point = self.nearest_point_from_way(other1, other2)

        return my_pos.distance(_nearest_point)

    def distance_cartesian_from_way(self, other1: List[float], other2: List[float]) -> float:
        my_pos = self.force_position()

        self_is_in = \
            max(other1[0], other2[0]) > my_pos[0] > min(other1[0], other2[0]) or\
            max(other1[1], other2[1]) > my_pos[1] > min(other1[1], other2[1])
        if not self_is_in:
            return min(my_pos.distance_cartesian(other1), my_pos.distance_cartesian(other2))

        _nearest_point = self.nearest_point_from_way(other1, other2)

        return my_pos.distance_cartesian(_nearest_point)

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
        if type(self[0]) is list:
            if type(self[0][0]) is list:
                if type(self[0][0][0]) is list:
                    return 'MultiPolygon'

                try:
                    self[0][1]
                except IndexError:
                    return 'Polygon'
                return 'MultiLineString'
            return 'LineString'
        return 'Point'

    def projection(self, distance: float, orientation: float) -> 'Position':
        """
        :param distance: float (meters)
        :param orientation: float (degrees)
        :return: Position
        """
        orientation %= 360
        orientation_x = 1 - abs(orientation % 180 - 90) / 90
        orientation_y = 1 - orientation_x
        if 270 > orientation > 90:
            orientation_y = -orientation_y
        if orientation > 180:
            orientation_x = -orientation_x

        new_x = self.lng + orientation_x * distance * LNG_1M
        new_y = self.lat + orientation_y * distance * LAT_1M
        return self.__class__([new_x, new_y])

    def orientation(self, other: List[float]) -> float:
        # orientation en degrés
        if self == other:
            raise ZeroDivisionError

        x1 = (other[0] - self.lng) * LNG_TO_LAT
        y1 = (other[1] - self.lat)  # * LAT_TO_LNG
        x = x1 * 90 / (abs(y1) + abs(x1))

        if y1 < 0:
            if x > 270:
                diff = 270
            else:
                diff = 90
            x -= (x - diff) * 2
        return x % 360

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
