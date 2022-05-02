from website.tests.conftest import client
import pytest
import json
from ..views import BASE_DIR
import os


@pytest.mark.parametrize("url", [
			'/', '/map/1', '/api/1', '/api/cross/1',
			'/mentions_legales/', '/about/', '/encyclopedia/',
			'/map_desc/1'])
def test_status_code_ok(client, url):
	print('test_status_code_ok', url)
	response = client.get(url)
	assert response.status_code == 200


def test_show_unknown_map(client):
	expected_response = client.get('/').data.decode()
	response = client.get('/map/testsdjsnc')
	assert response.data.decode() == expected_response


def test_show_unknown_map_desc(client):
	expected_response = client.get('/').data.decode()
	response = client.get('/map_desc/testsdjsnc')
	assert response.data.decode() == expected_response


def test_show_invert_map(client):
	expected_response = client.get('map/1').data.decode()
	response = client.get('/map/-1')
	assert response.data.decode() == expected_response


def test_api_known_file(client):
	filename = 'tests/mock_geojson.json'
	response = client.get('/api/' + filename)
	with open(os.path.join(BASE_DIR, 'db', filename), 'r') as file:
		expected_response = json.load(file)
	assert expected_response == json.loads(response.data.decode())


def test_api_unknown_file(client):
	response = client.get('/api/test.jsidsfd')
	response_json = json.loads(response.data)
	assert len(response_json) == 1
	assert 'Error' in response_json
