# -*- coding: utf-8 -*-
"""
DESCRIPTION:
Provides different algorithms for producing random points to be tested in a
discipline's input space.  All input variables must be normalized over its own
range such that the input spaces only consist of values between 0 and 1.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import numpy as np

"""
COMMANDS
"""
# Get random inputs for the independent variables
class getInput:
    
    # Initialize the class
    def __init__(self,Problem):
        self.P = Problem
        return
    
    # Assign uniform random values to each input variable - THIS SHOULD BE REPLACED WITH AN ACTUAL SAMPLING LIBRARY...SEE scipy.stats.qmc
    def getUniform(self):
        
        # Loop through each discipline
        for i in range(0,len(self.P)-1):
            
            # Append new points to test if discipline has already tested points
            if 'tested_ins' in self.P[i]:
                self.P[i]['tested_ins'] = np.append\
                    (self.P[i]['tested_ins'],\
                     np.random.rand(1,len(self.P[i]['ins'])),\
                     axis = 0)
            # Create a new tested_ins key if no points have been tested yet
            else:
                self.P[i]['tested_ins'] = np.random.rand\
                    (1,len(self.P[i]['ins']))
            
        # Return new dictionary with uniform random input points to be tested
        return self.P