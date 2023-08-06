from openride import bird_eye_view_distance
from openride.core.bounding_box import BoundingBox
from openride.core.geometry import Geometry
from openride.core.point import Point
from openride.core.polygon import Polygon
from openride.core.polyline import Polyline
from openride.core.rotation import Rotation
from openride.core.size import Size
from openride.test import get_pytest_benchmark
from openride.test.random_core_generator import get_random

from shapely import geometry

import pytest
import numpy as np



pytest_benchmark = get_pytest_benchmark(group="operations.bird_eye_view_distance")


@pytest_benchmark
def test_bev_distance_point_point(benchmark):
    p1 = Point(0,0,0)
    p2 = Point(1,1,1)
    assert benchmark(bird_eye_view_distance, p1, p2) == 2**0.5


def test_bev_distance_point_box_inside():
    p = Point(0,0,0)
    b = BoundingBox()
    assert bird_eye_view_distance(p,b) == 0.0


@pytest_benchmark
def test_bev_distance_point_box(benchmark):
    p = Point(2,0,0)
    b = BoundingBox()
    assert benchmark(bird_eye_view_distance, p, b) == 1.0


@pytest_benchmark
def test_bev_distance_point_line(benchmark):
    p = Point(2,2,0)
    l = Polyline([Point(x) for x in range(5)])
    assert benchmark(bird_eye_view_distance, p, l) == 2.0


@pytest_benchmark
def test_bev_distance_point_polygon(benchmark):
    p = Point(2,2,0)
    poly = Polygon([Point(1,1), Point(-1,1), Point(-1,-1), Point(1,-1)])
    assert benchmark(bird_eye_view_distance, p, poly) == 2**0.5


@pytest_benchmark
def test_bev_distance_box_box(benchmark):
    b1 = BoundingBox(Point(0,0,0), Rotation(0,0,0), Size(1,1,1))
    b2 = BoundingBox(Point(2*2**0.5+1,0,0), Rotation(0,0,np.pi/4), Size(1,1,1))
    assert benchmark(bird_eye_view_distance, b1, b2) == pytest.approx(2**0.5)


def test_bev_distance_box_box_overlap():
    b1 = BoundingBox()
    b2 = BoundingBox(Point(0.5,0.5))
    assert bird_eye_view_distance(b1, b2) == 0.0


@pytest_benchmark
def test_bev_distance_box_line(benchmark):
    b = BoundingBox(Point(0,0,0), Rotation(0,0,0), Size(1,1,1))
    l = Polyline([Point(x+2) for x in range(10)])
    assert benchmark(bird_eye_view_distance, b, l) == pytest.approx(1.0)


def test_bev_distance_box_line_overlap():
    b = BoundingBox(Point(0,0,0), Rotation(0,0,0), Size(1,1,1))
    l = Polyline([Point(x) for x in range(10)])
    assert pytest.approx(bird_eye_view_distance(b, l)) == 0.0


@pytest_benchmark
def test_bev_distance_box_polygon(benchmark):
    b = BoundingBox(Point(3,0,0), Rotation(0,0,0), Size(1,1,1))
    p = Polygon([Point(1,1), Point(-1,1), Point(-1,-1), Point(1,-1)])
    assert benchmark(bird_eye_view_distance, b, p) == pytest.approx(1.0)


def test_bev_distance_box_polygon_overlap():
    b = BoundingBox(Point(0,0,0), Rotation(0,0,0), Size(1,1,1))
    p = Polygon([Point(1,1), Point(-1,1), Point(-1,-1), Point(1,-1)])
    assert pytest.approx(bird_eye_view_distance(b, p)) == 0.0


@pytest_benchmark
def test_bev_distance_line_point(benchmark):
    p = Point(5.3,5,5)
    l = Polyline([Point(x) for x in range(10)])
    assert benchmark(bird_eye_view_distance, l, p) == pytest.approx(5.0)


def test_bev_distance_line_point_overlap():
    p = Point(5.3,0,5)
    l = Polyline([Point(x) for x in range(10)])
    assert pytest.approx(bird_eye_view_distance(l, p)) == 0.0


@pytest_benchmark
def test_bev_distance_line_line(benchmark):
    l1 = Polyline([Point(x) for x in range(10)])
    l2 = Polyline([Point(5.5, y+1) for y in range(10)])
    assert benchmark(bird_eye_view_distance, l1, l2) == 1.0


