from openride import Point, BoundingBox, Polyline, Rotation, Size, distance
from openride.test import get_pytest_benchmark

import numpy as np
import pytest



pytest_benchmark = get_pytest_benchmark(group="operations.distance_3D")


@pytest_benchmark
def test_distance_point_point(benchmark):
    p1 = Point(1,1,1)
    p2 = Point(2,2,2)
    assert benchmark(distance, p1, p2) == 3**0.5


@pytest_benchmark
def test_distance_point_box(benchmark):
    b = BoundingBox()
    p = Point(2.,2.,2.)
    assert benchmark(distance, p, b) == 3**0.5
    assert distance(b, p) == 3**0.5


def test_distance_point_box_overlap():
    b = BoundingBox()
    p = Point(0.5,0.5,0.5)
    assert distance(p, b) == 0.0
    assert distance(b, p) == 0.0


def test_distance_point_box_edge():
    b = BoundingBox()
    p = Point(2.,0.,2.)
    assert distance(p, b) == 2**0.5
    assert distance(b, p) == 2**0.5


def test_distance_point_box_face():
    b = BoundingBox()
    p = Point(0.75,0.5,2)
    assert distance(p, b) == 1.0
    assert distance(b, p) == 1.0


@pytest_benchmark
def test_distance_point_line(benchmark):
    l = Polyline([Point(0,0,0), Point(1,0,1)])
    p = Point(0.5,0.5, 0.5)
    assert benchmark(distance, l, p) == pytest.approx(0.5)
    assert distance(p, l) == pytest.approx(0.5)


def test_distance_point_line_overlap():
    l = Polyline([Point(0,0,0), Point(1,1,1)])
    p = Point(0.75,0.75, 0.75)
    assert distance(l, p) == 0.0
    assert distance(p, l) == 0.0


def test_distance_point_line_far():
    l = Polyline([Point(0,0,0), Point(1,1,1)])
    p = Point(2,2,2)
    assert pytest.approx(distance(l, p)) == 3**0.5
    assert pytest.approx(distance(p, l)) == 3**0.5


@pytest_benchmark
def test_distance_box_box(benchmark):
    b1 = BoundingBox(Point(0,0,0), Rotation(0,0,0), Size(1,1,1))
    b2 = BoundingBox(Point(3,3,3), Rotation(0,0,0), Size(1,1,1))
    assert benchmark(distance, b1, b2) == 3**0.5
    assert distance(b2, b1) == 3**0.5


def test_distance_box_box_overlap():
    b1 = BoundingBox()
    b2 = BoundingBox(Point(0,0,2), Rotation(np.pi/4, np.pi/4, 0))
    assert distance(b1, b2) == 0.0
    assert distance(b2, b1) == 0.0


def test_distance_box_box_corner_to_face():
    b1 = BoundingBox()
    b2 = BoundingBox(Point(0,0,3), Rotation(np.pi/4, np.pi/4, 0))
    assert pytest.approx(distance(b1, b2)) == (2-2**0.5)/2
    assert pytest.approx(distance(b2, b1)) == (2-2**0.5)/2


def test_distance_box_box_edge_to_face():
    b1 = BoundingBox()
    b2 = BoundingBox(Point(0,0,5), Rotation(np.pi/4, 0, 0), Size(2,2,2))
    assert pytest.approx(distance(b1, b2)) == 4-2*2**.5
    assert pytest.approx(distance(b2, b1)) == 4-2*2**.5


@pytest_benchmark
def test_distance_box_line(benchmark):
    l = Polyline([Point(-1,2,2), Point(0,2,2), Point(1,2,2)])
    b = BoundingBox()
    assert benchmark(distance, l, b) == pytest.approx(2**0.5)
    assert distance(b, l) == pytest.approx(2**0.5)


def test_distance_box_line_overlap():
    l = Polyline([Point(0.5,0.5,0.5), Point(0,2,2), Point(1,2,2)])
    b = BoundingBox()
    assert distance(l, b) == 0.0
    assert distance(b, l) == 0.0


@pytest_benchmark
def test_distance_line_line(benchmark):
    l1 = Polyline([Point(0), Point(1), Point(2)])
    l2 = Polyline([Point(0.5,1,1), Point(1.5,1,1), Point(2.5,1,1)])
    assert benchmark(distance, l1, l2) == 2**0.5


def test_distance_line_line_far():
    l1 = Polyline([Point(0), Point(1), Point(2)])
    l2 = Polyline([Point(3,1,1), Point(4,1,1), Point(5,1,1)])
    assert distance(l1, l2) == 3**0.5


def test_distance_line_line_overlap():
    l1 = Polyline([Point(-1,-1,-1), Point(0,0,0), Point(1,1,1)])
    l2 = Polyline([Point(-1.5,0,0), Point(-0.5,0,0), Point(0.5,0,0)])
    assert distance(l1, l2) == 0.0
