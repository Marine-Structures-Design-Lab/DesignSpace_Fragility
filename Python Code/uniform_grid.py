"""
SUMMARY:
Contains a function for creating an array of points to be used for
approximating the space remaining in each discipline's design space as space
reductions are made.  If more points are created, the designer will be able to
make more accurate predictions of the design space remaining after each
reduction; however, the convergent design simulation will take longer to
execute.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import numpy as np
import sympy as sp

"""
FUNCTIONS
"""
def uniformGrid(total_points, ndims, input_rules):
    """
    Description
    -----------
    Creates an array of evenly spaced points based on the total number of
    points the user desires and the discipline's number of dimensions

    Parameters
    ----------
    total_points : Integer
        An approximate total number of evenly spaced points the user desires
        for tracking the space remaining in the discipline's design space
    ndims : Integer
        The number of dimensions of which the design space consists
    input_rules : List
        List of sympy relationals defining the current set of all input rules

    Returns
    -------
    points : Numpy array
        An array of coordinates where each row represents a different point and
        each column represents the point's coordinate in a particular dimension
    num_points : Integer
        The actual total number of evenly spaced points that are created and
        stored in the points array
    index_list : List
        List of all the indices of evenly spaced points created
    """
    
    # Calculate the number of points in each dimension
    npoints_dim = int(round(total_points ** (1. / ndims)))
    
    # Create a list of 1D arrays representing the coordinates in each dimension
    coords = [np.linspace(0, 1, npoints_dim) for _ in range(ndims)]
    
    # Create a grid of coordinates
    grid = np.meshgrid(*coords, indexing='ij')
    
    # Reshape and stack to create a single array of points
    points = np.vstack([np.ravel(g) for g in grid]).T
    
    # Combine all constraints into a single expression
    constraints = sp.And(*input_rules)
    
    # Define sympy variables
    x = sp.symbols(f'x1:{ndims+1}')
    
    # Create a lambda function for evaluating the constraints
    constraints_func = sp.lambdify(x, constraints, modules='numpy')
    
    # Filter points to satisfy constraints
    valid_points = [point for point in points if constraints_func(*point)]
    
    # Calculate the number of points actually created
    num_points = len(valid_points)

    # Generate the 1D list of integers
    index_list = np.arange(num_points).tolist()

    # Return the array of points, actual number of points, and the index list
    return np.array(valid_points), num_points, index_list