"""
SUMMARY:
Contains functions that will help a designer dictate when any forced reductions
need to make depending on the amount of each discipline's design space that has
been eliminated thus far compared to the time remaining in the design problem.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import numpy as np
import matplotlib.pyplot as plt

"""
FUNCTIONS
"""
def calcExponential(x, p):
    """
    Description
    -----------
    Ensures parameters are within their required ranges and calculates the
    exponential function value for the given time elapsed (x-value)

    Parameters
    ----------
    x : Float
        The normalized time that has elapsed so far in the design problem
    p : Numpy vector
        Contains four user-defined parameters used in the exponential function
        defintion

    Returns
    -------
    exp : Float
        The normalized minimum amount of design space to be reduced based on
        the user-defined parameters and time elapsed
    """
    
    # Define necessary parameter ranges
    assert 0 <= p[0] < p[2] <= 1, (
        "Parameter 0 must be between 0 and Parameter 2, "
        "and Parameter 2 must be less than or equal to 1."
    )
    assert 0 <= p[3] <= 1, (
        "Parameter 3 must be between 0 and 1."
    )
    
    # Calculate the exponential function values for the provided x-value
    exp = p[3] * (np.exp(p[1] * (x-p[0]))-1) / (np.exp(p[1] * (p[2]-p[0]))-1)
    
    # Return the exponential function value
    return exp


def plotExponential(p):
    """
    Description
    -----------
    Create a 2D-plot to allow the user to visualize how their chosen parameters
    will lead to any forced reductions
    
    Parameters
    ----------
    p : Numpy vector
        Contains four user-defined parameters used in the exponential function
        defintion

    Returns
    -------
    None
    """
    
    # Create x values and calculate corresponding y values with exponential
    x_values = np.linspace(p[0], p[2], num=1000)
    y_values = calcExponential(x_values, p)
    
    # Specify characteristics of plot
    plt.figure(figsize=(8, 6))  # Initialize figure
    plt.plot(x_values, y_values)  # Plot x and y values
    plt.xlim((0,1))  # Set x-axis limits
    plt.ylim((0,1))  # Set y-axis limits
    plt.title("Discipline Space Reduction Pace", fontsize=16)  # Create title
    plt.xlabel("Fraction of Design Time Spent Exploring",\
               fontsize=14)  # Create x-axis label
    plt.ylabel("Minimum Fraction of Design Space to be Reduced",\
               fontsize=12)  # Create y-axis label
    plt.xticks(fontsize=12)  # Specify size of x-axis tick marks
    plt.yticks(fontsize=12)  # Specify size of y-axis tick marks
    plt.grid(True)  # Show grid lines
    plt.show()  # Show the plot
    
    # Nothing to return
    return