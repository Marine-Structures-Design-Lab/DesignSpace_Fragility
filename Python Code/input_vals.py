"""
SUMMARY:
Provides different algorithms for producing random points to be tested in a
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

"""
CLASS
"""
class getInput:
    
    def __init__(self,discip,input_rules,iters,i):
        self.d = discip
        self.ir = input_rules
        self.it = iters
        self.i = i
        return
    
    def getUniform(self):
        '''
        Description
        -----------
        Produces uniform random values for each normalized input variable and
        commits to the point produced when it is determined that it abides by
        the current set of all set rules/constraints
        
        Parameters
        ----------
        self.d : Dictionary
            The complete dictionary of sympy inputs, sympy outputs, sympy
            expressions, execution time, and an empty or partially filled list
            of tested input points
        self.ir : List of symbolic inequalities
            A condensed list of rules that the particular discipline passed
            to this method must consider
        self.it : Integer
            The desired amount of time iteration to produce input points
        self.i : Integer
            Identification of the discipline number for which input points are
            being produced

        Returns
        -------
        self.d : Dictionary
            The complete dictionary of sympy inputs, sympy outputs, sympy
            expressions, execution time, and a partially or completely filled
            list of tested input points
        '''
        
        # Initialize counting variables
        count1 = 0
        count2 = 0
        
        # Loop through potential uniform test points to add to discipline
        while count1 < self.it//self.d['time']:
            
            # Prevent an infinite loop from occurring (change value being
            # multiplied by self.it, if desired)
            if count2 >= 100*self.it*self.d['time']:
                print("Only created " + str(count1) + \
                      " new input point(s) for Discipline " + str(self.i+1) + \
                      " instead of " + str(self.it//self.d['time']))
                break
            
            # Increase the second counting variable by 1
            count2 += 1
            
            # Only try creating a point when the time iteration allows for it
            if count2 % self.d['time'] == 0:
                
                # Create a new input point in the normalized value bounds (0 to 1)
                point = np.random.rand(len(self.d['ins']))
                
                # Create a copy of the list of rules
                rules_copy = self.ir.copy()
                
                # Loop through each rule
                for j in range(0,len(self.ir)):
                    
                    # Gather free symbol(s) of the rule
                    symbs = list(self.ir[j].free_symbols)
                    
                    # Loop through each symbol of the rule
                    for k in range(0,len(symbs)):
                        
                        # Gather index of the symbol in the discipline's inputs
                        index = self.d['ins'].index(symbs[k])
                        
                        # Substitute proper index value from point into the rule
                        rules_copy[j] = \
                            self.ir[j].subs(self.d['ins'][index],point[index])
                
                # Check if each value in the copy of the rules list is true
                if all(rules_copy):
                    
                    # Append new points to the tested inputs
                    self.d['tested_ins'] = \
                        np.append(self.d['tested_ins'],point)
                    
                    # Increase the first counting variable by 1
                    count1 += 1
                
        # Reshape the numpy array of tested input points
        self.d['tested_ins'] = \
            np.reshape(self.d['tested_ins'],(-1,len(self.d['ins'])))
        
        # Return new dictionary with uniform random input points to be tested
        return self.d
    
    # ACTUAL SAMPLING LIBRARIES...SEE scipy.stats.qmc