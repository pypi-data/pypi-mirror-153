from openride import BoundingBox, Point, Polyline, Polygon, distance
from openride.core.numba.box_utils import vertices_inside_box

from multipledispatch import dispatch

import numpy as np



@dispatch(BoundingBox, Point)
def contains(obj1:BoundingBox, obj2:Point) -> bool:
    return len(vertices_inside_box(np.array([(obj2.x, obj2.y, obj2.z)], np.float64), obj1.get_vertices())) == 1


@dispatch(BoundingBox, BoundingBox)
def contains(obj1:BoundingBox, obj2:BoundingBox) -> bool:
    return len(vertices_inside_box(obj2.get_vertices(), obj1.get_vertices())) == 8


@dispatch(BoundingBox, Polyline)
def contains(obj1:BoundingBox, obj2:Polyline) -> bool:
    return len(vertices_inside_box(obj2.vertices, obj1.get_vertices())) == len(obj2)


@dispatch(BoundingBox, Polygon)
def contains(obj1:BoundingBox, obj2:Polygon) -> bool:
    return len(vertices_inside_box(obj2.vertices, obj1.get_vertices())) == obj2.vertices.shape[0]
    

@dispatch(Polyline, Point)
def contains(obj1:Polyline, obj2:Point) -> bool:
    return distance(obj1, obj2) == 0.0


@dispatch(Polyline, Polyline)
def contains(obj1:Polyline, obj2:Polyline) -> bool:
    return all([contains(obj1, point) for point in obj2])
