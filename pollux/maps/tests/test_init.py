from pollux import maps
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


def test_description(fix_default_cls):
    expected_value = {'name': 'default_value', 'href': '/map/X'}
    assert fix_default_cls.description == expected_value
