from pathlib import Path
import os
import json
from mimetypes import guess_type

from django.contrib.gis.geos import (
    Point,
    LineString,
    Polygon,
    MultiPolygon,
    MultiLineString,
)

from pollux.api_ext import Api_ext
from pollux.api_ext.osm import Osm
from pollux.formats.geojson import Geojson
from pollux.formats.position import Position
from typing import List
from pollux.formats import osm


BASE_DIR = Path(__file__).resolve().parent.parent.parent
POLLUX_DIR = Path(__file__).resolve().parent.parent
WORKS_DIR = Path(__file__).resolve().parent

"""
LAT_MAX = 45.19770374838654 # 45.198848
LAT_MIN = 45.18197633865329 # 45.187501
LNG_MAX = 5.7480812072753915 # 5.725703
LNG_MIN = 5.703964233398438 # 5.704696
"""

LAT_MAX = 45.198848
LAT_MIN = 45.087501
LNG_MAX = 5.735703
LNG_MIN = 5.704696

MAX_BOUND = [45.1028500272485, 5.67066192626953, 45.2760944159253, 5.8938217163086]
MAX_BOUND_LNG_LAT = [
    5.67066192626953,
    45.1028500272485,
    5.8938217163086,
    45.2760944159253,
]

# for test
# MAX_BOUND = [45.1824338559252, 5.71986436843872, 45.1833602226135, 5.72116255760193]
# MAX_BOUND_LNG_LAT = [ 5.728801,45.185848, 5.730523,45.186757]


class Default_works:
    DEFAULT_BOUND = MAX_BOUND
    query = ""
    url = ""
    filename = "empty"
    file_ext = "json"
    request_method = Api_ext().call
    COPYRIGHT_ORIGIN = "unknown"
    COPYRIGHT_LICENSE = "unknown"
    fake_request = False  # no auto-request: request in local db
    model = None

    def __init__(self, bound: List[float] = None):
        self.bound = bound

    @property
    def COPYRIGHT(self) -> str:
        return (
            f"The data included in this document is from {self.COPYRIGHT_ORIGIN}."
            + f" The data is made available under {self.COPYRIGHT_LICENSE}."
        )

    @property
    def output_filename(self) -> str:
        return self.filename + "_output"

    @property
    def bound(self) -> List[float]:
        return self._bound or self.DEFAULT_BOUND

    @bound.setter
    def bound(self, value: List[float]) -> None:
        self._bound = value

    def request(self, **kwargs) -> dict:
        if self.fake_request:
            return self.load(**kwargs)

        if self.query:
            kwargs["query"] = self.query

        return self.request_method(url=self.url, **kwargs)

    def load(
        self, filename: str = "", file_ext: str = "", directory="pollux/db"
    ) -> dict:
        filename = filename or self.filename
        file_ext = file_ext or self.file_ext
        with open(
            os.path.join(BASE_DIR, directory, f"{filename}.{file_ext}"), "r"
        ) as file:
            if guess_type(directory + f"/{filename}.{file_ext}")[0] == "application/json":
                file = json.load(file)
            else:
                file = self.convert_to_geojson(file)

        return file

    def bound_filter(self, geo: Geojson, bound: List[float] = None) -> dict:
        bound = bound or self.bound
        geo.features = [
            feature for feature in geo.features if feature.position.in_bound(bound)
        ]

        return geo

    TYPE_TO_FORM = {
        "Point": Point,
        "LineString": LineString,
        "MultiLineString": MultiLineString,
        "Polygon": Polygon,
        "MultiPolygon": MultiPolygon,
    }

    def output(self, data: dict, filename: str = "") -> None:
        data = self.convert_to_geojson(data)
        if self.model:
            if data and data["features"]:
                self.model.objects.all().delete()
                for feature in data["features"]:
                    feature = self._output_feature_with_model(feature)
                    self.model.objects.create(**feature)
            else:
                print("Aucune donnée trouvée.")
        else:
            geo = Geojson(COPYRIGHT=self.COPYRIGHT)
            for feature in data["features"]:
                if self._can_be_output(feature):
                    geo.append(self.Model(**feature).__dict__)
            # self.bound_filter(geo, self.bound)
            geo.dump("db/" + (filename or self.output_filename) + ".json")

    def _output_feature_with_model(self, feature: dict) -> dict:
        geo_type = feature["geometry"]["type"]
        feature = self.Model(**feature).__dict__
        method = self.TYPE_TO_FORM.get(geo_type, Point)

        try:
            feature["position"] = method(feature["position"])
        except (TypeError, ValueError):
            if method == MultiPolygon:
                feature["position"] = MultiPolygon(Polygon(feature["position"][0][0]))
            elif method == Polygon:
                feature["position"] = Polygon(feature["position"][0])
            elif method == MultiLineString:
                feature["position"] = MultiLineString(
                    LineString(feature["position"][0])
                )
        return feature

    def _can_be_output(self, feature, **kwargs) -> bool:
        return feature["geometry"]

    @staticmethod
    def convert_to_geojson(data_dict: dict) -> dict:
        return data_dict

    class Model:
        def __init__(self, **kwargs):
            self.position = Position(kwargs["geometry"]["coordinates"]).round(8)


class Osm_works(Default_works):
    request_method = Osm().call
    skel_qt = False
    COPYRIGHT_ORIGIN = "www.openstreetmap.org"
    COPYRIGHT_LICENSE = "ODbL"

    def _can_be_output(self, *args, **kwargs) -> bool:
        return True

    def request(self, **kwargs) -> dict:
        return super().request(skel_qt=self.skel_qt, **kwargs)

    @property
    def BBOX(self) -> str:
        return f"{tuple(self.bound)}"

    @staticmethod
    def convert_to_geojson(data_dict: dict) -> dict:
        return osm.convert_to_geojson(data_dict)
