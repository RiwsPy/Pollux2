from ..csv import convert_to_geojson
import os
from ..geojson import Geojson
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def test_convert_to_geojson():
    with open(os.path.join(BASE_DIR, 'db/tests/mock_csv.csv'), 'r') as file:
        geojson_file = convert_to_geojson('', file)
        ret_geojson = Geojson()
        ret_geojson.append({'Num_Acc': '202000000001',
                            'jour': '7',
                            'lat': '5.8',
                            'lon': '45.1'})
        assert geojson_file == ret_geojson
