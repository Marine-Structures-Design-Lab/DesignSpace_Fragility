# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 11:43:51 2024

@author: joeyvan
"""
import numpy as np




def convertNumpy(obj):
    """
    Recursively converts numpy arrays to lists within a given object.
    Works with nested structures like dictionaries and lists.
    """
    if isinstance(obj, np.ndarray):
        return obj.tolist()  # Convert ndarray to list
    elif isinstance(obj, list):
        return [convertNumpy(item) for item in obj]  # Recurse into lists
    elif isinstance(obj, dict):
        return {key: convertNumpy(value) for key, value in obj.items()}
    else:
        return obj
