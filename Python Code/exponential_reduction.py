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
import matplotlib.pyplot as plt

"""
FUNCTIONS
"""
def calcExponential(x, p):
    
    # Define necessary parameter ranges
    assert 0 <= p[0] < p[2] <= 1, (
        "Parameter 0 must be between 0 and Parameter 2, "
        "and Parameter 2 must be less than or equal to 1."
    )
    assert 0 <= p[3] <= 1, (
        "Parameter 3 must be between 0 and 1."
    )
    
    # Return the exponential function value for the provided x-value
    return p[3] * (np.exp(p[1] * (x-p[0]))-1) / (np.exp(p[1] * (p[2]-p[0]))-1)


def plotExponential(p):
    
    # Create x values and calculate corresponding y values with equation
    x_values = np.linspace(p[0], p[2], num=1000)
    y_values = calcExponential(x_values, p)
    
    # Specify characteristics of and show the plot
    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values)
    plt.xlim((0,1))  # Set x-axis limits
    plt.ylim((0,1))  # Set y-axis limits
    plt.title("Discipline Space Reduction Pace", fontsize=16)
    plt.xlabel("Fraction of Design Time Spent Exploring", fontsize=14)
    plt.ylabel("Minimum Fraction of Design Space to be Reduced", fontsize=12)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True)
    plt.show()
    
    # Nothing to return
    return