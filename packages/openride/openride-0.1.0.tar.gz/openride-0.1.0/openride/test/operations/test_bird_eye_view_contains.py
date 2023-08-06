from openride import Point, BoundingBox, Polyline, Polygon, Size, bird_eye_view_contains
from openride.test import get_pytest_benchmark



pytest_benchmark = get_pytest_benchmark(group="operations.bird_eye_view_contains")


@pytest_benchmark
def test_bev_contains_box_point_true(benchmark):
    box = BoundingBox(Point(4,8,-3))
    point = Point(4.5,7.5,5)
    assert benchmark(bird_eye_view_contains, box, point)


def test_bev_contains_box_point_false():
    assert not bird_eye_view_contains(BoundingBox(), Point(0,5,0))


@pytest_benchmark
def test_bev_contains_box_box_true(benchmark):
    box1 = BoundingBox()
    box2 = BoundingBox(Point(0,0,5), size=Size(0.5,0.5,2.5))
    assert benchmark(bird_eye_view_contains, box1, box2)


def test_bev_contains_box_box_false():
    assert not bird_eye_view_contains(BoundingBox(), BoundingBox(Point(0,0,5), size=Size(2.5,0.5,2.5)))


@pytest_benchmark
def test_bev_contains_box_polyline_true(benchmark):
    box = BoundingBox()
    polyline = Polyline([Point(), Point(0.5,0.3,2), Point(-0.3,0.7,-2)])
    assert benchmark(bird_eye_view_contains, box, polyline)


def test_bev_contains_box_polyline_false():
    polyline = Polyline([Point(), Point(2.5,0.3,2), Point(-0.3,0.7,-2)])
    assert not bird_eye_view_contains(BoundingBox(), polyline)


@pytest_benchmark
def test_bev_contains_box_polygon_true(benchmark):
    box = BoundingBox()
    polygon = Polygon([Point(), Point(0.5,0.3,2), Point(-0.3,0.7,-2)])
    assert benchmark(bird_eye_view_contains, box, polygon)


def test_bev_contains_box_polygon_false():
    polygon = Polygon([Point(), Point(2.5,0.3,2), Point(-0.3,0.7,-2)])
    assert not bird_eye_view_contains(BoundingBox(), polygon)


@pytest_benchmark
def test_bev_contains_polyline_point_true(benchmark):
    polyline = Polyline([Point(x,x,x) for x in range(5)])
    point = Point(1.3,1.3,-5)
    assert benchmark(bird_eye_view_contains, polyline, point)


def test_bev_contains_polyline_point_false():
    polyline = Polyline([Point(x,x,x) for x in range(5)])
    assert not bird_eye_view_contains(polyline, Point(1.2,1.3,-5))


@pytest_benchmark
def test_bev_contains_polyline_polyline_true(benchmark):
    pl1 = Polyline([Point(x,x,x) for x in range(5)])
    pl2 = Polyline([Point(x,x,-x) for x in range(1,4)])
    assert benchmark(bird_eye_view_contains, pl1, pl2)


def test_bev_contains_polyline_polyline_false():
    pl1 = Polyline([Point(x,x,x) for x in range(5)])
    pl2 = Polyline([Point(x,x,-x) for x in range(1,4)] + [Point(2,1,0)])
    assert not bird_eye_view_contains(pl1, pl2)


@pytest_benchmark
def test_bev_contains_polygon_point_true(benchmark):
    polygon = Polygon([Point(1,1), Point(-1,1), Point(-1,-1), Point(1,-1)])
    point = Point(0,0,4)
    assert benchmark(bird_eye_view_contains, polygon, point)


def test_bev_contains_polygon_point_false():
    polygon = Polygon([Point(1,1), Point(-1,1), Point(-1,-1), Point(1,-1)])
    assert not bird_eye_view_contains(polygon, Point(3,0,4))


@pytest_benchmark
def test_bev_contains_polygon_box_true(benchmark):
    polygon = Polygon([Point(2,2), Point(-2,2), Point(-2,-2), Point(2,-2)])
    box = BoundingBox(Point(0,0,-3))
    assert benchmark(bird_eye_view_contains, polygon, box)


def test_bev_contains_polygon_box_false():
    polygon = Polygon([Point(2,2), Point(-2,2), Point(-2,-2), Point(2,-2)])
    assert not bird_eye_view_contains(polygon, BoundingBox(Point(0,1.5,-3)))


@pytest_benchmark
def test_bev_contains_polygon_polyline_true(benchmark):
    polygon = Polygon([Point(3,3), Point(-3,3), Point(-3,-3), Point(3,-3)])
    polyline = Polyline([Point(x,x,x) for x in range(2)])
    assert benchmark(bird_eye_view_contains, polygon, polyline)


def test_bev_contains_polygon_polyline_false():
    polygon = Polygon([Point(2,2), Point(-2,2), Point(-2,-2), Point(2,-2)])
    polyline = Polyline([Point(x,x,x) for x in range(5)])
    assert not bird_eye_view_contains(polygon, polyline)


@pytest_benchmark
def test_bev_contains_polygon_polygon_true(benchmark):
    pg1 = Polygon([Point(3,3), Point(-3,3), Point(-3,-3), Point(3,-3)])
    pg2 = Polygon([Point(2,2,3), Point(-2,2), Point(-2,-2), Point(2,-2)])
    assert benchmark(bird_eye_view_contains, pg1, pg2)


def test_bev_contains_polygon_polygon_false():
    pg1 = Polygon([Point(3,3), Point(-3,3), Point(-3,-3), Point(3,-3)])
    pg2 = Polygon([Point(2,2,3), Point(-2,2), Point(-2,-2), Point(2,-2)])
    assert not bird_eye_view_contains(pg2, pg1)
