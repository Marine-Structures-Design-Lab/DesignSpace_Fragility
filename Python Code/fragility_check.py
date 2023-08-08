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
                    
                    # Assign combo to a key in proper dictionaries
                    prior_data[i][combo] = np.empty((0,j))
                    posterior_data[i][combo] = np.empty((0,j))
                    
                    # Gather all relevant data for variable combination's prior
                    # and posterior arrays
                    ### ELIMINATED DATA FIRST!
                    
        
        
        
        
        
        
        
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
