# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 11:52:01 2024

@author: joeyvan
"""
import json
import numpy as np

def load_and_convert(json_file_path):
    """
    Loads JSON data and converts it back into a list of lists of dictionaries,
    with NumPy arrays for 'space_remaining' values.
    
    :param json_file_path: Path to the JSON file.
    :return: The restored data structure.
    """
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    def restore_structure(obj):
        """
        Converts lists back to NumPy arrays for 'space_remaining' keys.
        """
        if isinstance(obj, list):
            # Process list of lists or list of dictionaries
            return [restore_structure(item) for item in obj]
        elif isinstance(obj, dict) and 'space_remaining' in obj:
            # Convert 'space_remaining' list back to a NumPy array
            obj['space_remaining'] = np.array(obj['space_remaining'])
        return obj
    
    # Apply the restoration to the loaded data
    restored_data = restore_structure(data)
    
    return restored_data



# Specify the name of your JSON file
file_name = "space_remaining_TC1_20240202173509.json"  # Replace YYYYMMDDHHMMSS with the actual timestamp

# Load the data using the function
loaded_data = load_and_convert(file_name)


# Now `loaded_data` will contain your data with lists converted back to NumPy arrays where you've deemed appropriate
