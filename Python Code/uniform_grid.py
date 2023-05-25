"""
SUMMARY:


CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import numpy as np

"""
FUNCTIONS
"""
def uniformGrid(total_points, ndims):
    
    # Calculate the number of points in each dimension
    npoints_dim = int(round(total_points ** (1. / ndims)))
    
    # Create a list of 1D arrays representing the coordinates in each dimension
    coords = [np.linspace(0, 1, npoints_dim) for _ in range(ndims)]
    
    # Create a grid of coordinates
    grid = np.meshgrid(*coords, indexing='ij')
    
    # Reshape and stack to create a single array of points
    points = np.vstack([np.ravel(g) for g in grid]).T

    # Return the array of points and actual number of points created
    return points, np.shape(points)[0]