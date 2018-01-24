from gameobjects.vector2 import Vector2
from gameobjects.vector3 import Vector3
from gameobjects.matrix44 import Matrix44
import math


def rotate_vector2(vec2, degrees):
    rotation_matrix = Matrix44.z_rotation(math.radians(degrees))
    transformed = rotation_matrix.transform_vec3(Vector3(vec2.x, vec2.y, 0))
    return Vector2(transformed.x, transformed.y)