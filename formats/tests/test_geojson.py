from ..geojson import Geojson, Geo_Feature, coord_pos_to_float
import pytest


def test_init_geojson():
    g = Geojson()
    assert g == {'type': 'FeatureCollection', 'COPYRIGHT': '', 'features': []}
    assert g.features == []

    with pytest.raises(KeyError):
        g['test']

    g.test = 'ok'
    assert g['test'] == 'ok'


def test_geojson_append():
    g = Geojson()
    g.append(1)
    assert g == {'type': 'FeatureCollection', 'COPYRIGHT': '', 'features': [1]}


def test_geojson_copyright():
    cpr = 'Test Copyright ok'
    g = Geojson(COPYRIGHT=cpr)
    assert g == {'COPYRIGHT': cpr, 'type': 'FeatureCollection', 'features': []}


def test_feature_init():
    f = Geo_Feature()
    assert f == {'type': 'Feature',
                 'properties': {},
                 'geometry': {'type': 'Point',
                              'coordinates': [0.0, 0.0]}}


def test_feature_setitem():
    f = Geo_Feature()
    f['test'] = 1
    assert f.properties == {'test': 1}

    f['properties'] = 1
    assert f.properties == 1


def test_feature_setitem_position():
    f = Geo_Feature()
    f['lat'] = 0.5
    with pytest.raises(KeyError):
        f['lat']

    f['lon'] = 1
    with pytest.raises(KeyError):
        f['lon']

    assert f.geometry['coordinates'] == [1, 0.5]

    f['lng'] = 12
    assert f.geometry['coordinates'] == [12, 0.5]
    f['long'] = 15
    assert f.geometry['coordinates'] == [15, 0.5]


def test_coord_pos_to_float():
    assert coord_pos_to_float(1.0) == 1.0
    assert coord_pos_to_float(1) == 1.0
    assert coord_pos_to_float("1") == 1.0
    assert coord_pos_to_float("1.2") == 1.2
    assert coord_pos_to_float("1,2") == 1.2
