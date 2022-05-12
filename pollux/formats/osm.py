from osm2geojson import json2geojson
from pollux.formats.geojson import Geojson


def convert_to_geojson(data_dict: dict) -> dict:
    if 'features' in data_dict:  # geojson
        return data_dict
    if 'elements' not in data_dict:  # unknown
        raise KeyError

    ret = Geojson(COPYRIGHT=data_dict.get('COPYRIGHT', ''))
    data_dict = json2geojson(data_dict)
    for feature in data_dict['features']:
        feature['properties'] = feature['properties']['tags']
        ret.append(feature)

    return ret
