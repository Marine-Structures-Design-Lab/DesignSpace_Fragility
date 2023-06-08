"""
SUMMARY:
Provides different algorithms for producing points to be tested in a
discipline's input space.  All input values must fall within the presently
allowed constraints.  All input points of this class are assumed to be
normalized variables initially falling within the 0 to 1 range.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import numpy as np
import copy

"""
CLASS
"""
class getInput:
    
    def __init__(self, discip, input_rules, iters, i):
        """
        Parameters
        ----------
        discip : Dictionary
            Contains various key-value pairs associated with the current 
            details of the particular discipline
        input_rules : List of symbolic inequalities
            A condensed list of rules that the particular discipline considers
        iters : Integer
            The desired amount of time iterations to produce input points
        i : Integer
            Identification of the discipline index for which input points are
            being produced
        """
        self.d = discip
        self.ir = input_rules
        self.it = iters
        self.i = i
    
    
    def getUniform(self):
        """
        Description
        -----------
        Produces uniform random values for each normalized input variable and
        commits to the point produced when it is determined that it abides by
        the current set of all established input rules
        
        Parameters
        ----------
        None.
        
        Returns
        -------
        self.d : Dictionary
            The same dictionary now updated with any new input points from
            exploration for evaluation
        """
        
        # Initialize counting variables
        count1 = 0
        count2 = 0
        
        # Loop through potential uniform test points to add to discipline
        while count1 < self.it//self.d['time']:
            
            # Prevent an infinite loop from occurring (change value being
            # multiplied by self.it, if desired)
            if count2 >= 100*self.it*self.d['time']:
                print(
                    f"Only created {count1} new input point(s) for Discipline "
                    f"{self.i+1} instead of "
                    f"{self.it//self.d['time']}"
                    )
                break
            
            # Increase the second counting variable by 1
            count2 += 1
            
            # Only try creating a point when the time iteration allows for it
            if count2 % self.d['time'] == 0:
                
                # Create new input point in normalized value bounds (0 to 1)
                point = np.random.rand(len(self.d['ins']))
                
                # Create a copy of the list of input rules
                rules_copy = copy.deepcopy(self.ir)
                
                # Loop through each input rule
                for i in range(0,len(self.ir)):
                    
                    # Convert set of variables to a list
                    symbs = list(self.ir[i].free_symbols)

                    # Loop through each symbol of the rule
                    for j in range(0,len(symbs)):
                        
                        # Gather index of the symbol in the discipline's inputs
                        index = self.d['ins'].index(symbs[j])
                        
                        # Substitute index value from point to rule
                        rules_copy[i] = rules_copy[i].subs\
                            (self.d['ins'][index],point[index])
                    
                # Check if necessary value(s) in the rules list copy is true
                if all(rules_copy):
                    
                    # Append new points to the tested inputs
                    self.d['tested_ins'] = \
                        np.append(self.d['tested_ins'],point)
                    
                    # Increase the first counting variable by 1
                    count1 += 1
                
        # Reshape the numpy array of tested input points
        self.d['tested_ins'] = \
            np.reshape(self.d['tested_ins'],(-1,len(self.d['ins'])))
        
        # Return new dictionary with uniform random input points
        return self.d


    # ACTUAL SAMPLING LIBRARIES...SEE scipy.stats.qmc
