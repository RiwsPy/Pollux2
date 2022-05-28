from pollux.formats.position import Position, LNG_1M, LAT_1M, LAT_TO_LNG, LNG_TO_LAT
import pytest


def test_create():
    assert Position([0.0, 0.0]) == [0.0, 0.0]


def test_add():
    a = Position([1.0, 0.0])
    b = Position([0.0, 2.3])
    assert a + b == [1.0, 2.3]


def test_truediv():
    a = Position([1.0, 2.0])
    assert a / 2 == [0.5, 1.0]


def test_distance():
    a = Position()
    b = a + [LNG_1M, 0]
    assert round(a.distance(b), 5) == round(1, 5)
    c = a + [0, LAT_1M]
    assert round(a.distance(c), 5) == round(1, 5)

    a = Position([0.0, 0.0])
    b = Position([1.0, 1.0])
    assert round(a.distance(b), 5) == 157249.38127


def test_distance_cartesian():
    a = Position()
    b = a + [LNG_1M, 0]
    assert round(a.distance_cartesian(b), 5) == 1
    c = a + [0, LAT_1M]
    assert round(a.distance_cartesian(c), 5) == round(1, 5)


def test_nearest_point_from_way():
    a = Position([0, 0])
    assert a.nearest_point_from_way([0, 0], [0, 0]) == [0, 0]
    assert a.nearest_point_from_way([1, 1], [2, 2]) == [0, 0]


"""
def test_distance_from_way():
    a = Position([5.71091412, 45.18741829])
    b = [[5.7124465, 45.1873667], [5.7115641, 45.187425]]
    assert a.distance_from_way(b[0], b[1]) == 1

    b = Position()
    assert round(b.distance_from_way(Position([1, 1]), Position()), 5) == 0
    assert round(b.distance_from_way(Position(), Position([2, 2])), 5) == 0
    assert round(b.distance_from_way(Position([LNG_1M*10, 0]), Position([LNG_1M*20, LAT_1M])), 5) == round(10*LNG_TO_LAT, 5)
    assert round(b.distance_from_way(Position([0, LAT_1M*2]), Position([LNG_1M*2, LAT_1M*2])), 5) == round(2, 5)
    assert round(b.distance_from_way(Position([-LNG_1M, LAT_1M]), Position([LNG_1M, LAT_1M])), 5) == round(1, 5)
    #assert round(b.distance_from_way(Position([LNG_1M*-2, LAT_1M*4]), Position([LNG_1M, LAT_1M])), 5) == round(2**0.5, 5)
"""

def test_orientation():
    a = Position()
    assert a.orientation([0, 1]) == 0
    assert a.orientation([1, 0]) == 90
    assert a.orientation([0, -1]) == 180
    assert a.orientation([-1, 0]) == 270
    # TODO modificateur à intégrer
    """
    assert a.orientation([0.5, 0.5]) == 45
    assert a.orientation([10, 10]) == 45
    assert a.orientation([0.5, -0.5]) == 135
    assert a.orientation([-0.5, 0.5]) == 315
    assert a.orientation([-0.5, -0.5]) == 225
    assert a.orientation([1, 1/2]) == 60
    """
    with pytest.raises(ZeroDivisionError):
        assert a.orientation([0, 0])

    a = Position([3.384, 45.323747])
    b = Position([3.97575, 45.13842])
    mid = Position([a.lng+(b.lng-a.lng)/2, a.lat+(b.lat-a.lat)/2])
    assert round(a.orientation(b), 5) == round((b.orientation(a) + 180) % 360, 5)
    assert round(a.orientation(b), 5) == round(a.orientation(mid), 5)
    assert round(b.orientation(a), 5) == round(b.orientation(mid), 5)


def test_to_position():
    a = Position([[0, 0], [1, 1]])
    assert a.force_position() == [0.5, 0.5]
    a = Position([[[0, 0], [1, 1]], [[1, 1], [2, 2]]])
    assert a.force_position() == [1, 1]


"""
def test_projection():
    a = Position()
    test_values = [
        # position, orientation, expected_distance
        [[0, LAT_1M], 0, 1*LAT_TO_LNG],
        [[0, LAT_1M], 360, 1*LAT_TO_LNG],
        [[LNG_1M, 0], 90, 1],
        [[-LNG_1M, 0], 270, 1],
        [[0, -LAT_1M], 180, 1*LAT_TO_LNG],
        # [[LNG_1M/2, LAT_1M/2], 45, 0.71],
        # [[-LNG_1M/2, -LAT_1M/2], 225, 0.71],
    ]

    for values in test_values:
        print(values, 'en cours...')
        expected_position = Position(values[0])
        ret = a.projection(distance=1, orientation=values[1])
        assert ret == expected_position
        assert a.orientation(expected_position) == values[1] % 360
        assert round(a.distance(expected_position), 2) == round(values[2], 2)
"""
