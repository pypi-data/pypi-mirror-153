from openride.core.point import Point
from openride.core.rotation import Rotation
from openride.core.transform import Transform
from openride.test import get_pytest_benchmark

from shapely import geometry

import numpy as np
import pytest



pytest_benchmark = get_pytest_benchmark(group="core.point")


def test_point_init():
    p = Point(1,2,3)
    assert p.x == 1 and p.y == 2 and p.z == 3


def test_point_to_shapely():
    p = Point(1,2,3)
    ps = p.to_shapely()
    assert isinstance(ps, geometry.Point)


@pytest_benchmark
def test_transform_point(benchmark):
    p = Point(0,0,0)
    tf = Transform()
    p2 = benchmark(p.transform, tf)
    assert p == p2


def test_translate_point():
    p = Point(1,2,3)
    tf = Transform(Point(4,5,6))
    p2 = p.transform(tf)
    assert p2 == Point(5,7,9)


def test_rotate_x_point():
    p = Point(1,1,1)
    tf = Transform(rotation=Rotation(roll=np.pi/2))
    p2 = p.transform(tf)
    assert pytest.approx(p2.x) == 1
    assert pytest.approx(p2.y) == 1
    assert pytest.approx(p2.z) == -1


def test_rotate_y_point():
    p = Point(1,1,1)
    tf = Transform(rotation=Rotation(pitch=np.pi/2))
    p2 = p.transform(tf)
    assert pytest.approx(p2.x) == -1
    assert pytest.approx(p2.y) == 1
    assert pytest.approx(p2.z) == 1


def test_rotate_z_point():
    p = Point(1,1,1)
    tf = Transform(rotation=Rotation(yaw=np.pi/2))
    p2 = p.transform(tf)
    assert pytest.approx(p2.x) == 1
    assert pytest.approx(p2.y) == -1
    assert pytest.approx(p2.z) == 1


@pytest_benchmark
def test_add_points(benchmark):
    p1 = Point(1,2,3)
    p2 = Point(4,5,6)
    assert benchmark(p1.__add__, p2) == Point(5,7,9)


def test_substract_points():
    p1 = Point(1,2,3)
    p2 = Point(4,5,6)
    assert p1 - p2 == Point(-3,-3,-3)


def test_multiply_point():
    p = Point(1,2,3)
    assert p*2 == Point(2,4,6)


def test_reverse_multiply_point():
    p = Point(1,2,3)
    assert 2*p == Point(2,4,6)


def test_repr_point():
    assert isinstance(str(Point()), str)
