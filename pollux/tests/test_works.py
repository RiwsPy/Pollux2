import os.path
from pollux.formats.position import Position
from pollux.formats.osm import convert_to_geojson
from pollux.works import Default_works
import pytest
import json

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


def test_load(base_dir, db_dir):
    w = Default_works()
    data_test = w.load('mock_geojson', 'json', directory=db_dir)
    with open(os.path.join(base_dir, db_dir, 'mock_geojson.json'), 'r') as file:
        expected_value = json.load(file)
    assert data_test['features'] == expected_value['features']


def test_convert_osm_to_geojson(db_dir):
    w = Default_works()
    data_test = w.load('mock_osm', 'json', directory=db_dir)
    w2 = Default_works()
    expected_value = w2.load('mock_geojson', 'json', directory=db_dir)
    assert convert_to_geojson(data_test) == expected_value

    del data_test['elements']
    with pytest.raises(KeyError):
        convert_to_geojson(data_test)


def test_convert_osm_to_geojson_way(db_dir):
    w = Default_works()
    data_test = w.load('mock_osm_way', 'json', directory=db_dir)
    w2 = Default_works()
    expected_value = w2.load('mock_geojson_way', 'json', directory=db_dir)
    assert convert_to_geojson(data_test) == expected_value


def test_can_be_output(db_dir):
    w = Default_works(bound=DEFAULT_BOUND)
    data = w.load('mock_geojson', 'json', directory=db_dir)
    for feature in data['features']:
        feature = Default_works.Model(**feature)
        assert w._can_be_output(feature)
        feature.position = Position([0.0, 0.0])
        assert not w._can_be_output(feature)


def test_fake_request(db_dir):
    w = Default_works()
    w.fake_request = True
    assert w.request(directory=db_dir) == w.load(directory=db_dir)


def test_bound():
    w = Default_works()
    assert w.bound

    expected_value = [1, 2]
    w = Default_works(bound=expected_value)
    assert w.bound == expected_value

    expected_value = [1.23, 2.32]
    w.bound = expected_value
    assert w.bound == expected_value
