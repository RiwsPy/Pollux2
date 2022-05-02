import maps
import pytest


class mock_Default_Config(maps.Default_Config):
    _DEFAULT_DATA = {
        'test': 'default_value'}
    _DEFAULT_DESCRIPTION = {
        'name': 'default_value'
    }


class mock_Config(mock_Default_Config):
    ID = 1
    DATA = {
        'test': 'test ok',
        'description': {
            'href': '/map/X'
        }
    }


@pytest.fixture
def fix_default_cls(monkeypatch):
    monkeypatch.setattr(maps, 'Default_Config', mock_Default_Config)
    return mock_Config()


def test_data(fix_default_cls):
    expected_value = {'test': 'test ok', 'description': {'name': 'default_value', 'href': '/map/X'}}
    assert fix_default_cls.data == expected_value


def test_description(fix_default_cls):
    expected_value = {'name': 'default_value', 'href': '/map/X'}
    assert fix_default_cls.description == expected_value


def test_href(fix_default_cls):
    expected_value = '/map/1'
    assert fix_default_cls.href == expected_value


def test__dict__(fix_default_cls):
    expected_value = {'test': 'test ok', 'href': '/map/1', 'description': {'name': 'default_value', 'href': '/map/X'}}
    assert fix_default_cls.__dict__ == expected_value
