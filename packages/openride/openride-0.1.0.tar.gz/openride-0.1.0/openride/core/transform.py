from openride.core.point import Point
from openride.core.rotation import Rotation

from dataclasses import dataclass

import numpy as np



@dataclass
class Transform:
    
    translation: Point = Point(0,0,0)
    rotation: Rotation = Rotation(0,0,0)


    def __post_init__(self):
        self._cached_matrix = None
        self._cached_inverse_matrix = None


    def get_matrix(self) -> np.ndarray:
        if self._cached_matrix is None:
            self._cached_matrix = np.eye(4)
            self._cached_matrix[:3,:3] = self.rotation.get_matrix()
            self._cached_matrix[:3,3] = [self.translation.x, self.translation.y, self.translation.z]
        return self._cached_matrix


    def get_inverse_matrix(self) -> np.ndarray:
        if self._cached_inverse_matrix is None:
            tf = self.get_matrix()
            self._cached_inverse_matrix = np.zeros_like(tf)
            self._cached_inverse_matrix[:3,:3] = tf[:3,:3].T 
            self._cached_inverse_matrix[:3,3] = np.dot(-tf[:3,:3].T, tf[:3, 3])
            self._cached_inverse_matrix[3,3] = 1
        return self._cached_inverse_matrix


    def inverse(self) -> 'Transform':
        return Transform.from_matrix(self.get_inverse_matrix())


    @classmethod
    def from_matrix(cls, matrix:np.ndarray) -> 'Transform':
        tf = cls(Point(*matrix[:3,3]), Rotation.from_matrix(matrix))
        tf._cached_matrix = matrix
        return tf
