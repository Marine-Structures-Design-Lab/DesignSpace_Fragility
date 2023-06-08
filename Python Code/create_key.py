"""
SUMMARY:
Various functions for creating a dictionary key if it does not already exist
and pairing the key with an empty list, dictionary, or numpy vector/array.

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
def createKey(key,Dict):
    """
    Description
    -----------
    Checks if a key is in the supplied dictionary and puts it there with an
    empty list as the value if not
    
    Parameters
    ----------
    key : String
        The specific key being looked for
    Dict : Dictionary
        The dictionary within which the key is being searched
    
    Returns
    -------
    Dict : Dictionary
        The original dictionary or an updated dictionary containing the new key
    """
    
    # Check if key is not already in the dictionary
    if key not in Dict:
        
        # Add the key with an empty list
        Dict[key] = []
    
    # Return the same dictionary with a potentially new key
    return Dict


def createDict(key,Dict):
    """
    Description
    -----------
    Checks if a key is in the supplied dictionary and puts it there with an
    empty dictionary as the value if not
    
    Parameters
    ----------
    key : String
        The specific key being looked for
    Dict : Dictionary
        The dictionary within which the key is being searched
    
    Returns
    -------
    Dict : Dictionary
        The original dictionary or an updated dictionary containing the new key
    """
    
    # Check if key is not already in the dictionary
    if key not in Dict:
        
        # Add the key with an empty dictionary
        Dict[key] = {}
    
    # Return the same dictionary with a potentially new key
    return Dict


def createNumpy(key,Dict):
    """
    Description
    -----------
    Checks if a key is in the supplied dictionary and puts it there with an
    empty numpy vector as the value if not
    
    Parameters
    ----------
    key : String
        The specific key being looked for
    Dict : Dictionary
        The dictionary within which the key is being searched
    
    Returns
    -------
    Dict : Dictionary
        The original dictionary or an updated dictionary containing the new key
    """
    
    # Check if key is not already in the dictionary
    if key not in Dict:
        
        # Add the key with an empty 1-D array
        Dict[key] = np.array([])
    
    # Return the same dictionary with a potentially new key
    return Dict


def createNumpy2(key,Dict,cols):
    """
    Description
    -----------
    Checks if a key is in the supplied dictionary and puts it there with an
    empty numpy array as the value if not

    Parameters
    ----------
    key : String
        The specific key being looked for
    Dict : Dictionary
        The dictionary within which the key is being searched
    cols : Integer
        The number of columns to initialize for the 2-D numpy array

    Returns
    -------
    Dict : Dictionary
        The original dictionary or an updated dictionary containing the new key
    """
    
    # Check if key is not already in the dictionary
    if key not in Dict:
        
        # Add the key with an empty 2-D array
        Dict[key] = np.empty((0,cols))
        
    # Return the same dictionary with a potentially new key
    return Dict
