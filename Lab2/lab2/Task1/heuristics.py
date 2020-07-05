import numpy as np
from scipy.spatial.distance import minkowski
# Returns map with euclidean heuristic values.
def euclidean(_map, goal):
    heuristic_map = np.copy(_map)
    for ix, iy in np.ndindex(_map.shape):
        heuristic_map[ix, iy] = np.linalg.norm(np.array([ix, iy]) - goal)
    return heuristic_map



# Returns map with manhattan heuristic values.
def manhattan(_map, goal):
    heuristic_map = np.copy(_map)
    for ix, iy in np.ndindex(_map.shape):
        heuristic_map[ix, iy] = minkowski(np.array([ix, iy]), goal, p=1)
    return heuristic_map