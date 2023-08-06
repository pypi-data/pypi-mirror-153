from openride import Polyline, Point, Transform
from openride.test.random_core_generator import get_random

from shapely import geometry

import pytest
import numpy as np




def test_init_numpy_array():
    pl = Polyline(np.random.random((10,3)))
    assert pl.vertices.shape == (10,3)


def test_init_list_points():
    pl = Polyline([Point(x) for x in range(2)])
    assert np.all(pl.vertices == np.array([[0,0,0],[1,0,0]]))


def test_polyline_to_shapely():
    pl = Polyline(np.random.random((10,3)))
    assert isinstance(pl.to_shapely(), geometry.LineString)


def test_line_transform_identity():
    l = get_random(Polyline)
    assert np.all(l.vertices == l.transform(Transform()).vertices)


def test_polyline_to_shapely_single_point():
    pl = Polyline(np.random.random((1,3)))
    assert isinstance(pl.to_shapely(), geometry.Point)


def test_len_polyline():
    pl = Polyline(np.random.random((10,3)))
    assert len(pl) == 10


def test_append():
    pl = Polyline(np.random.random((10,3)))
    pl2 = pl.append(Point())
    assert isinstance(pl2, Polyline)
    assert len(pl2) == 11


def test_extent():
    pl1 = Polyline(np.random.random((10,3)))
    pl2 = Polyline(np.random.random((10,3)))
    pl3 = pl1.extent(pl2)
    assert isinstance(pl3, Polyline)
    assert len(pl3) == 20


def test_polyline_distances():
    pl = Polyline([Point(x) for x in range(5)])
    assert np.all(pl.get_distances() == np.arange(5))


def test_polyline_total_distance():
    pl = Polyline([Point(x) for x in range(5)])
    assert pl.get_total_distance() == 4


def test_index_to_distance():
    pl = Polyline([Point(x) for x in range(10)])
    assert pl.index_to_distance(5.2) == 5.2


def test_distance_to_index():
    pl = Polyline([Point(x) for x in range(10)])
    assert pl.distance_to_index(5.2) == 5.2


def test_index_distance_reciprocal():
    for _ in range(10):
        pl = Polyline(np.random.random((10,3)))
        index = np.random.random() * pl.get_total_distance()
        distance = pl.index_to_distance(index)
        assert pytest.approx(pl.distance_to_index(distance)) == index


def test_getitem_int():
    pl = Polyline([Point(x) for x in range(10)])
    assert pl[5] == Point(5,0,0)


def test_getitem_float():
    pl = Polyline([Point(x) for x in range(10)])
    assert pytest.approx(pl[3.4].x) == 3.4


def test_getitem_float_zero_decimal():
    pl = Polyline([Point(x) for x in range(10)])
    assert pl[3.0].x == 3


def test_getitem_slice_integers():
    pl = Polyline([Point(x) for x in range(10)])
    assert np.all(pl[2:5].vertices == Polyline([Point(x) for x in range(2,5)]).vertices)


def test_getitem_slice_floats():
    pl = Polyline([Point(x) for x in range(10)])
    assert np.all(pytest.approx(pl[2.2:5.9].vertices) == Polyline([Point(x) for x in [2.2, 3, 4, 5, 5.9]]).vertices)


def test_iter_polyline():
    pl = Polyline([Point(x) for x in range(10)])
    for i, point in enumerate(pl):
        assert pl[i].x == Point(i).x