def test_bev_distance_line_line_overlap():
    l1 = Polyline([Point(x) for x in range(10)])
    l2 = Polyline([Point(5, y-5) for y in range(10)])
    assert bird_eye_view_distance(l1, l2) == 0.0


def test_bev_distance_line_polygon_overlap():
    l = Polyline([Point(x) for x in range(10)])
    p = Polygon([Point(1,1), Point(-1,1), Point(-1,-1), Point(1,-1)])
    assert bird_eye_view_distance(l, p) == 0.0


@pytest_benchmark
def test_bev_distance_polygon_polygon(benchmark):
    p1 = Polygon([Point(1,1), Point(-1,1), Point(-1,-1), Point(1,-1)])
    p2 = Polygon([Point(2,0), Point(3,-1), Point(4,0), Point(3,1)])
    assert benchmark(bird_eye_view_distance, p1, p2) == pytest.approx(1.0)


def test_bev_distance_line_line_same_as_shapely():
    for _ in range(10):
        l1 = get_random(Polyline)
        l2 = get_random(Polyline)
        assert pytest.approx(bird_eye_view_distance(l1, l2)) == l1.to_shapely().distance(l2.to_shapely())


def test_bev_distance_point_point_same_as_shapely():
    for _ in range(10):
        p1 = get_random(Point)
        p2 = get_random(Point)
        assert pytest.approx(bird_eye_view_distance(p1, p2)) == p1.to_shapely().distance(p2.to_shapely())


def test_bev_distance_box_point_same_as_shapely():
    for _ in range(10):
        p = get_random(Point)
        b = get_random(BoundingBox)
        assert pytest.approx(bird_eye_view_distance(b, p)) == b.to_shapely().distance(p.to_shapely())


def test_bev_distance_box_box_same_as_shapely():
    for _ in range(10):
        b1 = get_random(BoundingBox)
        b2 = get_random(BoundingBox)
        assert pytest.approx(bird_eye_view_distance(b1, b2)) == b1.to_shapely().distance(b2.to_shapely())


def test_bev_distance_box_line_same_as_shapely():
    for _ in range(10):
        l = get_random(Polyline)
        b = get_random(BoundingBox)
        assert pytest.approx(bird_eye_view_distance(b, l)) == b.to_shapely().distance(l.to_shapely())


def test_bev_distance_line_point_same_as_shapely():
    for _ in range(10):
        p = get_random(Point)
        l = get_random(Polyline)
        assert pytest.approx(bird_eye_view_distance(l, p)) == l.to_shapely().distance(p.to_shapely())


def test_bev_distance_line_box_same_as_shapely():
    for _ in range(10):
        l = get_random(Polyline)
        b = get_random(BoundingBox)
        assert pytest.approx(bird_eye_view_distance(l, b)) == l.to_shapely().distance(b.to_shapely())
        

def test_bev_distance_polygon_point_same_as_shapely():
    for _ in range(10):
        poly = get_random(Polygon)
        p = get_random(Point)
        assert pytest.approx(bird_eye_view_distance(poly, p)) == poly.to_shapely().distance(p.to_shapely())
        

def test_bev_distance_polygon_box_same_as_shapely():
    for _ in range(10):
        p = get_random(Polygon)
        b = get_random(BoundingBox)
        assert pytest.approx(bird_eye_view_distance(p, b)) == p.to_shapely().distance(b.to_shapely())


def test_bev_distance_polygon_line_same_as_shapely():
    for _ in range(10):
        p = get_random(Polygon)
        l = get_random(Polyline)
        assert pytest.approx(bird_eye_view_distance(p, l)) == p.to_shapely().distance(l.to_shapely())
       

def test_bev_distance_polygons_same_as_shapely():
    for _ in range(10):
        p1 = get_random(Polygon)
        p2 = get_random(Polygon)
        assert pytest.approx(bird_eye_view_distance(p1, p2)) == p1.to_shapely().distance(p2.to_shapely())


def test_default_geometry_distance_from_shapely():

    class MockGeometry(Geometry):
        def to_shapely(self):
            return geometry.Point([1,1,1])
        def transform(self, transform):
            pass
    
    p1 = Point(0,0,0)
    p2 = MockGeometry()
    assert bird_eye_view_distance(p1, p2) == 2**0.5
