"""
SUMMARY:
Creates a new key containing an empty list if the key does not yet reside in
the existing dictionary.

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
    Checks if a key is in the supplied dictionary and puts it there if not
    
    Parameters
    ----------
    key : string
        The specific key being looked for and/or being added to the dictionary
    Dict : dictionary
        The dictionary being assessed
    
    Returns
    -------
    Dict : dictionary
        The original dictionary or an updated dictionary containing the new key
    """
    
    if key not in Dict:
        Dict[key] = []
    
    return Dict

def createDict(key,Dict):
    
    if key not in Dict:
        Dict[key] = {}
    
    return Dict

def createNumpy(key,Dict):
    
    if key not in Dict:
        Dict[key] = np.array([])
    
    return Dict
