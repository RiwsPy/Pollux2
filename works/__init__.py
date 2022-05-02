from pathlib import Path
import os
import json
from api_ext import Api_ext
from api_ext.osm import Osm
from formats.geojson import Geojson, Geo_Feature
from formats.csv import convert_to_geojson
from formats.position import Position
from typing import List


BASE_DIR = Path(__file__).resolve().parent.parent

'''
LAT_MAX = 45.19770374838654 # 45.198848
LAT_MIN = 45.18197633865329 # 45.187501
LNG_MAX = 5.7480812072753915 # 5.725703
LNG_MIN = 5.703964233398438 # 5.704696
'''

LAT_MAX = 45.198848
LAT_MIN = 45.087501
LNG_MAX = 5.735703
LNG_MIN = 5.704696

MAX_BOUND = [45.15008475740563, 5.664997100830078, 45.221347171208436, 5.766019821166993]
#MAX_BOUND = [45.1886431, 5.7300864, 45.1889222, 5.7303789]


class Default_works(dict):
    DEFAULT_BOUND = MAX_BOUND
    #DEFAULT_BOUND = [LAT_MIN, LNG_MIN, LAT_MAX, LNG_MAX]
    query = ""
    url = ""
    data_attr = "features"
    filename = "empty"
    file_ext = "json"
    request_method = Api_ext().call
    COPYRIGHT_ORIGIN = 'unknown'
    COPYRIGHT_LICENSE = 'unknown'
    fake_request = False  # no auto-request: request in local db
    convert_to_geojson_method = convert_to_geojson

    def __init__(self, *args, bound: List[float] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.bound = bound

    def __iter__(self):
        yield from self.features

    @property
    def features(self) -> list:
        return self[self.data_attr]

    @property
    def COPYRIGHT(self) -> str:
        return f'The data included in this document is from {self.COPYRIGHT_ORIGIN}.' +\
               f' The data is made available under {self.COPYRIGHT_LICENSE}.'

    @property
    def output_filename(self) -> str:
        return self.filename + '_output'

    @property
    def bound(self) -> List[float]:
        return self._bound or self.DEFAULT_BOUND

    @bound.setter
    def bound(self, value: List[float]) -> None:
        self._bound = value

    def update(self, kwargs) -> None:
        super().update(convert_osm_to_geojson(kwargs))
        self[self.data_attr] = [self.Model(**feature) for feature in self.features]

    def request(self, **kwargs) -> dict:
        if self.fake_request:
            return self.load()

        if self.query:
            kwargs['query'] = self.query

        return self.request_method(url=self.url, **kwargs)

    def load(self, filename: str = '', file_ext: str = '') -> dict:
        filename = filename or self.filename
        file_ext = file_ext or self.file_ext
        with open(os.path.join(BASE_DIR, f'db/{filename}.{file_ext}'), 'r') as file:
            if file_ext == 'json':
                file = json.load(file)
            elif file_ext == 'csv':
                file = self.convert_to_geojson_method(file)
            else:
                raise TypeError

        return file

    def bound_filter(self, geo: Geojson, bound: List[float] = None) -> dict:
        bound = bound or self.bound
        #new_f = self.__class__(bound=bound)
        #new_f.update(self)
        geo.features = \
            [feature
             for feature in geo.features
             if self._can_be_output(feature, bound=bound)]
        """
        for obj in new_f.features:
            if obj['geometry']['type'] != 'Point':
                obj['geometry']['type'] = 'Point'
                obj['geometry']['coordinates'] = Position(obj['geometry']['coordinates'])
        """
        return geo

    def output(self, data: dict, filename: str = '') -> None:
        data = convert_osm_to_geojson(data)
        geo = Geojson(COPYRIGHT=self.COPYRIGHT)
        for feature in data['features']:
            if feature['geometry']:
                geo.append(self.Model(**feature).__dict__)
        self.bound_filter(geo, self.bound)
        geo.dump('db/' + (filename or self.output_filename) + '.json')

    def _can_be_output(self, feature: Geo_Feature, **kwargs) -> bool:
        return feature.position.in_bound(kwargs.get('bound', self.bound))

    def dump(self, filename: str = '') -> None:
        with open(os.path.join(BASE_DIR, f'db/{filename or self.filename + ".json"}'),
                  'w') as file:
            json.dump({'COPYRIGHT': self.COPYRIGHT, **self},
                      file,
                      ensure_ascii=False,
                      indent=1)

    class Model:
        def __init__(self, **kwargs):
            self.position = Position(kwargs['geometry']['coordinates']).round(8)


class Osm_works(Default_works):
    request_method = Osm().call
    skel_qt = False
    COPYRIGHT_ORIGIN = 'www.openstreetmap.org'
    COPYRIGHT_LICENSE = 'ODbL'
    data_attr = "elements"

    def _can_be_output(self, feature: Geo_Feature, bound=None) -> bool:
        return True

    def request(self, **kwargs) -> dict:
        return super().request(skel_qt=self.skel_qt, **kwargs)

    @property
    def BBOX(self) -> str:
        return f'{tuple(self.bound)}'


convert_type = {'node': 'Point'}


def convert_osm_to_geojson(data_dict: dict) -> dict:
    if 'features' in data_dict:  # geojson
        return data_dict
    if 'elements' not in data_dict:  # unknown
        raise KeyError

    ret = Geojson(COPYRIGHT=data_dict.get('COPYRIGHT', ''))
    nodes_id_to_data = {
        elt['id']: elt
        for elt in data_dict['elements']
        if elt['type'] == 'node'}
    nodes_dont_copy = set()

    for elt in data_dict['elements']:
        if elt['id'] in nodes_dont_copy:
            continue

        elt_geojson = dict()
        elt_geojson['properties'] = elt.get('tags', {})
        if elt['type'] == 'node':
            elt_geojson['lat'] = elt['lat']
            elt_geojson['lng'] = elt['lon']
        elif elt['type'] == 'way':
            elt_geojson['geometry'] = {}
            elt_geojson['geometry']['type'] = 'Polygon'
            elt_geojson['geometry']['coordinates'] = [[]]
            for search_node_id in elt['nodes']:
                node_data = nodes_id_to_data.get(search_node_id)
                if node_data:
                    elt_geojson['geometry']['coordinates'][0].append(
                        [node_data['lon'], node_data['lat']]
                    )
                    nodes_dont_copy.add(search_node_id)
                else:
                    print(node_data, ': id introuvable, type "node" ?')
        else:
            print(f"{elt['type']} non traité.")

        ret.append(elt_geojson)
    return ret
