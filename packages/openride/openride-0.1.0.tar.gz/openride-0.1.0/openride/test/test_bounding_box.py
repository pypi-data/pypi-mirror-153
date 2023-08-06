from openride.core.bounding_box import BoundingBox
from openride.core.numba.transforms import transform_vertices
from openride.core.point import Point
from openride.core.rotation import Rotation
from openride.core.size import Size
from openride.test.random_core_generator import get_random
from openride.core.transform import Transform
from openride.test import get_pytest_benchmark

from shapely import geometry

import numpy as np
import pytest



pytest_benchmark = get_pytest_benchmark(group="core.bounding_box")


def test_init():
    b = BoundingBox()
    assert b.position == Point()
    assert b.rotation == Rotation()
    assert b.size == Size()


@pytest_benchmark
def test_box_get_bird_eye_view_vertices(benchmark):
    box = BoundingBox()
    vertices = benchmark(box.get_bird_eye_view_vertices)
    assert vertices.shape == (4,2)


def test_bird_eye_view_vertices_translation():
    v = BoundingBox(Point(1,2,3)).get_bird_eye_view_vertices()
    assert np.all(v == np.array([[2,3],[2,1],[0,1],[0,3]]))


def test_bird_eye_view_vertices_rotation():
    v = BoundingBox(rotation=Rotation(0,0,np.pi/6)).get_bird_eye_view_vertices()
    x = np.sin(np.deg2rad(15))*2**0.5
    assert np.all(pytest.approx(v) == np.array([[x,1+x],[1+x,-x],[-x,-1-x],[-1-x,x]]))


def test_bird_eye_view_vertices_scale():
    v = BoundingBox(size=Size(2,2,2)).get_bird_eye_view_vertices()
    assert np.all(v == np.array([[2,2],[2,-2],[-2,-2],[-2,2]]))


@pytest_benchmark
def test_box_get_vertices(benchmark):
    box = BoundingBox()
    vertices = benchmark(box.get_vertices)
    assert vertices.shape == (8,3)


def test_bounding_box_to_shapely():
    b = BoundingBox()
    assert isinstance(b.to_shapely(), geometry.Polygon)


def test_get_transform():
    b = BoundingBox()
    assert isinstance(b.get_transform(), Transform)


def test_box_transform_identity():
    b = BoundingBox()
    assert b == b.transform(Transform())


def test_box_rotation():
    b = BoundingBox()
    tf = Transform(rotation=Rotation(0,0,np.pi/6))
    assert pytest.approx(b.transform(tf).rotation.yaw) == np.pi/6


@pytest_benchmark
def test_box_transform(benchmark):
    box = get_random(BoundingBox)
    tf = Transform(Point(*np.random.random(3)*10), Rotation(0,0,np.random.random()*2*np.pi))
    benchmark(box.transform, tf)
    v1 = box.transform(tf).get_vertices()
    v2 = transform_vertices(box.get_vertices(), tf.get_matrix())
    assert np.all(pytest.approx(v1) == v2)
        