from ..osm import Osm, get_query
import requests
import pytest
from .. import BadStatusError
import os
import json
from . import BASE_DIR


class Mock_request:
    def __init__(self, status_code: int):
        self.status_code = status_code

    @staticmethod
    def json():
        with open(os.path.join(BASE_DIR, 'db/tests/mock_osm.json'), 'r') as file:
            return json.load(file)


def test_call_ok(monkeypatch):
    def mock_get(*args, **kwargs):
        return Mock_request(200)

    monkeypatch.setattr(requests, "request", mock_get)
    req = Osm().call(query="")
    assert req['elements'] == [{
      "lat": 45.188724499762,
      "lon": 5.70497723253789,
      "type": "node",
      "tags": {
        "ELEM_POINT_ID": 22519,
        "CODE": "ESP28703"
      },
      "id": 2045858
    }]


def test_call_fail(monkeypatch):
    def mock_get(*args, **kwargs):
        return Mock_request(404)

    monkeypatch.setattr(requests, "request", mock_get)
    with pytest.raises(BadStatusError):
        Osm().call(query="")


default_query = b"""[out:json];

out body;"""


def test_get_query():
    assert get_query('') == default_query

    qur = 'node[highway=crossing]'
    assert get_query(qur) == b"""[out:json];
node[highway=crossing]
out body;"""

    assert b'[out:test];' in get_query('', out_format='test')
    assert get_query('', end='truc').rpartition(b'out truc;')[1:] == (b'out truc;', b'')
    assert get_query('', skel_qt=True).rpartition(b'out skel qt;')[1:] == (b'out skel qt;', b'')
