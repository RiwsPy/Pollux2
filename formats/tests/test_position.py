from ..position import Position, LNG_1M, LAT_1M


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
    assert round(a.distance(b), 5) == 1
    c = a + [0, LAT_1M]
    assert round(a.distance(c), 5) == 1

    a = Position([0.0, 0.0])
    b = Position([1.0, 1.0])
    assert round(a.distance(b), 5) == 157249.38127


def test_distance_from_way():
    a = Position([1, 1])
    assert round(a.distance_from_way(Position([1, 1]), Position()), 5) == 0
    assert round(a.distance_from_way(Position([1+LNG_1M*10, 1]), Position([1+LNG_1M*20, 1+LAT_1M])), 5) == 9.99848
    assert round(a.distance_from_way(Position([0, 0]), Position([2, 2])), 5) == 0
    assert round(a.distance_from_way(Position([2, 0]), Position([2, 2])), 5) == 157249.38127


def test_projection():
    a = Position()
    assert a.projection(distance=1, orientation=0) == Position([0, LAT_1M])
    assert a.projection(distance=1, orientation=360) == Position([0, LAT_1M])
    assert a.projection(distance=1, orientation=90) == Position([LNG_1M, 0])
    assert a.projection(distance=1, orientation=270) == Position([-LNG_1M, 0])
    assert a.projection(distance=1, orientation=180) == Position([0, -LAT_1M])
    assert a.projection(distance=1, orientation=45) == Position([LNG_1M/2, LAT_1M/2])
    assert a.projection(distance=1, orientation=225) == Position([LNG_1M/2, -LAT_1M/2])
