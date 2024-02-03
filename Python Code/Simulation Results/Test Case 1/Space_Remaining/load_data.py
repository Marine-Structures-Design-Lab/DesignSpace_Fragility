import h5py
import glob
import os

def load_space_remaining_from_all_hdf5(directory_path):
    """
    Load space remaining data from all HDF5 files in a directory that match a specific pattern
    and reconstruct the original data structure: a dictionary of lists of dictionaries with 'iter'
    and 'space_remaining', where each key within is "Run_{number}" based on the file name.

    Parameters:
    - directory_path: str, path to the directory containing HDF5 files.

    Returns:
    - space_remaining_data: The reconstructed data structure.
    """
    space_remaining_data = {}
    hdf5_files = glob.glob(os.path.join(directory_path, "space_remaining_*.hdf5"))
    
    for hdf5_file_path in hdf5_files:
        run_number = hdf5_file_path.split('_')[-1].split('.')[0]  # Extract run number from file name
        key_name = f"Run_{run_number}"  # Construct the key name
        
        discipline_data_list = []
        with h5py.File(hdf5_file_path, 'r') as hdf_file:
            for discipline_group_name in hdf_file:
                discipline_data = []
                discipline_group = hdf_file[discipline_group_name]
                
                for data_point_name in discipline_group:
                    data_point_group = discipline_group[data_point_name]
                    data_point_dict = {
                        'iter': data_point_group.attrs['iter'],
                        'space_remaining': data_point_group['space_remaining'][:]
                    }
                    discipline_data.append(data_point_dict)
                
                discipline_data_list.append(discipline_data)
        
        space_remaining_data[key_name] = discipline_data_list
    
    return space_remaining_data

# Example usage:
directory_path = '.'  # Use '.' for current directory or specify a path
Test_Case_1 = load_space_remaining_from_all_hdf5(directory_path)
