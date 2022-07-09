from pollux.formats.csv import convert_to_geojson
from pollux.formats.geojson import Geojson


def test_convert_to_geojson(base_dir, db_dir):
    data_dict = convert_to_geojson(db_dir + "/mock_csv.csv")
    ret_geojson = Geojson()
    ret_geojson.append(
        {"Num_Acc": "202000000001", "jour": "7", "lat": "5.8", "lon": "45.1"}
    )
    assert data_dict == ret_geojson
