"""
SUMMARY:
Uses history of formed perceptions of feasibility within each discipline's 
design space to determine potentials for regret and windfall before quantifying
the risk of a space reduction decision by calculating the added potentials
relative to leaving the design spaces untouched.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import numpy as np
from dit import ScalarDistribution
from dit.other import generalized_cumulative_residual_entropy as gcre
from windfall_regret import minmaxNormalize


"""
SECONDARY FUNCTIONS
"""
def initializePF(passfail, Discips_fragility, mean_or_std):
    """
    Description
    -----------
    Gathers the pass-fail data pertinent to each discipline's remaining
    potential design solutions for eventual sorting of the history of a point's
    predictions.

    Parameters
    ----------
    passfail : List of dictionaries
        History of each discipline's pass-fail predictions up to a certain
        point in time
    Discips_fragility : List of dictionaries
        Contains all of the information pertaining to each discipline at the
        beginning of a space reduction cycle
    mean_or_std : String
        Either "mean" or "std" to detail whether pass-fail predictions or their
        standard deviations are to be consolidated

    Returns
    -------
    passfail_frag : Dictionary
        Consolidated pass-fail data for each discipline at the start of a space
        reduction cycle being prepared for reorganization based on the history
        of a particular point's history of pass-fail predictions
    """
    
    # Initialize a small maximum time integer
    max_time = 0
    
    # Initialize an index in the pass-fail list
    index_dict = 0
    
    # Loop through each instance of gathered pass-fail data
    for i, data in enumerate(passfail):
        
        # Continue to next set of data if dictionary key is not None
        if None not in data: continue
    
        # Check if new time is larger than current benchmark
        if data['time'] > max_time:
            
            # Set new index to current one in the loop
            index_dict = i
            
            # Reset max_time to new maximum value
            max_time = data['time']

    # Initialize dictionary of passfail predictions
    passfail_frag = {}
    
    # Loop through each instance of gathered pass-fail data
    for data in passfail:
        
        # Continue to next set of data if dictionary key is not None
        if None not in data: continue
        
        # Initialize an empty list for disciplines' data
        passfail_frag[data['time']] = []
        
        # Loop through each discipline's data
        for i, discip in enumerate(data[None]):
            
            # Find indices of remaining potential design solutions
            indices = [discip['indices'].index(x) \
                       for x in passfail[index_dict][None][i]['indices']]
            
            # Append discipline's data to the list for remaining solutions
            passfail_frag[data['time']].append(discip['non_reduced'][indices])
    
    # Identify the smallest key in the dictionary
    min_key = min(passfail_frag.keys())
    
    # Get the list of numpy arrays from the smallest key
    arrays = passfail_frag[min_key]
    
    # Check if dealing with mean assignment or standard deviation assignment
    if mean_or_std == 'mean':
        
        # Create numpy arrays of zeros with matching sizes to smallest key
        new_arrays = [np.zeros_like(array) for array in arrays]
    
    else:
        
        # Create numpy arrays of std dev of uniform distribution between -1 & 1
        new_arrays = [np.full_like(array, 1.0/np.sqrt(3.0)) \
                      for array in arrays]
    
    # Add list of arrays to dictionary under key 0
    passfail_frag[0] = new_arrays
    
    # Return the consolidated sorted passfail data
    return passfail_frag


def timeHistory(Discips_fragility):
    """
    Description
    -----------
    Initializes empty numpy arrays for the space remaining points in each
    discipline to be able to track their history of pass-fail predictions.

    Parameters
    ----------
    Discips_fragility : List of dictionaries
        Contains all of the information pertaining to each discipline at the
        beginning of a space reduction cycle

    Returns
    -------
    passfail_frag : List of lists of numpy arrays
        Empty numpy arrays for each space remaining point in a discipline for
        tracking its history of pass-fail predictions
    """
    
    # Initialize a list of passfail tracking lists for the disciplines
    passfail_frag = [[] for _ in Discips_fragility]
    
    # Loop through each discipline
    for i, discip in enumerate(Discips_fragility):
        
        # Loop over each row in the space remaining array
        for _ in range(0, discip['space_remaining'].shape[0]):
            
            # Append an empty numpy array to the inner list
            passfail_frag[i].append(np.array([]))
    
    # Return initalized lists ready to receive history of passfail values
    return passfail_frag


def reassignPF(pf_old, pf_new):
    """
    Description
    -----------
    Fill the numpy arrays with history of pass-fail predictions for each space
    remaining point in a discipline.

    Parameters
    ----------
    pf_old : Dictionary
        Consolidated pass-fail data for each discipline at the start of a space
        reduction cycle being prepared for reorganization based on the history
        of a particular point's history of pass-fail predictions
    pf_new : List of lists of numpy arrays
        Empty numpy arrays for each space remaining point in a discipline for
        tracking its history of pass-fail predictions

    Returns
    -------
    pf_new : List of Lists of numpy arrays
        Filled numpy arrays for each space remaining point in a discipline for
        tracking its history of pass-fail predictions
    """
    
    # Sort the old passfail keys by their time values
    sorted_keys = sorted(pf_old.keys())
    
    # Loop through the list of sorted keys
    for time in sorted_keys:
        
        # Loop through each discipline at the current time stamp
        for i, discip in enumerate(pf_old[time]):
            
            # Loop through discipline's passfail data
            for index, value in enumerate(discip):
                
                # Append the data to the proper index in new passfail list
                pf_new[i][index] = np.append(pf_new[i][index], value)
        
    # Return the passfail list ready for TVE and DTVE evaluation
    return pf_new


"""
MAIN FUNCTIONS
"""

def prepEntropy(pf, Df, pf_std):
    """
    Description
    -----------
    Goes through steps to organize history of each discipline's space 
    remaining points pass-fail predictions for TVE and DTVE calculations.
    
    Parameters
    ----------
    pf : List of dictionaries
        History of each discipline's pass-fail predictions up to a certain
        point in time
    Df : Dictionary
        All information pertaining to each discipline at the beginning of
        the newest space reduction cycle
    pf_std : List of dictionaries
        History of each discipline's pass-fail standard deviatiokns up to a
        certain point in time

    Returns
    -------
    passfail_frag2 : List of lists of numpy arrays
        Filled numpy arrays for each space remaining point in a discipline
        for tracking its history of pass-fail predictions
    passfail_std_frag2 : List of lists of numpy arrays
        Same thing as above except for their history of standard deviation
        values associated with the predictions
    """
    
    # Initialize an empty dictionary for consolidated passfail data
    passfail_frag1 = initializePF(pf, Df, 'mean')
    passfail_std_frag1 = initializePF(pf_std, Df, 'std')
    
    # Initalize a list for time history of passfail values
    passfail_frag2 = timeHistory(Df)
    passfail_std_frag2 = timeHistory(Df)
    
    # Populate list with time history of passfail values
    passfail_frag2 = reassignPF(passfail_frag1, passfail_frag2)
    passfail_std_frag2 = reassignPF(passfail_std_frag1, passfail_std_frag2)
    
    # Return each discipline's time history of passfail predictions for 
    # remaining design solutions in non-reduced design space
    return passfail_frag2, passfail_std_frag2


def evalEntropy(passfail_frag, passfail_std_frag):
    """
    Description
    -----------
    Calculates normalized TVE values from history of passfail predictions for
    potential design solutions remaining in each discipline's non-reduced
    design space.

    Parameters
    ----------
    passfail_frag : List of lists of numpy arrays
        Filled numpy arrays for each space remaining point in a discipline
        for tracking its history of pass-fail predictions
    passfail_std_frag : List of lists of numpy arrays
        Same thing as above except for their history of standard deviation
        values associated with the predictions

    Returns
    -------
    TVE : List of numpy arrays
        Normalized TVE values for non-reduced design space in each discipline
    """
    
    # Initialize empty TVE list
    TVE = [None for _ in passfail_frag]
    
    # Loop through each discipline
    for i, (discip_pf, discip_pf_std) in enumerate(zip(passfail_frag, 
                                                       passfail_std_frag)):
        
        # Initialize a numpy array for TVE values
        TVE[i] = np.zeros(len(passfail_frag[i]))
        
        # Loop through each history of data points' passfail predictions
        for j, (index_pf, index_pf_std) in enumerate(zip(discip_pf, 
                                                         discip_pf_std)):
            
            # Create probability array from standard deviations
            total_sum = np.sum(1.0 / index_pf_std)
            index_pf_std = (1.0 / index_pf_std) / total_sum
            
            # Create a scalar distribution for the data
            dist = ScalarDistribution(index_pf, index_pf_std)
            
            # Calculate the TVE value
            tve = gcre(dist)
            
            # Assign the TVE value to the TVE array
            TVE[i][j] = tve
        
        # Normalize TVE for the current discipline
        TVE[i] = minmaxNormalize(TVE[i])
        
    # Return normalized TVE values for each design point in non-reduced space
    return TVE
    