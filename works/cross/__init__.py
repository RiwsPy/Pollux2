from formats.geojson import Geojson, Geo_Feature
from works import BASE_DIR, Default_works
import os
import json
from typing import List
from formats.position import LNG_1M, LAT_1M, Relation
from math import ceil, floor
import numpy as np
from collections import defaultdict
from formats.position import Position


class Works_cross:
    value_attr = '_pollux_values'
    max_range = 25
    multiplier = 1
    filename = __file__

    def __init__(self):
        self.bound = Default_works.DEFAULT_BOUND
        self.teams = []
        self.teams_array = []
        self.copyrights = set()
        self.new_features = Geojson()

    # Works_cross(input=[[teammate1, teammate2], [teammate1], [teammate1], ...])
    def load(self, *teams, bound: List[float] = None, max_range: int = 0, multiplier: int = 0,
             segment=False):
        self.bound = bound or self.bound
        self.max_range = max_range or self.max_range
        self.multiplier = multiplier or self.multiplier
        dim = self.bound_to_array(self.bound, self.max_range)
        for team in teams:
            if not team:
                continue

            np_array = np.empty(dim, dtype=np.dtype('O'))
            team_data = Geojson(name='')
            team_names = []
            team_cpr = set()
            for works_cls in team:
                team_works = works_cls.Works(bound=self.bound)
                try:
                    data = team_works.load(team_works.output_filename, 'json')
                except FileNotFoundError:
                    data = team_works.load(team_works.filename, 'json')
                geo = Geojson(COPYRIGHT=team_works.COPYRIGHT)
                geo.extend(data['features'])
                new_features = team_works.bound_filter(geo).features
                if new_features:
                    if segment:
                        np_array = self.repartition_segment_in_array(new_features, np_array)
                    else:
                        np_array = self.repartition_in_array(new_features, np_array)
                    team_data.extend(new_features)
                    team_names.append(team_works.filename)
                    team_cpr.add(team_works.COPYRIGHT)
                    self.copyrights.add(team_works.COPYRIGHT)
            self.teams_array.append(np_array)
            team_data.name = '-'.join(team_names)
            team_data.COPYRIGHT = ' -- '.join(team_cpr)
            self.teams.append(team_data)

    def _iter_double_and_range(self):
        for team in self.teams:
            for teammate in team.features:
                teammate.position = teammate.position.force_position()
                teammate['geometry']['type'] = teammate.position.type_of_pos()
                value_attr_copy = teammate['properties'].get(f'{self.value_attr}', {}).copy()
                teammate['properties'][self.value_attr] = defaultdict(int)
                for k, v in value_attr_copy.items():
                    teammate['properties'][self.value_attr][k] = v

        for blue_teammate in self.teams[0].features:
            blue_position = blue_teammate.position
            blue_case = self.feature_position_case(blue_teammate)

            for i in range(blue_case[0]-1, blue_case[0]+2):
                for j in range(blue_case[1]-1, blue_case[1]+2):
                    try:
                        red_features = self.teams_array[1][(i, j)] or ()
                    except IndexError:
                        continue
                    else:
                        for red_teammate in red_features:
                            if isinstance(red_teammate, Segment):
                                geo_distance_between = blue_position.distance_from_way(*red_teammate.positions)
                            else:
                                geo_distance_between = blue_position.distance(red_teammate.position)
                            if geo_distance_between <= self.max_range:
                                yield blue_teammate, red_teammate, geo_distance_between

    def __str__(self) -> str:
        return self.filename.rpartition('/')[-1]

    def __repr__(self) -> str:
        return f"{self.__str__().rpartition('.')[0]}.Cross(max_range= {self.max_range}, multiplier= {self.multiplier})"

    @property
    def db_name(self) -> str:
        return f"{self.filename.rpartition('/')[-1].replace('.py', '')}--" +\
               f"{'--'.join(team.name.replace('cross/', '') for team in self.teams)}--{self.max_range}"

    @property
    def COPYRIGHT(self) -> str:
        return ' || '.join(self.copyrights)

    @property
    def features(self) -> list:
        ret = []
        for team in self.teams:
            ret.extend(team.features)
        return ret

    def dump(self, filename: str = "", features: list = None) -> None:
        print(f'Ecriture de db/cross/{filename or self.db_name + ".json"}')
        with open(os.path.join(BASE_DIR, f'db/cross/{filename or self.db_name + ".json"}'),
                  'w') as file:
            geo_features = []
            for feature in (features or self.features):
                if feature['properties'].get(self.value_attr):
                    feature['properties'][self.value_attr] = {
                        key: round(value, 2)
                        for key, value in feature['properties'][self.value_attr].items()
                    }
                geo_features.append(feature)

            json.dump(Geojson(COPYRIGHT=self.COPYRIGHT, features=geo_features),
                      file,
                      ensure_ascii=False,
                      indent=1)

    def apply_algo(self) -> None:
        pass

    def feature_position_case(self, feature, bound=None, max_range=None):
        lat_min, lng_min, lat_max, lng_max = bound or self.bound
        if isinstance(feature, Position):
            position = feature
        else:
            try:
                test = feature.position.lat
                position = feature.position
            except IndexError:
                position = Relation(feature.position).to_position()

        height = floor((position.lat - lat_min) / LAT_1M / (max_range or self.max_range))
        width = floor((position.lng - lng_min) / LNG_1M / (max_range or self.max_range))
        return height, width

    def repartition_in_array(self, features, array, bound=None, max_range=None):
        for feature in features:
            case = self.feature_position_case(feature, bound=bound, max_range=max_range)
            array = append_elt_in_array(array, case, feature)
        return array

    def repartition_segment_in_array(self, features, array):
        max_range = self.max_range
        for feature in features:
            if feature['geometry']['type'] == 'MultiLineString':
                for line in feature['geometry']['coordinates']:
                    for position1, position2 in zip(line[:-1], line[1:]):
                        position1 = Position(position1)
                        position2 = Position(position2)
                        distance_between = position1.distance(position2)
                        nb_decoupe = ceil(distance_between/max_range)
                        gain_lng_decoupe = (position2.lng - position1.lng)/nb_decoupe
                        gain_lat_decoupe = (position2.lat - position1.lat)/nb_decoupe
                        for i in range(nb_decoupe):
                            seg = Segment(position1+[gain_lng_decoupe*i, gain_lat_decoupe*i],
                                          position1+[gain_lng_decoupe*(i+1), gain_lat_decoupe*(i+1)])

                            seg.properties = feature['properties']
                            case_pos1 = self.feature_position_case(seg[0])
                            case_pos2 = self.feature_position_case(seg[1])
                            array = append_elt_in_array(array, case_pos1, seg)
                            if case_pos2 != case_pos1:
                                array = append_elt_in_array(array, case_pos2, seg)
        return array

    @staticmethod
    def bound_to_array(bound: List[float], side: int) -> tuple:
        lat_min, lng_min, lat_max, lng_max = bound
        height = (lat_max - lat_min) / LAT_1M / side
        width = (lng_max - lng_min) / LNG_1M / side
        return ceil(height), ceil(width)


def append_elt_in_array(array, position, elt):
    try:
        if array[position]:
            array[position].append(elt)
        else:
            array[position] = [elt]
    except IndexError:
        pass
        #print('out of bound:', position)
    return array


class Segment:
    def __init__(self, posA, posB):
        self.positions = [Position(posA), Position(posB)]

    def __getitem__(self, value):
        return self.positions[value]
