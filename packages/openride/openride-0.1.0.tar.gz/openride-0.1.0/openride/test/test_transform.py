from openride.core.point import Point
from openride.core.rotation import Rotation
from openride.core.transform import Transform
from openride.test import get_pytest_benchmark

import numpy as np
import pytest



pytest_benchmark = get_pytest_benchmark(group="core.transform")


def test_transform_init():
    tf = Transform()
    assert tf.translation == Point()
    assert tf.rotation == Rotation()


@pytest_benchmark
def test_transform_get_matrix(benchmark):
    tf = Transform()
    matrix = benchmark(tf.get_matrix)
    assert np.all(matrix == np.eye(4))


def test_transform_matrix_translation():
    tf = Transform(translation=Point(1,2,3))
    matrix = tf.get_matrix()
    assert matrix[0,3] == 1
    assert matrix[1,3] == 2
    assert matrix[2,3] == 3


@pytest_benchmark
def test_transform_get_inverse_matrix(benchmark):
    tf = Transform()
    matrix = benchmark(tf.get_inverse_matrix)
    assert np.all(matrix == np.eye(4))


def test_transform_inverse_matrix_translation():
    tf = Transform(translation=Point(1,2,3))
    matrix = tf.get_inverse_matrix()
    assert matrix[0,3] == -1
    assert matrix[1,3] == -2
    assert matrix[2,3] == -3


def test_transform_matrix_inverse_reciprocal():
    tf1 = Transform(
        translation=Point(1,2,3), 
        rotation=Rotation(*np.random.random(3)),
    )
    tf2 = Transform.from_matrix(tf1.get_matrix())
    assert np.all(pytest.approx(tf1.get_matrix()) == tf2.get_matrix())
    

@pytest_benchmark
def test_transform_inverse(benchmark):
    tf = Transform(
        translation=Point(1,2,3), 
        rotation=Rotation(*np.random.random(3)),
    )
    tf_inf = benchmark(tf.inverse)
    p1 = Point(8,3,4)
    p2 = p1.transform(tf).transform(tf_inf)
    assert pytest.approx(p1.x) == p2.x
    assert pytest.approx(p1.y) == p2.y
    assert pytest.approx(p1.z) == p2.z
    