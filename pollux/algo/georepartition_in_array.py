from math import ceil, floor
from typing import List, Tuple, Any
from pollux.formats.position import LNG_1M, LAT_1M
import numpy as np
from django.contrib.gis.geos import Point, Polygon, LineString, MultiLineString
from pollux.formats.position import Position
from django.db.models.query import QuerySet


class Repartition_point:
    def __init__(self, queryset: QuerySet, bound: List[float] = None, max_range: int = 1):
        if max_range <= 0:
            print('max_range must be positive')
            raise ValueError
        elif not queryset or not bound:
            raise ValueError

        self.nb_errors = 0
        self.bound = bound
        self.max_range = max_range
        dim_bound = self.dim_bound()
        self.array = np.empty(dim_bound, dtype=np.dtype('O'))

        if isinstance(queryset, QuerySet):
            # queryset = queryset.filter(position__within=Polygon.from_bbox(self.bound))
            elt_count = queryset.count()
        else:
            elt_count = len(queryset)
        print(elt_count, 'éléments présents.')
        for feature in queryset:
            self.place_feature_in_array(feature)

    def place_feature_in_array(self, feature) -> None:
        if isinstance(feature.position, (Point, Position)):
            positions = [feature.position]
        elif isinstance(feature.position, LineString):
            positions = self.cut_linestring(feature.position)
        elif isinstance(feature.position, MultiLineString):
            positions = []
            for position in feature.position:
                positions.extend(self.cut_linestring(position))
        else:
            print(type(feature.position), 'non géré')
            return
        self.place_position_in_array(feature, *positions)

    def place_position_in_array(self, owner, *positions):
        for position in positions:
            array_case = self.feature_position_case(position)
            try:
                self.array[array_case].add(owner)
            except AttributeError:
                # array[case] = None
                self.array[array_case] = {owner}
            except IndexError:
                # out of bound
                self.nb_errors += 1
                # print('IndexError', array_case)
                pass

    def dim_bound(self) -> Tuple[int, int]:
        lng_min, lat_min, lng_max, lat_max = self.bound
        height = (lat_max - lat_min) / LAT_1M / self.max_range
        width = (lng_max - lng_min) / LNG_1M / self.max_range
        return ceil(height), ceil(width)

    def feature_position_case(self, position: tuple) -> Tuple[int, int]:
        lng_min, lat_min, lng_max, lat_max = self.bound
        height = (position[1] - lat_min) / LAT_1M / self.max_range
        width = (position[0] - lng_min) / LNG_1M / self.max_range
        return floor(height), floor(width)

    def cut_linestring(self, position: LineString) -> LineString:
        """
        Découpe la LineString en segment d'une longueur inférieure ou égale à self.max_range
        :param position: LineString
        :return: LineString
        """
        if not isinstance(position, LineString):
            print('TypeError, linestring expected, got', type(position))
            return LineString()
        ret = []
        for pos_a, pos_b in zip(position[:-1], position[1:]):
            distance_between = Position(pos_a).distance(pos_b)
            nb_decoupe = ceil(distance_between / self.max_range)

            lng_gain_decoupe = (pos_b[0] - pos_a[0]) / nb_decoupe
            lat_gain_decoupe = (pos_b[1] - pos_a[1]) / nb_decoupe
            new_point_lng, new_point_lat = pos_a
            for _ in range(nb_decoupe+1):
                ret.append(Point(new_point_lng, new_point_lat))
                new_point_lng += lng_gain_decoupe
                new_point_lat += lat_gain_decoupe

        return LineString(ret)


def adjacent_match(array1, array2, max_case_range: int = 1) -> Tuple[Any, Any]:
    if max_case_range <= 0:
        print('max_range must be > 0')
        raise AttributeError
    if array1.shape != array2.shape:
        print(f'Warning : Array shape are different: {array1.shape} != {array2.shape}')

    for (x, y), features in np.ndenumerate(array1):
        if not features:
            continue

        for feature1 in features:
            features2 = set()
            for i in range(x - max_case_range, x + max_case_range + 1):
                for j in range(y - max_case_range, y + max_case_range + 1):
                    try:
                        features2 = features2.union(array2[(i, j)])
                    except (IndexError, TypeError):
                        # IndexError: out of bound
                        # TypeError: array[x, y] = None
                        continue

            for feature2 in features2:
                yield feature1, feature2
