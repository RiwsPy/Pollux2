from itertools import zip_longest
import math
from typing import List

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

    def distance(self, other: List[float]) -> float:
        # return ((abs(self.lat - other[1]) * 111.2) ** 2 + (abs(self.lng - other[0]) * 78.6) ** 2) ** 0.5 * 1000
        my_pos = self.force_position()
        dlat_rad = math.radians(other[1]-my_pos[1])
        dlon_rad = math.radians(other[0]-my_pos[0])
        lat1_rad = math.radians(my_pos[1])
        lat2_rad = math.radians(other[1])

        a = math.sin(dlat_rad/2)**2 + \
            math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon_rad/2)**2

        return EARTH_RADIUS * 2 * math.asin(a**0.5)

    def distance2(self, other: List[float]) -> float:
        e = 0.081819191
        adjustedX = other[0] * math.cos(self.lat) / (1 - e**2 * math.sin(self.lat)**2)**0.5
        adjustedY = other[1] * math.cos(self.lat) * (1 - e**2) / pow(1 - e**2 * math.sin(self.lat)**2, 3 / 2)
        return (adjustedX**2 + adjustedY**2)**0.5

    def nearest_point_from_way(self, other1: List[float], other2: List[float]) -> 'Position':
        my_pos = self.force_position()
        try:
            a1 = (other2[1] - other1[1]) / (other2[0] - other1[0])
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
                    test = self[0][1]
                except IndexError:
                    return 'Polygon'
                else:
                    return 'MultiLineString'
        return 'Point'

    def projection(self, distance: float, orientation: int, pr=False) -> 'Position':
        orientation %= 360
        orientation_x = 90 - abs(orientation % 180 - 90)
        orientation_y = 90 - orientation_x
        if 270 > orientation > 90:
            orientation_y = -orientation_y
        if orientation > 180:
            orientation_x = -orientation_x

        new_x = self.lng + orientation_x/90 * distance * LNG_1M
        new_y = self.lat + orientation_y/90 * distance * LAT_1M
        return self.__class__([new_x, new_y])

    def orientation(self, other: List[float]) -> float:
        y1 = (other[1] - self.lat) * LAT_1M
        x1 = (other[0] - self.lng) * LNG_1M
        try:
            x = abs(x1) / (abs(y1) + abs(x1)) * 90
            y = abs(y1) / (abs(y1) + abs(x1)) * 90
        except ZeroDivisionError:
            x = 0.5
            y = 0.5

        x = x * 90 / (abs(x) + abs(y))
        if x1 < 0:
            x = 360 - x
        if y1 < 0:
            if x > 270:
                x -= (x - 270) * 2
            else:
                x -= (x - 90) * 2
        return x

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
            for position in self:
                cumul_lng += position[0]
                cumul_lat += position[1]
                nb += 1
        return Position([cumul_lng/nb, cumul_lat/nb])

    def round(self, number=None) -> 'Relation':
        if type(self[0]) is float:
            return self.__class__([round(ax, number) for ax in self])
        return self


LNG_1M = 1 / Position([0, 0]).distance([1, 0])
LAT_1M = 1 / Position([0, 0]).distance([0, 1])
MOY_1M = (LNG_1M+LAT_1M)/2
a = Position([45.18376101332543, 5.739578604698182])
b = Position([45.18425254525199, 5.740799009799958])
