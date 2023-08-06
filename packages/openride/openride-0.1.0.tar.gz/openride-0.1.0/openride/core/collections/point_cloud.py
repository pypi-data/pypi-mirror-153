from openride.core.collections.collection import Collection
from openride.core.point import Point
from openride.core.transform import Transform
from openride.core.numba.transforms import transform_vertices

from typing import List, Union

import numpy as np



class PointCloud(Collection):

    def __init__(self, points:Union[np.ndarray, List[Point]] = np.empty((0,3))):

        if isinstance(points, list):
            self._raw = np.zeros((len(points), 3))
            for i, point in enumerate(points):
                self._raw[i] = point.x, point.y, point.z

        else:
            self._raw = points


    def __len__(self) -> int:
        return self._raw.shape[0]


    def append(self, obj:Point):
        self._raw = np.vstack((self._raw, np.array((obj.x, obj.y, obj.z))))


    def extend(self, collection:'PointCloud'):
        self._raw = np.vstack((self._raw, collection._raw))


    def pop(self, index:int) -> Point:
        point = self[index]
        self._raw = np.delete(self._raw, index, axis=0)
        return point


    def __getitem__(self, index:int) -> Point:
        return Point(*self._raw[index])


    def get_point_cloud(self) -> np.ndarray:
        return self._raw


    def transform(self, transform:Transform) -> 'PointCloud':        
        tmp = np.copy(self._raw)
        tmp = transform_vertices(self._raw, transform.get_matrix())
        return PointCloud(tmp)
