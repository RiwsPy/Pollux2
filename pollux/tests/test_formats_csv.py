from pollux.formats.csv import convert_to_geojson
import os
from pollux.formats.geojson import Geojson


def test_convert_to_geojson(base_dir, db_dir):
    with open(os.path.join(base_dir, db_dir, 'mock_csv.csv'), 'r') as file:
        geojson_file = convert_to_geojson(file)
        ret_geojson = Geojson()
        ret_geojson.append({'Num_Acc': '202000000001',
                            'jour': '7',
                            'lat': '5.8',
                            'lon': '45.1'})
        assert geojson_file == ret_geojson
