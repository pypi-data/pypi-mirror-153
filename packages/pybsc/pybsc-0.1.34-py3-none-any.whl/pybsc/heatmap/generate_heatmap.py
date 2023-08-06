import numpy as np


def generate_gaussian_heatmap(shape, xy, sigma=1.0):
    """Return generated gaussian heatmap.

    Parameters
    ==========
    shape : tuple(int, int)
        width, height
    xy : tuple(int, int)
        x y position.
    sigma : float
        sigma
    """
    width, height = shape
    x, y = xy
    grid_x = np.tile(np.arange(width), (height, 1))
    grid_y = np.tile(np.arange(height), (width, 1)).transpose()
    grid_distance = (grid_x - x) ** 2 + (grid_y - y) ** 2
    gaussian_heatmap = np.exp(-0.5 * grid_distance / sigma**2)
    return gaussian_heatmap
