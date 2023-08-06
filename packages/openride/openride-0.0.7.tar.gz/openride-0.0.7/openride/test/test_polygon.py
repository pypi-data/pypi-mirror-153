from openride.core.point import Point
from openride.core.polygon import Polygon
from openride.core.transform import Transform
from openride.test.random_core_generator import get_random

from shapely import geometry

import numpy as np
import pytest



def test_init_list_points():
    p = Polygon([Point(x) for x in range(10)]+[Point(0)])
    assert p.vertices.shape == (11,3)


def test_post_init_connect_ends():
    p = get_random(Polygon)
    assert np.all(p.vertices[0] == p.vertices[-1])


def test_polygon_to_shapely():
    assert isinstance(get_random(Polygon).to_shapely(), geometry.Polygon)


def test_polygon_transform_identity():
    p = get_random(Polygon)
    assert np.all(p.vertices == p.transform(Transform()).vertices)


def test_polygon_from_shapely():
    p1 = get_random(Polygon)
    p2 = Polygon.from_shapely(p1.to_shapely())
    assert np.all(pytest.approx(p1.vertices) == p2.vertices)


def test_polygon_area():
    poly = Polygon([Point(1,1), Point(-1,1), Point(-1,-1), Point(1,-1)])
    assert poly.get_area() == 4.0