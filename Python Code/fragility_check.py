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
import itertools

"""
CLASS
"""
class checkFragility:
    
    def __init__(self, Discips, irules_new):
        self.D = Discips
        self.ir = irules_new
        return
    
    # Organize data into numpy arrays (x-locs, fail_amount)
    def createDataSets(self, KLgap):
        
        # Create empty lists of dictionaries corresponding to each discipline
        prior_data = [{} for _ in self.D]
        posterior_data = [{} for _ in self.D]
        
        # Loop through each discipline
        for i in range(0, len(self.D)):
            
            # Loop over all possible input variable combination lengths
            for j in range(1, len(self.D[i]['ins'])+1):
                
                # Generate combinations
                for combo in itertools.combinations(self.D[i]['ins'], j):
                    
                    # Gather the indices of the variables in the combo
                    indices = [self.D[i]['ins'].index(var) for var in combo]
                    indices = tuple(indices)
                    
                    # Collect eliminated data
                    elim_data = self.D[i].get('eliminated', {})
                    etested_ins = elim_data.get('tested_ins', np.empty((0, j)))
                    etested_ins = etested_ins[:, indices]
                    ef_amount = elim_data.get('Fail_Amount', np.array([]))
                    ef_amount = np.reshape(ef_amount, (-1, 1))
                    elim_data = np.hstack((etested_ins, ef_amount))
                    
                    # Collect non-eliminated data
                    tested_ins = self.D[i].get('tested_ins', np.empty((0, j)))
                    tested_ins = tested_ins[:, indices]
                    f_amount = self.D[i].get('Fail_Amount', np.array([]))
                    f_amount = np.reshape(f_amount, (-1, 1))
                    nonelim_data = np.hstack((tested_ins, f_amount))
                    
                    # Add eliminated and non-eliminated data together
                    all_data = np.vstack((elim_data, nonelim_data))
                    
                    # Assign proper rows of data to prior and posterior arrays
                    prior_data[i][combo] = all_data[:-KLgap]
                    posterior_data[i][combo] = all_data
        
        # Return the prior and posterior data sets
        return prior_data, posterior_data
    
    
    
    
    # Set the parameters for the data sets
    def initializeParams(self):
        return
    
    
    # Calculate the mutual information between each set of input variables
    def mutualInfo(self):
        return
    
    # Return a true or false boolean value if fragile or not
    def basicCheck(self):
        
        fragile = False
        
        return fragile
