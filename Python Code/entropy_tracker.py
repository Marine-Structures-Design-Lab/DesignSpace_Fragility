"""
SUMMARY:


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
from point_sorter import sortPoints
from merge_constraints import sharedIndices


"""
FUNCTION
"""
def initializePF(passfail):
    
    # Initialize dictionary of passfail predictions
    passfail_frag = {}
    
    # Loop through each instance of gathered pass-fail data
    for data in passfail:
        
        # Continue to next set of data if dictionary key is not None
        if None not in data: continue
        
        # Initialize an empty list for disciplines' data
        passfail_frag[data['time']] = []
        
        # Loop through each discipline's data
        for discip in data[None]:
            
            # Append discipline's data to the list
            passfail_frag[data['time']].append(discip['non_reduced'])
    
    # Identify the smallest key in the dictionary
    min_key = min(passfail_frag.keys())
    
    # Get the list of numpy arrays from the smallest key
    arrays = passfail_frag[min_key]
    
    # Create numpy arrays of zeros with matching sizes to smallest key
    new_arrays = [np.zeros_like(array) for array in arrays]
    
    # Add list of arrays to dictionary under key 0
    passfail_frag[0] = new_arrays
    
    # Return the consolidated sorted passfail data
    return passfail_frag


def timeHistory(Discips_fragility):
    
    # Initialize a list of passfail tracking lists for the disciplines
    passfail_frag = [[] for _ in Discips_fragility]
    
    # Loop through each discipline
    for i, discip in enumerate(Discips_fragility):
        
        # Loop over each row in the space remaining array
        for j in range(0, discip['space_remaining'].shape[0]):
            
            # Append an empty numpy array to the inner list
            passfail_frag[i].append(np.array([]))
    
    # Return initalized lists ready to receive history of passfail values
    return passfail_frag


def reassignPF(pf_old, pf_new):
    
    # Sort the old passfail keys by their time values
    sorted_keys = sorted(pf_old.keys())
    
    # Loop through the list of sorted keys
    for time in sorted_keys:
        
        # Loop through each discipline
        for i, discip in enumerate(pf_old[time]):
            
            # Loop through discipline's passfail data at the time stamp
            for index, value in enumerate(discip):
                
                # Append the data to the proper index in new passfail list
                pf_new[i][index] = np.append(pf_new[i][index], value)
        
    # Return the passfail list ready for TVE and DTVE evaluation
    return pf_new



"""
CLASS
"""
class entropyTracker:
    
    def __init__(self, passfail, Discips_fragility):
        self.pf = passfail
        self.Df = Discips_fragility
        return
    
    
    def prepEntropy(self):
        
        # Initialize an empty dictionary for consolidated passfail data
        passfail_frag1 = initializePF(self.pf)
        
        # Initalize a list for time history of passfail values
        passfail_frag2 = timeHistory(self.Df)
        
        # Populate list with time history of passfail values
        passfail_frag2 = reassignPF(passfail_frag1, passfail_frag2)
        
        # Return each discipline's time history of passfail predictions for 
        # remaining design solutions in non-reduced design space
        return passfail_frag2
    
    
    def evalEntropy(self, passfail_frag):
        
        # Initialize empty TVE and DTVE lists
        TVE = [[] for _ in passfail_frag]
        DTVE = [[] for _ in passfail_frag]
        
        # Loop through each discipline
        for i, discip in enumerate(passfail_frag):
            
            # Loop through each history of data points' passfail predictions
            for index in discip:
                
                # Determine equal probability for each passfail prediction
                prob = 1 / len(index)
                
                # Create a scalar distribution for the data
                dist = ScalarDistribution({value: prob for value in index})
                
                # Calculate the TVE value
                tve = gcre(dist)
                
                # Append the TVE value to the inner TVE list
                TVE[i].append(tve)
                
                # Calculate the difference between consecutive predictions
                diffs = np.diff(index)
                
                # Determine new equal probability for each passfail prediction
                prob = 1 / len(diffs)
                
                # Create a scalar distribution for the difference data
                dist = ScalarDistribution({value: prob for value in diffs})
                
                # Calculate the DTVE value
                dtve = gcre(dist)
                
                # Append the DTVE value to the inner DTVE list
                DTVE[i].append(dtve)
        
        # Return TVE and DTVE values for each design point in non-reduced space remaining
        return TVE, DTVE
    
    
    
    def calcWindRegret(self, TVE, DTVE):
        
        
        wr = 0
        
        run_wind = 0
        
        run_reg = 0
        
        
        return wr, run_wind, run_reg
    
    
    
    
    
    
    
    def quantRisk(self, run_wind, run_reg, wr):
        
        ris = 0
        
        return ris
    
    
    
    
    

    
