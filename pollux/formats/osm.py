from osm2geojson import json2geojson
from pollux.formats.geojson import Geojson


def convert_osm_to_geojson(data: dict) -> dict:
    if "features" in data:  # geojson
        return data
    if "elements" not in data:  # unknown
        raise KeyError

    ret = Geojson(COPYRIGHT=data.get("COPYRIGHT", ""))
    data_dict = json2geojson(data)
    for feature in data_dict["features"]:
        feature["properties"] = feature["properties"]["tags"]
        ret.append(feature)

    return ret
