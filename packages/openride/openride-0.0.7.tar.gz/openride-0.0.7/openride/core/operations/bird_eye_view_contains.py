from openride import Point, BoundingBox, Polyline, Polygon, bird_eye_view_distance
from openride.core.numba.polygon_utils import polygon_contains_point

from multipledispatch import dispatch



@dispatch(BoundingBox, Point)
def bird_eye_view_contains(obj1:BoundingBox, obj2:Point) -> bool:
    return bird_eye_view_distance(obj1, obj2) == 0.0


@dispatch(BoundingBox, BoundingBox)
def bird_eye_view_contains(obj1:BoundingBox, obj2:BoundingBox) -> bool:
    return all([bird_eye_view_contains(obj1, Point(*v)) for v in obj2.get_bird_eye_view_vertices()])


@dispatch(BoundingBox, Polyline)
def bird_eye_view_contains(obj1:BoundingBox, obj2:Polyline) -> bool:
    return all([bird_eye_view_contains(obj1, point) for point in obj2])


@dispatch(BoundingBox, Polygon)
def bird_eye_view_contains(obj1:BoundingBox, obj2:Polygon) -> bool:
    return all([bird_eye_view_contains(obj1, Point(*v)) for v in obj2.vertices[:,:2]])
    

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
    return all([polygon_contains_point(obj1.vertices, *p) for p in obj2.get_bird_eye_view_vertices()])


@dispatch(Polygon, Polyline)
def bird_eye_view_contains(obj1:Polygon, obj2:Polyline) -> bool:
    return all([polygon_contains_point(obj1.vertices, *p) for p in obj2.vertices[:,:2]])


@dispatch(Polygon, Polygon)
def bird_eye_view_contains(obj1:Polygon, obj2:Polygon) -> bool:
    return all([polygon_contains_point(obj1.vertices, *p) for p in obj2.vertices[:,:2]])
