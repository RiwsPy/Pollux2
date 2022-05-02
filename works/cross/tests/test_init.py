from .. import Works_cross
from ... import crossings, Default_works


def test_works_cross_init():
    w = Works_cross()
    assert w.teams == []
    assert w.copyrights == set()
    assert w.db_name == '__init__----25'
    assert w.COPYRIGHT == ''
    assert w.features == []


class mock_crossings(Default_works):
    filename = "tests/mock_geojson"
    file_ext = 'json'
    COPYRIGHT_ORIGIN = 'truc'
    COPYRIGHT_LICENSE = 'test'
    output_filename = "tests/mock_geojson"


def test_db_name(monkeypatch):
    monkeypatch.setattr('works.crossings.Works', mock_crossings)

    w = Works_cross()
    w.load([crossings], [crossings])
    assert w.db_name.count("tests/mock_geojson", 2)


def test_features(monkeypatch):
    monkeypatch.setattr('works.crossings.Works', mock_crossings)

    expected_features = crossings.Works().load()
    w = Works_cross()
    w.load([crossings], [crossings])
    assert w.features == expected_features['features'] + expected_features['features']


def test_copyright(monkeypatch):
    monkeypatch.setattr('works.crossings.Works', mock_crossings)

    test_works = crossings.Works()
    test_works.update(test_works.load())
    w = Works_cross()
    w.load([crossings], [crossings])
    assert w.COPYRIGHT == test_works.COPYRIGHT
