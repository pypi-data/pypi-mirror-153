from openride.core.collections.collection import Collection
from openride.core.bounding_box import BoundingBox
from openride.core.point import Point
from openride.core.rotation import Rotation
from openride.core.size import Size
from openride.core.transform import Transform
from openride.core.numba.transforms import transform_vertices

from typing import List

import numpy as np



class BoundingBoxCollection(Collection):

    def __init__(self, bounding_boxes:List[BoundingBox]=[]):

        self.dtype = np.dtype([('position', 'f8', (3)), ('rotation', 'f8', (3)), ('size', 'f8', (3))])
        self._raw:np.ndarray = np.empty(0, self.dtype)

        for bounding_box in bounding_boxes:
            self.append(bounding_box)


    def __len__(self) -> int:
        return self._raw.shape[0]


    def append(self, bbox:BoundingBox):
        array = np.array((
            (bbox.position.x, bbox.position.y, bbox.position.z),
            (bbox.rotation.roll, bbox.rotation.pitch, bbox.rotation.yaw),
            (bbox.size.x, bbox.size.y, bbox.size.z),
        ), self.dtype)
        self._raw = np.hstack((self._raw, array))


    def extend(self, box_collection:'BoundingBoxCollection'):
        self._raw = np.hstack((self._raw, box_collection._raw))


    def pop(self, index:int) -> BoundingBox:
        bbox = self[index]
        self._raw = np.delete(self._raw, index, axis=0)
        return bbox


    def __getitem__(self, index:int) -> BoundingBox:
        return BoundingBox(
            position = Point(*self._raw[index]['position']),
            rotation = Rotation(*self._raw[index]['rotation']),
            size = Size(*self._raw[index]['size']),
        )


    def transform(self, transform:Transform) -> 'BoundingBoxCollection':        
        tmp = np.copy(self._raw)
        tmp['position'] = transform_vertices(self._raw['position'], transform.get_matrix())
        tmp['rotation'][:,0] = (tmp['rotation'][:,0] + transform.rotation.roll) % (2*np.pi)
        tmp['rotation'][:,1] = (tmp['rotation'][:,1] + transform.rotation.pitch) % (2*np.pi)
        tmp['rotation'][:,2] = (tmp['rotation'][:,2] + transform.rotation.yaw) % (2*np.pi)
        transformed = BoundingBoxCollection()
        transformed._raw = tmp
        return transformed


    def get_distances(self) -> np.ndarray:
        return (self._raw['position'][:,0] ** 2 + self._raw['position'][:,1] ** 2 + self._raw['position'][:,2] ** 2) ** 0.5


    def filter(self, indices:List[int]) -> 'BoundingBoxCollection':
        filtered = BoundingBoxCollection()
        filtered._raw = self._raw[indices]
        return filtered

    
    def filter_distance(self, min_distance:float=0.0, max_distance:float=100.0) -> 'BoundingBoxCollection':
        distances = self.get_distances()
        return self.filter(np.where((distances >= min_distance) & (distances <= max_distance)))
