from openride import BoundingBoxCollection, BoundingBox
from openride.core.point import Point
from openride.core.rotation import Rotation
from openride.core.size import Size
from openride.core.transform import Transform

import numpy as np
import pytest



def test_init_empty():
    bc = BoundingBoxCollection()
    assert len(bc) == 0


def test_init():
    bc = BoundingBoxCollection([BoundingBox(), BoundingBox()])
    assert len(bc) == 2


def test_append():
    bc = BoundingBoxCollection([BoundingBox(), BoundingBox()])
    bc.append(BoundingBox())
    assert len(bc) == 3


def test_extend():
    bc = BoundingBoxCollection([BoundingBox(), BoundingBox()])
    bc2 = BoundingBoxCollection([BoundingBox(), BoundingBox()])
    bc.extend(bc2)
    assert len(bc) == 4


def test_pop():
    bc = BoundingBoxCollection([BoundingBox(), BoundingBox(Point(1)), BoundingBox()])
    box = bc.pop(1)
    assert box.position.x == 1
    assert len(bc) == 2


def test_repr():
    bc = BoundingBoxCollection([BoundingBox(), BoundingBox()])
    assert isinstance(str(bc), str)


def test_getitem():
    bc = BoundingBoxCollection([BoundingBox(), BoundingBox(Point(1), Rotation(0,2), Size(1,1,3)), BoundingBox()])
    box = bc[1]
    assert box.position.x == 1
    assert box.rotation.pitch == 2
    assert box.size.z == 3


def test_transform():
    bc = BoundingBoxCollection([BoundingBox(), BoundingBox()])
    bc = bc.transform(Transform(Point(1), Rotation(0,0,np.pi)))
    assert pytest.approx(bc[0].position.x) == -1
    assert pytest.approx(bc[1].position.x) == -1
    assert pytest.approx(bc[0].rotation.yaw) == np.pi


def test_get_distances():
    bc = BoundingBoxCollection([BoundingBox(Point(x,x,x)) for x in range(3)])
    assert np.all(bc.get_distances() == np.array([0, 3**0.5, 12**0.5]))


def test_filter():
    bc = BoundingBoxCollection([BoundingBox(Point(x)) for x in range(3)])
    bcf = bc.filter([0,2])
    assert bcf[0].position.x == 0 and bcf[1].position.x == 2


def test_filter_distance_min():
    bc = BoundingBoxCollection([BoundingBox(Point(x,x,x)) for x in range(3)])
    bcf = bc.filter_distance(min_distance=2.0)
    assert bcf.get_distances() == np.array([12**0.5])


def test_filter_distance_max():
    bc = BoundingBoxCollection([BoundingBox(Point(x,x,x)) for x in range(3)])
    bcf = bc.filter_distance(max_distance=1.0)
    assert bcf.get_distances() == np.array([0.0])
