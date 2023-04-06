# Gavin Girard - April 2023

from modules.vector import Vector3D
from typing import List, Tuple

def pair_vectors(vector_set: List[Vector3D]) -> List[Tuple[Vector3D, Vector3D]]:
    vector_pairs = []
    for index, vector in enumerate(vector_set):
        if index == len(vector_set) - 1:
            break
        vector_pairs.append((vector, vector_set[index + 1]))
    return vector_pairs

def generate_vector_set(file_content: str) -> List[Tuple]:
    vector_set = []
    for line in file_content.split("\n"):
        _, __, x, y, z = line[:-1].split(", ")
        vector_set.append(Vector3D(float(x), float(y), float(z)))
    return vector_set

def parse_jpl_content(in_file) -> str:
    return in_file.read().split("$$SOE\n")[1].split("\n$$EOE")[0]