from openride import Point, BoundingBox, Polyline, Polygon, bird_eye_view_distance
from openride.core.numba.polygon_utils import polygon_contains_point, polygon_contains_all_vertices
from openride.core.numba.distances_bev import bev_distance_between_box_and_point

from multipledispatch import dispatch



@dispatch(BoundingBox, Point)
def bird_eye_view_contains(obj1:BoundingBox, obj2:Point) -> bool:
    return bev_distance_between_box_and_point(obj1.position.x, obj1.position.y, obj1.size.x, obj1.size.y, obj1.rotation.yaw, obj2.x, obj2.y) == 0.0


@dispatch(BoundingBox, BoundingBox)
def bird_eye_view_contains(obj1:BoundingBox, obj2:BoundingBox) -> bool:
    return polygon_contains_all_vertices(obj1.get_bird_eye_view_vertices(), obj2.get_bird_eye_view_vertices())


@dispatch(BoundingBox, Polyline)
def bird_eye_view_contains(obj1:BoundingBox, obj2:Polyline) -> bool:
    return polygon_contains_all_vertices(obj1.get_bird_eye_view_vertices(), obj2.vertices)


@dispatch(BoundingBox, Polygon)
def bird_eye_view_contains(obj1:BoundingBox, obj2:Polygon) -> bool:
    return polygon_contains_all_vertices(obj1.get_bird_eye_view_vertices(), obj2.vertices)
    

@dispatch(Polyline, Point)
def bird_eye_view_contains(obj1:Polyline, obj2:Point) -> bool:
    return bird_eye_view_distance(obj1, obj2) == 0.0


@dispatch(Polyline, Polyline)
def bird_eye_view_contains(obj1:Polyline, obj2:Polyline) -> bool:
    return all([bird_eye_view_contains(obj1, point) for point in obj2])


@dispatch(Polygon, Point)
def bird_eye_view_contains(obj1:Polygon, obj2:Point) -> bool:
    return polygon_contains_point(obj1.vertices, obj2.x, obj2.y)


@dispatch(Polygon, BoundingBox)
def bird_eye_view_contains(obj1:Polygon, obj2:BoundingBox) -> bool:
    return polygon_contains_all_vertices(obj1.vertices, obj2.get_bird_eye_view_vertices())


@dispatch(Polygon, Polyline)
def bird_eye_view_contains(obj1:Polygon, obj2:Polyline) -> bool:
    return polygon_contains_all_vertices(obj1.vertices, obj2.vertices)


@dispatch(Polygon, Polygon)
def bird_eye_view_contains(obj1:Polygon, obj2:Polygon) -> bool:
    return polygon_contains_all_vertices(obj1.vertices, obj2.vertices)
