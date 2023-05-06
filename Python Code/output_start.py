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
    Returns the beginning index where a loop evaluating output values should
    begin

    Parameters
    ----------
    discip : dictionary
        Contains various key-value pairs associated with the current details of
        the particular discipline
    key : string
        The particular key of the discipline to assess for its size

    Returns
    -------
    start : integer
        Index where further output value assessment should begin
    """
    
    # Check if discipline values of key are empty
    if len(discip[key]) == 0:
        
        # Start assessment at the first index
        start = 0
        
    # Perform following command if values of key are not empty
    else:
        
        # Start assessment at one index beyond the amound of rows present
        start = np.shape(discip[key])[0]
    
    # Return the starting index
    return start