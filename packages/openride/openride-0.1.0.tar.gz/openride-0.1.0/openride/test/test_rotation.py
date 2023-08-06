from openride import Rotation

import numpy as np
import pytest



def test_init():
    r = Rotation(1,2,3)
    assert r.roll == 1 and r.pitch == 2 and r.yaw == 3


def test_post_init():
    r = Rotation(1+2*np.pi,2-2*np.pi,3+10*np.pi)
    assert r.roll == 1 and r.pitch == 2 and r.yaw == 3


def test_rotation_matrix_identity():
    r = Rotation(0,0,0)
    assert np.all(r.get_matrix() == np.eye(3))


def test_rotation_from_identity():
    r = Rotation.from_matrix(np.eye(3))
    assert r.roll == 0 and r.pitch == 0 and r.yaw == 0


def test_rotation_euler_matrix_reciprocal():
    for _ in range(10):
        r1 = Rotation(*np.random.random(3)*2*np.pi)
        r2 = Rotation.from_matrix(r1.get_matrix())
        assert np.all(pytest.approx(r1.get_matrix()) == r2.get_matrix())


def test_add_rotations():
    r = Rotation(1,2,3) + Rotation(0.1, 0.2, 0.3)
    assert r.roll == 1.1
    assert r.pitch == 2.2
    assert r.yaw == 3.3


def test_sub_rotations():
    r = Rotation(1,2,3) - Rotation(0.1, 0.2, 0.3)
    assert r.roll == 0.9
    assert r.pitch == 1.8
    assert r.yaw == 2.7
