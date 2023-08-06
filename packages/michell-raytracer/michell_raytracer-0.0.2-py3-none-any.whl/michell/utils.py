"""Different utils to for some small and regular calculations."""

import numpy as np

def vector_normalization(input_vector):
    """Returns unit vector with same direction as input vector had."""
    return input_vector / np.linalg.norm(input_vector)

def matrix_normalization(matrix_of_vectors):
    """Returns matrix (m, n, 3) of unit vectors with same directions
    as vectors of input matrix (m, n, 3) had."""
    return matrix_of_vectors / np.apply_over_axes(
        lambda  x, a: np.linalg.norm(x, axis=a),
        matrix_of_vectors,
        [2]
    )

def projections_on_plane(matrix_of_vectors, normal_vector):
    """Returns matrix of projections (m, n, 3) on plane defined by its normal vector
    getted from input matrix of vectors (m, n, 3)."""
    return matrix_of_vectors - (
        np.dot(matrix_of_vectors, normal_vector) /
        np.linalg.norm(normal_vector)**2
    )[:,:,np.newaxis,] * normal_vector

def count_steps(distances, step):
    """Returns matrix of steps' sizes (m, n, 1) to increase calculated rays."""
    normal_steps = (distances >= step) * 1 * step
    small_steps = ((distances < step) & (distances > 0)) * 1 * distances
    return normal_steps + small_steps

def count_progress(distances):
    """Returns percentage of zero elements in matrix of distances."""
    i, j, k = distances.shape
    total = i * j * k
    zeros = total - np.count_nonzero(np.round(distances, 5))
    result = (zeros / total) * 100
    return result
