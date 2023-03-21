"""
SUMMARY:
Determine the index where output value calculations and/or output value
assessment should begin so as to not repeat for points that these actions were
already carried out for.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import numpy as np

"""
FUNCTION
"""
def outputStart(discip,key):
    """
    Description
    -----------
    Simple function for returning the beginning index where a loop evaluating
    output values should begin

    Parameters
    ----------
    discip : dictionary
        The complete dictionary of sympy inputs, sympy outputs, sympy
        expressions, execution time, and a partially filled list of tested
        output points that coincides with the input points
    key : string
        The particular key of the discipline to assess for its length

    Returns
    -------
    start : integer
        Index where further output value calculations/assessment should begin
    """
    
    if len(discip[key]) == 0:
        start = 0
    else:
        start = np.shape(discip[key])[0]
    
    return start