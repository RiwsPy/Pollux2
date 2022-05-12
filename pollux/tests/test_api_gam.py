from pollux.api_ext.grenoble_alpes_metropole import Gam
import requests
import pytest
from pollux.api_ext import BadStatusError
import os
import json
from .conftest import BASE_DIR, DB_DIR


class Mock_request:
    def __init__(self, status_code: int):
        self.status_code = status_code

    @staticmethod
    def json():
        with open(os.path.join(BASE_DIR, DB_DIR, 'mock_geojson.json'), 'r') as file:
            return json.load(file)


def test_call_ok(monkeypatch):
    def mock_get(*args, **kwargs):
        return Mock_request(200)

    monkeypatch.setattr(requests, "request", mock_get)
    req = Gam().call(url="test.json")
    assert req['features'] == [{
      "type": "Feature",
      "properties": {
        "ELEM_POINT_ID": 22519,
        "CODE": "ESP28703"
      },
      "geometry": {
        "type": "Point",
        "coordinates": [
          5.70497723253789,
          45.188724499762
        ]
      }
    }]


def test_call_fail(monkeypatch):
    def mock_get(*args, **kwargs):
        return Mock_request(404)

    monkeypatch.setattr(requests, "request", mock_get)
    with pytest.raises(BadStatusError):
        Gam().call(url="test.json")
