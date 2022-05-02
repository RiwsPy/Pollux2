import os.path
from formats.position import Position
from .. import Default_works, convert_osm_to_geojson
import pytest
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LAT_MAX = 45.198848
LAT_MIN = 45.187501
LNG_MAX = 5.725703
LNG_MIN = 5.704696
DEFAULT_BOUND = [LAT_MIN, LNG_MIN, LAT_MAX, LNG_MAX]


def test_base():
    w = Default_works()
    assert w.COPYRIGHT == 'The data included in this document is from unknown.' +\
                          ' The data is made available under unknown.'

    assert w.output_filename == 'empty_output'


def test_load():
    w = Default_works()
    data_test = w.load('tests/mock_geojson', 'json')
    with open(os.path.join('db/tests/mock_geojson.json'), 'r') as file:
        expected_value = json.load(file)
    assert data_test['features'] == expected_value['features']

    with pytest.raises(TypeError):
        w.load('tests/empty', 'bad_ext')


def test_iter():
    w = Default_works()
    w.update(w.load('empty', 'json'))
    for feature1, feature2 in zip(w, w.features):
        assert feature1 == feature2


def test_convert_osm_to_geojson():
    w = Default_works()
    data_test = w.load('tests/mock_osm', 'json')
    w2 = Default_works()
    expected_value = w2.load('tests/mock_geojson', 'json')
    assert convert_osm_to_geojson(data_test) == expected_value

    del data_test['elements']
    with pytest.raises(KeyError):
        convert_osm_to_geojson(data_test)


def test_convert_osm_to_geojson_way():
    w = Default_works()
    data_test = w.load('tests/mock_osm_way', 'json')
    w2 = Default_works()
    expected_value = w2.load('tests/mock_geojson_way', 'json')
    assert convert_osm_to_geojson(data_test) == expected_value


def test_can_be_output():
    w = Default_works(bound=DEFAULT_BOUND)
    w.update(w.load('tests/mock_geojson', 'json'))
    for feature in w:
        assert w._can_be_output(feature)

    for feature in w:
        feature.position = Position([0.0, 0.0])
        assert not w._can_be_output(feature)


def test_fake_request():
    w = Default_works()
    w.fake_request = True
    assert w.request() == w.load()


def test_bound():
    w = Default_works()
    assert w.bound

    expected_value = [1, 2]
    w = Default_works(bound=expected_value)
    assert w.bound == expected_value

    expected_value = [1.23, 2.32]
    w.bound = expected_value
    assert w.bound == expected_value
