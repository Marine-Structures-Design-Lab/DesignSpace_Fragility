"""
SUMMARY:
Reads Gradient_Factor results from the HDF5 files and converts them back into 
usable data types for post-processing.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import h5py
import glob
import os

"""
FUNCTION
"""
def loadGradientFactor(directory_path):
    """
    Description
    -----------
    Loads gradient factor data from all HDF5 files in a directory and
    reconstructs the original data structure.

    Parameters
    ----------
    directory_path: String
        Path to the directory containing HDF5 files

    Returns
    -------
    gradient_factor_data: Dictionary
        The reconstructed data structure
    """
    
    # Initialize an empty dictionary for gradient factor data
    gradient_factor_data = {}
    
    # Create a list of file paths for each gradient factor data file
    hdf5_files = glob.glob(os.path.join(directory_path, 
                                        "gradient_factor_*.hdf5"))
    
    # Loop through each file path
    for hdf5_file_path in hdf5_files:
        
        # Extract run number from file name
        run_number = hdf5_file_path.split('_')[-1].split('.')[0]
        
        # Construct name for key
        key_name = f"Run_{run_number}"
        
        # Initialize an empty list to store data points
        data_points = []
        
        # Open HDF5 file in read mode
        with h5py.File(hdf5_file_path, 'r') as hdf_file:
            
            # Loop through each top-level group (data points) in the file
            for data_point_name in hdf_file:
                
                # Access the group corresponding to the current data point
                data_point_group = hdf_file[data_point_name]
                
                # Extract iteration number, gradient factor, and threshold
                data_point_dict = {
                    'iter': data_point_group.attrs['iter'],
                    'gradient_factor': \
                        float(data_point_group['gradient_factor'][()]),
                    'Threshold_value': \
                        float(data_point_group['Threshold_value'][()])
                }
                
                # Append constructed dictionary to the list of data points
                data_points.append(data_point_dict)
        
        # Organize data by run number
        gradient_factor_data[key_name] = data_points
    
    # Return the reconstructed data structure
    return gradient_factor_data

"""
SCRIPT
"""
# Use '.' for current directory or specify a path
directory_path = '.'

# Store data in Test Case variable
Gradient_Factor_5 = loadGradientFactor(directory_path)
