from openride.core.point import Point
from openride.core.polygon import Polygon
from openride.core.transform import Transform
from openride.test import get_pytest_benchmark
from openride.test.random_core_generator import get_random

from shapely import geometry

import numpy as np
import pytest



pytest_benchmark = get_pytest_benchmark(group="core.polygon")


def test_init_list_points():
    p = Polygon([Point(x) for x in range(10)]+[Point(0)])
    assert p.vertices.shape == (11,3)


def test_post_init_connect_ends():
    p = get_random(Polygon)
    assert np.all(p.vertices[0] == p.vertices[-1])


def test_polygon_to_shapely():
    assert isinstance(get_random(Polygon).to_shapely(), geometry.Polygon)


@pytest_benchmark
def test_polygon_transform_identity(benchmark):
    polygon = get_random(Polygon)
    tf = Transform()
    polygon_tf = benchmark(polygon.transform, tf)
    assert np.all(polygon.vertices == polygon_tf.vertices)


def test_polygon_from_shapely():
    p1 = get_random(Polygon)
    p2 = Polygon.from_shapely(p1.to_shapely())
    assert np.all(pytest.approx(p1.vertices) == p2.vertices)


@pytest_benchmark
def test_polygon_area(benchmark):
    poly = Polygon([Point(1,1), Point(-1,1), Point(-1,-1), Point(1,-1)])
    assert benchmark(poly.get_area) == 4.0
