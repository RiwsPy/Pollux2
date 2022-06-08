from pollux.utils import linestring_to_polygon, update_deep

data = {
    'geometry': {
        'type': 'LineString',
        'coordinates': [
             [5.7054703, 45.1808808],
             [5.7054081, 45.1807483],
        ]
    },
    'properties': {
        'attr_test': 'ok'
    }
}
expected_data = {
    'geometry': {
        'type': 'Polygon',
        'coordinates': [
            [
                [5.705477935150345, 45.18087721580112],
                [5.705462664849655, 45.180884384198876],
                [5.705400464849655, 45.18075188419888],
                [5.7054157351503445, 45.18074471580112],
                [5.705477935150345, 45.18087721580112]
            ]
        ]
    },
    'properties': {
        'attr_test': 'ok'
    }
}


def test_linestring_to_polygon():
    ret = linestring_to_polygon(data['geometry']['coordinates'], width=2)
    assert ret == expected_data['geometry']['coordinates']

    ret = linestring_to_polygon(data['geometry']['coordinates'], width=0)
    p0 = data['geometry']['coordinates'][0]
    p1 = data['geometry']['coordinates'][1]
    assert ret == [[p0, p0, p1, p1, p0]]


dict_a = {'a': 1, 'b': {'test': 1, 'lolo': 2}}
dict_b = {'a': 2, 'c': 4, 'b': {'lolo': 'ok'}}
expected_dict_ab = {'a': 2, 'c': 4, 'b': {'test': 1, 'lolo': 'ok'}}
dict_c = {'a': 1, 'b': 2}
dict_d = {'b': 1}
expected_dict_cd = {'a': 1, 'b': 1}


def test_update_deep():
    update_deep(dict_c, dict_d)
    assert dict_c == expected_dict_cd

    update_deep(dict_a, dict_b)
    assert dict_a == expected_dict_ab
