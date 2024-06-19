"""
SUMMARY:
Reads Space_Remaining results from the HDF5 files produced by the SBD
simulation and converts them back into usable data types for post-processing.

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
def loadSpaceRemaining(directory_path):
    """
    Description
    -----------
    Loads space remaining data from all HDF5 files in a directory and
    reconstructs the original data structure.

    Parameters
    ----------
    directory_path: String
        Path to the directory containing HDF5 files

    Returns
    -------
    space_remaining_data: Dictionary
        The reconstructed data structure
    """
    
    # Initialize an empty dictionary for space remaining data
    space_remaining_data = {}
    
    # Create a list of file paths for each space remaining data file
    hdf5_files=glob.glob(os.path.join(directory_path,"space_remaining_*.hdf5"))
    
    # Loop through each file path
    for hdf5_file_path in hdf5_files:
        
        # Extract run number from file name
        run_number = hdf5_file_path.split('_')[-1].split('.')[0]
        
        # Construct name for key
        key_name = f"Run_{run_number}"
        
        # Initialize an empty list for each discipline's data
        discipline_data_list = []
        
        # Open HDF5 file in read mode
        with h5py.File(hdf5_file_path, 'r') as hdf_file:
            
            # Loop through each top-level group in file
            for discipline_group_name in hdf_file:
                
                # Create empty list for storing discipline's data points
                discipline_data = []
                
                # Retrieve group corresponding to the current discipline
                discipline_group = hdf_file[discipline_group_name]
                
                # Loop through each data point
                for data_point_name in discipline_group:
                    
                    # Access subgroup of current data point
                    data_point_group = discipline_group[data_point_name]
                    
                    # Extract iteration number and space remaining data
                    data_point_dict = {
                        'iter': data_point_group.attrs['iter'],
                        'space_remaining': data_point_group\
                            ['space_remaining'][:]
                    }
                    
                    # Append constructed dictionary to list of discipline data
                    discipline_data.append(data_point_dict)
                
                # Append all of the discipline's data to discipline list
                discipline_data_list.append(discipline_data)
        
        # Organize data by run number
        space_remaining_data[key_name] = discipline_data_list
    
    # Return the reconstructed data structure
    return space_remaining_data


"""
SCRIPT
"""
# Use '.' for current directory or specify a path
directory_path = '.'

# Store data in Test Case variable
Test_Case_2 = loadSpaceRemaining(directory_path)
