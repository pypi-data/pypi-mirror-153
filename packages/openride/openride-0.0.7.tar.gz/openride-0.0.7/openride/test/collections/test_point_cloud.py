from openride import PointCloud
from openride.core.point import Point
from openride.core.rotation import Rotation
from openride.core.transform import Transform

import numpy as np
import pytest



def test_init_empty():
    pc = PointCloud()
    assert len(pc) == 0


def test_init():
    pc = PointCloud([Point(), Point()])
    assert len(pc) == 2


def test_append():
    pc = PointCloud([Point(), Point()])
    pc.append(Point())
    assert len(pc) == 3


def test_extend():
    pc = PointCloud([Point(), Point()])
    pc2 = PointCloud([Point(), Point()])
    pc.extend(pc2)
    assert len(pc) == 4


def test_pop():
    pc = PointCloud([Point(), Point(1), Point()])
    point = pc.pop(1)
    assert point.x == 1
    assert len(pc) == 2


def test_repr():
    pc = PointCloud([Point(), Point()])
    assert isinstance(str(pc), str)


def test_getitem():
    pc = PointCloud([Point(), Point(1)])
    point = pc[1]
    assert point.x == 1


def test_transform():
    pc = PointCloud([Point(), Point()])
    pc = pc.transform(Transform(Point(1), Rotation(0,0,np.pi)))
    assert pytest.approx(pc[0].x) == -1


def test_get_point_cloud():
    pc = PointCloud([Point(), Point()])
    xyz = pc.get_point_cloud()
    assert xyz.shape == (2,3)
    assert np.all(xyz == 0.0)
    