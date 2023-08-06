from openride.core.numba.box_utils import vertices_inside_box

import numpy as np
import numba



@numba.njit(cache=True)
def distance_between_points_3d(x1, y1, z1, x2, y2, z2) -> float:
    return ((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)**0.5


@numba.njit(cache=True)
def distance_between_box_and_point_3d(box_vertices, px, py, pz) -> float:
    point = np.array((px, py, pz))
    if len(vertices_inside_box(np.reshape(point, (1,3)), box_vertices)) > 0: return 0.0
    box_triangle_indices = [[0,1,2], [1,2,3], [0,2,4], [0,4,6], [2,3,4], [3,4,5], [0,1,6], [1,6,7], [4,5,6], [5,6,7], [1,3,5], [1,5,7]]
    distances = np.zeros(12)
    for i, triangle in enumerate(box_triangle_indices):
        _triangle = np.vstack((box_vertices[triangle[0]], box_vertices[triangle[1]], box_vertices[triangle[2]]))
        distances[i] = distance_triangle_point_3d(_triangle, px, py, pz)
    return np.min(distances)


@numba.njit(cache=True)
def distance_between_line_and_point_3d(vertices:np.ndarray, x:float, y:float, z:float) -> float:
    distances = np.zeros(vertices.shape[0]-1)
    p = np.array((x, y, z))
    for i in range(vertices.shape[0]-1):
        distances[i] = point_segment_distance_3d(p, vertices[i], vertices[i+1])
    return np.min(distances)


@numba.njit(cache=True)
def distance_between_lines_3d(vertices1:np.ndarray, vertices2:np.ndarray) -> float:
    distances = np.zeros((vertices1.shape[0]-1, vertices2.shape[0]-1))
    for i in range(vertices1.shape[0]-1):
        for j in range(vertices2.shape[0]-1):
            distances[i,j] = segments_distance_3d(vertices1[i], vertices1[i+1], vertices2[j], vertices2[j+1])
    return np.min(distances)


@numba.njit(cache=True)
def distance_between_line_and_box_3d(line_vertices:np.ndarray, box_vertices:np.ndarray) -> float:
    if len(vertices_inside_box(line_vertices, box_vertices)) > 0: return 0.0
    distances = np.zeros((12, line_vertices.shape[0]-1))
    faces = [[0,1,2], [1,2,3], [0,2,4], [0,4,6], [2,3,4], [3,4,5], [0,1,6], [1,6,7], [4,5,6], [5,6,7], [1,3,5], [1,5,7]]
    for i, face in enumerate(faces):
        triangle = np.vstack((box_vertices[face[0]], box_vertices[face[1]], box_vertices[face[2]]))
        for j in range(line_vertices.shape[0]-1):
            p1 = line_vertices[j]
            direction = line_vertices[j+1] - p1
            distances[i,j] = segment_triangle_distance(p1, direction, triangle)
            if distances[i,j] == 0.0: return 0.0
    return np.min(distances)


@numba.njit(cache=True)
def distance_between_boxes_3d(vertices1:np.ndarray, vertices2:np.ndarray) -> float:
    if len(vertices_inside_box(vertices1, vertices2)) > 0: return 0.0
    if len(vertices_inside_box(vertices2, vertices1)) > 0: return 0.0
    distances = []
    box_face_indices = [[0,1,2], [1,2,3], [0,2,4], [0,4,6], [2,3,4], [3,4,5], [0,1,6], [1,6,7], [4,5,6], [5,6,7], [1,3,5], [1,5,7]]
    for face in box_face_indices:
        triangle = np.vstack((vertices1[face[0]], vertices1[face[1]], vertices1[face[2]]))
        for p in vertices2:
            distances.append(distance_triangle_point_3d(triangle, p[0], p[1], p[2]))
    for face in box_face_indices:
        triangle = np.vstack((vertices2[face[0]], vertices2[face[1]], vertices2[face[2]]))
        for p in vertices1:
            distances.append(distance_triangle_point_3d(triangle, p[0], p[1], p[2]))

    box_segment_indices = [6,7, 7,1, 1,0, 0,6,       4,5, 5,3, 3,2, 2,4,      6,4, 7,5, 0,2, 1,3]
    for i in range(0, len(box_segment_indices)-1, 2):
        v1 = vertices1[box_segment_indices[i]]
        v2 = vertices1[box_segment_indices[i+1]]
        for j in range(0, len(box_segment_indices)-1, 2):
            v3 = vertices2[box_segment_indices[j]]
            v4 = vertices2[box_segment_indices[j+1]]
            distances.append(segments_distance_3d(v1, v2, v3, v4))

    return min(distances)


@numba.njit(cache=True)
def point_segment_distance_3d(p, a, b):

    # normalized tangent vector
    diff = b - a
    norm = (diff[0]**2 + diff[1]**2 + diff[2]**2)**.5
    d = np.divide(diff, norm)

    # signed parallel distance components
    s = np.dot(a - p, d)
    t = np.dot(p - b, d)

    # clamped parallel distance
    h = max([s, t, 0.0])

    # perpendicular distance component
    c = np.cross(p - a, d)

    return np.hypot(h, np.linalg.norm(c))


@numba.njit(cache=True)
def segments_distance_3d(p11, p12, p21, p22):

    # Calculate denomitator
    A = p12 - p11
    B = p22 - p21
    magA = np.linalg.norm(A)
    magB = np.linalg.norm(B)
    
    _A = A / magA
    _B = B / magB
    
    cross = np.cross(_A, _B)
    denom = np.linalg.norm(cross)**2
    
    # If lines are parallel (denom=0) test if lines overlap.
    # If they don't overlap then there is a closest point solution.
    # If they do overlap, there are infinite closest positions, but there is a closest distance
    if not denom:
        d0 = np.dot(_A,(p21-p11))
        d1 = np.dot(_A,(p22-p11))
        
        # Is segment B before A?
        if d0 <= 0 >= d1:
            if np.absolute(d0) < np.absolute(d1):
                return np.linalg.norm(p11-p21)
            return np.linalg.norm(p11-p22)
            
        # Is segment B after A?
        elif d0 >= magA <= d1:
            if np.absolute(d0) < np.absolute(d1):
                return np.linalg.norm(p12-p21)
            return np.linalg.norm(p12-p22)
                
        # Segments overlap, return distance between parallel segments
        return np.linalg.norm(((d0*_A)+p11)-p21)
        

    # Lines criss-cross: Calculate the projected closest points
    t = (p21 - p11)
    detA = np.linalg.det(np.vstack((t, _B, cross)))
    detB = np.linalg.det(np.vstack((t, _A, cross)))

    t0 = detA/denom
    t1 = detB/denom

    pA = p11 + (_A * t0) # Projected closest point on segment A
    pB = p21 + (_B * t1) # Projected closest point on segment B

    # Clamp projections
    if t0 < 0: pA = p11
    elif t0 > magA: pA = p12
    
    if t1 < 0: pB = p21
    elif t1 > magB: pB = p22
        
    # Clamp projection A
    if (t0 < 0) or (t0 > magA):
        dot = np.dot(_B,(pA-p21))
        if dot < 0: dot = 0
        elif dot > magB: dot = magB
        pB = p21 + (_B * dot)

    # Clamp projection B
    if (t1 < 0) or (t1 > magB):
        dot = np.dot(_A,(pB-p11))
        if dot < 0: dot = 0
        elif dot > magA: dot = magA
        pA = p11 + (_A * dot)

    return np.linalg.norm(pA-pB)


@numba.njit(cache=True)
def distance_triangle_point_3d(triangle, px, py, pz):
    """https://gist.github.com/joshuashaffer/99d58e4ccbd37ca5d96e"""
    
    B = triangle[0, :]
    E0 = triangle[1, :] - B
    E1 = triangle[2, :] - B
    D = B - np.array((px, py, pz))
    a = np.dot(E0, E0)
    b = np.dot(E0, E1)
    c = np.dot(E1, E1)
    d = np.dot(E0, D)
    e = np.dot(E1, D)
    f = np.dot(D, D)

    det = a * c - b * b
    s = b * e - c * d
    t = b * d - a * e

    # Terible tree of conditionals to determine in which region of the diagram
    # shown above the projection of the point into the triangle-plane lies.
    if (s + t) <= det:
        if s < 0.0:
            if t < 0.0:
                # region4
                if d < 0:
                    t = 0.0
                    if -d >= a:
                        s = 1.0
                        sqrdistance = a + 2.0 * d + f
                    else:
                        s = -d / a
                        sqrdistance = d * s + f
                else:
                    s = 0.0
                    if e >= 0.0:
                        t = 0.0
                        sqrdistance = f
                    else:
                        if -e >= c:
                            t = 1.0
                            sqrdistance = c + 2.0 * e + f
                        else:
                            t = -e / c
                            sqrdistance = e * t + f

                            # of region 4
            else:
                # region 3
                s = 0
                if e >= 0:
                    t = 0
                    sqrdistance = f
                else:
                    if -e >= c:
                        t = 1
                        sqrdistance = c + 2.0 * e + f
                    else:
                        t = -e / c
                        sqrdistance = e * t + f
                        # of region 3
        else:
            if t < 0:
                # region 5
                t = 0
                if d >= 0:
                    s = 0
                    sqrdistance = f
                else:
                    if -d >= a:
                        s = 1
                        sqrdistance = a + 2.0 * d + f;  # GF 20101013 fixed typo d*s ->2*d
                    else:
                        s = -d / a
                        sqrdistance = d * s + f
            else:
                # region 0
                invDet = 1.0 / det
                s = s * invDet
                t = t * invDet
                sqrdistance = s * (a * s + b * t + 2.0 * d) + t * (b * s + c * t + 2.0 * e) + f
    else:
        if s < 0.0:
            # region 2
            tmp0 = b + d
            tmp1 = c + e
            if tmp1 > tmp0:  # minimum on edge s+t=1
                numer = tmp1 - tmp0
                denom = a - 2.0 * b + c
                if numer >= denom:
                    s = 1.0
                    t = 0.0
                    sqrdistance = a + 2.0 * d + f;  # GF 20101014 fixed typo 2*b -> 2*d
                else:
                    s = numer / denom
                    t = 1 - s
                    sqrdistance = s * (a * s + b * t + 2 * d) + t * (b * s + c * t + 2 * e) + f

            else:  # minimum on edge s=0
                s = 0.0
                if tmp1 <= 0.0:
                    t = 1
                    sqrdistance = c + 2.0 * e + f
                else:
                    if e >= 0.0:
                        t = 0.0
                        sqrdistance = f
                    else:
                        t = -e / c
                        sqrdistance = e * t + f
                        # of region 2
        else:
            if t < 0.0:
                # region6
                tmp0 = b + e
                tmp1 = a + d
                if tmp1 > tmp0:
                    numer = tmp1 - tmp0
                    denom = a - 2.0 * b + c
                    if numer >= denom:
                        t = 1.0
                        s = 0
                        sqrdistance = c + 2.0 * e + f
                    else:
                        t = numer / denom
                        s = 1 - t
                        sqrdistance = s * (a * s + b * t + 2.0 * d) + t * (b * s + c * t + 2.0 * e) + f

                else:
                    t = 0.0
                    if tmp1 <= 0.0:
                        s = 1
                        sqrdistance = a + 2.0 * d + f
                    else:
                        if d >= 0.0:
                            s = 0.0
                            sqrdistance = f
                        else:
                            s = -d / a
                            sqrdistance = d * s + f
            else:
                # region 1
                numer = c + e - b - d
                if numer <= 0:
                    s = 0.0
                    t = 1.0
                    sqrdistance = c + 2.0 * e + f
                else:
                    denom = a - 2.0 * b + c
                    if numer >= denom:
                        s = 1.0
                        t = 0.0
                        sqrdistance = a + 2.0 * d + f
                    else:
                        s = numer / denom
                        t = 1 - s
                        sqrdistance = s * (a * s + b * t + 2.0 * d) + t * (b * s + c * t + 2.0 * e) + f

    # account for numerical round-off error
    if sqrdistance < 0:
        sqrdistance = 0

    dist = sqrdistance ** 0.5

    return dist


@numba.njit(cache=True)
def ray_triangle_intersect(ray_origin, ray_direction, triangle):
    """https://github.com/johnnovak/raytriangle-test/blob/master/python/perftest.py"""
    v0, v1, v2 = triangle[0], triangle[1], triangle[2]
    v0v1 = v1 - v0
    v0v2 = v2 - v0
    pvec = np.cross(ray_direction, v0v2)
    det = np.dot(v0v1, pvec)
    if det < 0.000001: return False
    invDet = 1.0 / det
    tvec = ray_origin - v0
    u = np.dot(tvec, pvec) * invDet
    if u < 0 or u > 1: return False
    qvec = np.cross(tvec, v0v1)
    v = np.dot(ray_direction, qvec) * invDet
    if v < 0 or u + v > 1: return False
    if np.dot(v0v2, qvec) * invDet < 0.000001: return False
    return True


@numba.njit(cache=True)
def segment_triangle_intersects(ray_origin, ray_direction, triangle):
    intersects1 = ray_triangle_intersect(ray_origin, ray_direction, triangle)
    intersects2 = ray_triangle_intersect((ray_origin+ray_direction), ray_direction*-1, triangle[::-1])
    return intersects1 and intersects2


@numba.njit(cache=True)
def segment_triangle_distance(ray_origin, ray_direction, triangle):
    if segment_triangle_intersects(ray_origin, ray_direction, triangle): return 0.0
    p1 = ray_origin
    p2 = ray_origin + ray_direction
    distances = []
    for i,j in ((0,1),(1,2),(2,0)):
        distances.append(segments_distance_3d(p1, p2, triangle[i], triangle[j]))
    return min(distances)
