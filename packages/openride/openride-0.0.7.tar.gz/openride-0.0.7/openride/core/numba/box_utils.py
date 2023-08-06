from openride.core.numba.transforms import transform_vertices

import numba
import numpy as np



@numba.njit(cache=True)
def bev_box_vertices(position_x, position_y, sixe_z, size_y, matrix) -> np.ndarray:
    vertices = np.array([[ sixe_z, size_y, 0]
                        ,[ sixe_z,-size_y, 0]
                        ,[-sixe_z,-size_y, 0]
                        ,[-sixe_z, size_y, 0]])
    matrix4x4 = np.eye(4)
    matrix4x4[:3,:3] = matrix
    vertices = transform_vertices(vertices, matrix4x4)
    vertices[:,0] += position_x
    vertices[:,1] += position_y
    return vertices[:,:2]


@numba.njit(cache=True)
def box_vertices(position_x, position_y, position_z, size_x, size_y, size_z, matrix) -> np.ndarray:
    vertices = np.array([[-size_x, size_y,-size_z]
                        ,[-size_x, size_y, size_z]
                        ,[ size_x, size_y,-size_z]
                        ,[ size_x, size_y, size_z]
                        ,[ size_x,-size_y,-size_z]
                        ,[ size_x,-size_y, size_z]
                        ,[-size_x,-size_y,-size_z]
                        ,[-size_x,-size_y, size_z]])
    matrix4x4 = np.eye(4)
    matrix4x4[:3,:3] = matrix
    vertices = transform_vertices(vertices, matrix4x4)
    vertices[:,0] += position_x
    vertices[:,1] += position_y
    vertices[:,2] += position_z
    return vertices


@numba.njit(cache=True)
def vertices_inside_box(vertices, box_vertices):
    """Returns indices of the vertices that are inside the box"""
    P = box_vertices
    u, v, w = P[1]-P[0], P[2]-P[0], P[6]-P[0]
    pu, pv, pw = np.dot(vertices, u), np.dot(vertices, v), np.dot(vertices, w)
    inside_box = np.where((pu <= np.dot(P[1], u)) & (pu >= np.dot(P[0], u))\
                        & (pv <= np.dot(P[2], v)) & (pv >= np.dot(P[0], v))\
                        & (pw <= np.dot(P[6], w)) & (pw >= np.dot(P[0], w))
                        )[0]
    return inside_box
    