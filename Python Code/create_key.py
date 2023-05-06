"""
SUMMARY:
Various functions for creating a dictionary key if it does not already exist
and pairing the key with an empty list, dictionary, or numpy vector.

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
    key : string
        The specific key being looked for
    Dict : dictionary
        The dictionary within which the key is being searched
    
    Returns
    -------
    Dict : dictionary
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
    key : string
        The specific key being looked for
    Dict : dictionary
        The dictionary within which the key is being searched
    
    Returns
    -------
    Dict : dictionary
        The original dictionary or an updated dictionary containing the new key
    """
    
    # Check if key is not already in the dictionary
    if key not in Dict:
        
        # Add the key with an empty list
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
    key : string
        The specific key being looked for
    Dict : dictionary
        The dictionary within which the key is being searched
    
    Returns
    -------
    Dict : dictionary
        The original dictionary or an updated dictionary containing the new key
    """
    
    # Check if key is not already in the dictionary
    if key not in Dict:
        
        # Add the key with an empty list
        Dict[key] = np.array([])
    
    # Return the same dictionary with a potentially new key
    return Dict
