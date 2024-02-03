# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 10:06:44 2024

@author: joeyvan
"""

import h5py
import numpy as np

def load_space_remaining_from_hdf5(hdf5_file_path):
    """
    Load the space remaining data from an HDF5 file and reconstruct the original
    data structure: a list of lists of dictionaries with 'iter' and 'space_remaining'.
    
    Parameters:
    - hdf5_file_path: str, path to the HDF5 file.
    
    Returns:
    - space_remaining_data: The reconstructed data structure.
    """
    space_remaining_data = []

    with h5py.File(hdf5_file_path, 'r') as hdf_file:
        # Iterate over disciplines in the HDF5 file
        for discipline_group_name in hdf_file:
            discipline_data = []
            discipline_group = hdf_file[discipline_group_name]
            
            # Iterate over data points within a discipline
            for data_point_name in discipline_group:
                data_point_group = discipline_group[data_point_name]
                
                # Reconstruct the dictionary for this data point
                data_point_dict = {
                    'iter': data_point_group.attrs['iter'],  # Retrieve 'iter' from attributes
                    'space_remaining': data_point_group['space_remaining'][:]  # Retrieve numpy array
                }
                
                # Add this dictionary to the discipline data list
                discipline_data.append(data_point_dict)
            
            # Add the reconstructed discipline data to the main list
            space_remaining_data.append(discipline_data)
    
    return space_remaining_data

# Example usage:
hdf5_file_path = 'space_remaining_20240203100353_26768.hdf5'
loaded_data = load_space_remaining_from_hdf5(hdf5_file_path)
