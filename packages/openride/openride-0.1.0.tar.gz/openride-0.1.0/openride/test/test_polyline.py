from openride import Polyline, Point, Transform
from openride.core.numba.coordinate_systems import spherical_to_cartesian
from openride.test import get_pytest_benchmark
from openride.test.random_core_generator import get_random

from shapely import geometry

import pytest
import numpy as np



pytest_benchmark = get_pytest_benchmark(group="core.polyline")


def test_init_numpy_array():
    pl = Polyline(np.random.random((10,3)))
    assert pl.vertices.shape == (10,3)


def test_init_list_points():
    pl = Polyline([Point(x) for x in range(2)])
    assert np.all(pl.vertices == np.array([[0,0,0],[1,0,0]]))


def test_polyline_to_shapely():
    pl = Polyline(np.random.random((10,3)))
    assert isinstance(pl.to_shapely(), geometry.LineString)


@pytest_benchmark
def test_line_transform_identity(benchmark):
    line = get_random(Polyline)
    tf = Transform()
    line_tf = benchmark(line.transform, tf)
    assert np.all(line.vertices == line_tf.vertices)


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


@pytest_benchmark
def test_polyline_get_distances(benchmark):
    pl = Polyline([Point(x) for x in range(5)])
    distances = benchmark(pl.get_distances)
    assert np.all(distances == np.arange(5))


def test_polyline_get_total_distance():
    pl = Polyline([Point(x) for x in range(5)])
    assert pl.get_total_distance() == 4


def test_polyline_get_total_distance_zero():
    assert Polyline().get_total_distance() == 0


@pytest_benchmark
def test_index_to_distance(benchmark):
    pl = Polyline([Point(x) for x in range(10)])
    distance = benchmark(pl.index_to_distance, 5.2)
    assert distance == 5.2


@pytest_benchmark
def test_distance_to_index(benchmark):
    pl = Polyline([Point(x) for x in range(10)])
    index = benchmark(pl.distance_to_index, 5.2)
    assert index == 5.2


def test_index_distance_reciprocal():
    for _ in range(10):
        pl = Polyline(np.random.random((10,3)))
        index = np.random.random() * pl.get_total_distance()
        distance = pl.index_to_distance(index)
        assert pytest.approx(pl.distance_to_index(distance)) == index


@pytest_benchmark
def test_getitem_int(benchmark):
    pl = Polyline([Point(x) for x in range(10)])
    result = benchmark(pl.__getitem__, 5)
    assert result == Point(5,0,0)


@pytest_benchmark
def test_getitem_float(benchmark):
    pl = Polyline([Point(x) for x in range(10)])
    result = benchmark(pl.__getitem__, 3.4)
    assert pytest.approx(result.x) == 3.4


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


@pytest_benchmark
def test_polyline_get_tangent_angles(benchmark):
    pl = Polyline([Point(x, x) for x in range(5)])
    tangents = benchmark(pl.get_tangent_angles)
    assert tangents.size == len(pl)
    assert np.all(tangents == pytest.approx(np.pi/4))


@pytest_benchmark
def test_polyline_get_radius_of_curvature(benchmark):
    pl = Polyline([Point(*spherical_to_cartesian(5, theta, np.pi/2)) for theta in np.arange(-np.pi/2, np.pi/2, 0.1)])
    radius_of_curvature = benchmark(pl.get_radius_of_curvature)
    assert radius_of_curvature.size == len(pl)
    assert np.all(radius_of_curvature == pytest.approx(5, rel=1e-2))


@pytest_benchmark
def test_polyline_resample(benchmark):
    pl = Polyline([Point(x, x) for x in range(5)])
    plr = benchmark(pl.resample, 0.5)
    assert pl.get_total_distance() == pytest.approx(plr.get_total_distance())
    assert np.all(plr.get_distances()[1:] - plr.get_distances()[:-1] == pytest.approx(0.5, rel=0.1))


def test_polyline_resample_return_indices():
    pl = Polyline([Point(x) for x in range(3)])
    plr, indices = pl.resample(0.5, return_indices=True)
    assert len(plr) == indices.size
    assert np.all(indices[1:] - indices[:-1] == pytest.approx(0.5))
