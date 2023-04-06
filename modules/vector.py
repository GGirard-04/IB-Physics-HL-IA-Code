# Gavin Girard - April 2023

import math
from modules import util, stats
from typing import List

class Vector3D:
    def __init__(self, x: float, y: float, z: float):
        self.x, self.y, self.z = x, y, z
    
    def length(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

def cross_product(v1: Vector3D, v2: Vector3D) -> Vector3D:
    return Vector3D(
             (v1.y * v2.z) - (v1.z * v2.y),
        -1 * (v1.x * v2.z) + (v1.z * v2.x),
             (v1.x * v2.y) - (v1.y * v2.x)
    )

def dot_product(v1: Vector3D, v2: Vector3D) -> float:
    return (v1.x * v2.x) + (v1.y * v2.y) + (v1.z * v2.z)

class OrbitSlice3D:
    def __init__(self, vector1: Vector3D, vector2: Vector3D):
        self.vector1 = vector1
        self.vector2 = vector2
        self.traversed_area = self.get_traversed_area()
        self.traversed_angle = self.get_traversed_angle()
        self.longest_vector_length = self.get_longest_vector_length()

    def get_traversed_area(self) -> float:
        return 0.5 * cross_product(self.vector1, self.vector2).length()
    
    def get_traversed_angle(self) -> float:
        cos_theta = dot_product(self.vector1, self.vector2) / (self.vector1.length() * self.vector2.length())
        return math.acos(cos_theta)

    def get_longest_vector_length(self) -> float:
        return stats.get_stat_max([self.vector1.length(), self.vector2.length()])
    
    def get_calculated_slice_distance(self, average_area: float) -> float:
        return math.sqrt(2 * average_area / math.sin(self.traversed_angle))

def construct_slice_set(vector_set: List[Vector3D]) -> List[OrbitSlice3D]:
    vector_pairs = util.pair_vectors(vector_set)
    orbit_slices = []
    for vector_pair in vector_pairs:
        orbit_slices.append(OrbitSlice3D(*vector_pair))
    return orbit_slices