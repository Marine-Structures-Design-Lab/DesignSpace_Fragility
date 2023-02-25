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
    def __init__(self,Problem,Set_rules,iters):
        self.P = Problem
        self.sr = Set_rules
        self.i = iters
        return
    
    # Assign uniform random values to each input variable - THIS SHOULD BE REPLACED WITH AN ACTUAL SAMPLING LIBRARY...SEE scipy.stats.qmc
    def getUniform(self):
        
        # Loop through each discipline
        for i in range(0,len(self.P)-1):
            
            # Initialize counting variables
            count1 = 0
            count2 = 0
            
            # Loop through potential uniform test points to add to discipline
            while count1 < self.i:
                
                # Prevent an infinite loop from occurring (change value being
                # multiplied by self.i if desired)
                if count2 >= 100*self.i:
                    print("Only created " + count1 + \
                          " new input point(s) instead of " + self.i)
                    break
                
                # Increase the second counting variable by 1
                count2 = count2 + 1
                
                # Create a new input point in the normalized value bounds (0 to 1)
                point = np.random.rand(1,len(self.P[i]['ins']))
                
                # Check if input point abides by all of the current set_rules
                ### SHOULD PROBABLY TURN THIS INTO SOME SORT OF FUNCTION
                ###### This is going to be tricky and may required nested functions
                
                
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
                
                
                #### MAKE SURE I BRING THE COUNT1 UP ONE!
                
        # Return new dictionary with uniform random input points to be tested
        return self.P