from openride.core.bounding_box import BoundingBox
from openride.core.point import Point
from openride.core.polyline import Polyline

from openride.core.numba.distances_3d import (
    distance_between_points_3d, distance_between_box_and_point_3d,
    distance_between_boxes_3d, distance_between_line_and_point_3d,
    distance_between_lines_3d, distance_between_line_and_box_3d,
)

from multipledispatch import dispatch



@dispatch(Point, Point)
def distance(obj1:Point, obj2:Point) -> float:
    return distance_between_points_3d(obj1.x, obj1.y, obj1.z, obj2.x, obj2.y, obj2.z)


@dispatch(Point, BoundingBox)
def distance(obj1:Point, obj2:BoundingBox) -> float:
    return distance_between_box_and_point_3d(obj2.get_vertices(), obj2.position.x, obj2.position.y, obj2.position.z, obj1.x, obj1.y, obj1.z)


@dispatch(Point, Polyline)
def distance(obj1:Point, obj2:Polyline) -> float:
    return distance_between_line_and_point_3d(obj2.vertices, obj1.x, obj1.y, obj1.z)


@dispatch(BoundingBox, Point)
def distance(obj1:BoundingBox, obj2:Point) -> float:
    return distance_between_box_and_point_3d(obj1.get_vertices(), obj1.position.x, obj1.position.y, obj1.position.z, obj2.x, obj2.y, obj2.z)


@dispatch(BoundingBox, BoundingBox)
def distance(obj1:BoundingBox, obj2:BoundingBox) -> float:
    return distance_between_boxes_3d(obj1.get_vertices(), obj2.get_vertices())


@dispatch(BoundingBox, Polyline)
def distance(obj1:BoundingBox, obj2:Polyline) -> float:
    return distance_between_line_and_box_3d(obj2.vertices, obj1.get_vertices())


@dispatch(Polyline, Point)
def distance(obj1:Polyline, obj2:Point) -> float:
    return distance_between_line_and_point_3d(obj1.vertices, obj2.x, obj2.y, obj2.z)


@dispatch(Polyline, BoundingBox)
def distance(obj1:Polyline, obj2:BoundingBox) -> float:
    return distance_between_line_and_box_3d(obj1.vertices, obj2.get_vertices())


@dispatch(Polyline, Polyline)
def distance(obj1:Polyline, obj2:Polyline) -> float:
    return distance_between_lines_3d(obj1.vertices, obj2.vertices)
