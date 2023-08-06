from openride import Point, BoundingBox, Polygon, Polyline, Size, contains
from openride.test import get_pytest_benchmark



pytest_benchmark = get_pytest_benchmark(group="operations.contains_3D")


@pytest_benchmark
def test_contains_box_point_true(benchmark):
    box = BoundingBox()
    point = Point()
    assert benchmark(contains, box, point)


def test_contains_box_point_false():
    assert not contains(BoundingBox(), Point(0,0,5))


def test_contains_box_point_on_edge():
    assert contains(BoundingBox(), Point(1))


@pytest_benchmark
def test_contains_box_box_true(benchmark):
    box1 = BoundingBox(size=Size(1,1,1))
    box2 = BoundingBox(size=Size(0.1,0.1,0.1))
    assert benchmark(contains, box1, box2)


def test_contains_box_box_false():
    assert not contains(BoundingBox(size=Size(1,1,1)), BoundingBox(size=Size(2,2,2)))


def test_contains_box_box_partial_false():
    assert not contains(BoundingBox(), BoundingBox(Point(1,1,1)))


@pytest_benchmark
def test_contains_box_polyline_true(benchmark):
    box = BoundingBox()
    polyline = Polyline([Point(), Point(0.5)])
    assert benchmark(contains, box, polyline)


def test_contains_box_polyline_false():
    assert not contains(BoundingBox(), Polyline([Point(), Point(1.5)]))


@pytest_benchmark
def test_contains_box_polygon_true(benchmark):
    box = BoundingBox()
    polygon = Polygon([Point(), Point(0.5), Point(0.5, 0.5)])
    assert benchmark(contains, box, polygon)


def test_contains_box_polygon_false():
    assert not contains(BoundingBox(), Polygon([Point(), Point(1.5), Point(1.5, 1.5)]))


@pytest_benchmark
def test_contains_polyline_point_true(benchmark):
    polyline = Polyline([Point(x,x,x) for x in range(2)])
    point = Point(0.5,0.5,0.5)
    assert benchmark(contains, polyline, point)


def test_contains_polyline_point_false():
    pl = Polyline([Point(x,x,x) for x in range(2)])
    assert not contains(pl, Point(0.5,0.5,0.0))


@pytest_benchmark
def test_contains_polyline_polyline_true(benchmark):
    pl1 = Polyline([Point(x,x,x) for x in range(5)])
    pl2 = Polyline([Point(x,x,x) for x in range(1,4)])
    assert benchmark(contains, pl1, pl2)


def test_contains_polyline_polyline_false():
    pl1 = Polyline([Point(x,x,x) for x in range(5)])
    pl2 = Polyline([Point(x,x,x) for x in range(1,6)])
    assert not contains(pl1, pl2)
