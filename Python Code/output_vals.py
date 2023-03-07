"""
SUMMARY:
Calculates output value(s) for each design point in the input space that is
provided.  For now, this class is geared towards mathematical equations.
Later, this class may be more geared towards simply calling on and/or setting
up an external marine design program for calculating the output value(s).

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import numpy as np
import sympy as sp

"""
CLASS
"""
class getOutput:
    
    def __init__(self,discip,iters):
        self.d = discip
        self.it = iters
        return
    
    # Calculate the outputs of each input point with provided equation(s)
    def getValues(self):
        '''
        Description
        -----------
        Calculates the output values based on the provided input values and
        equations and then assigns those values to the proper numpy indices as
        part of the "tested_outs" key
        
        Parameters
        ----------
        self.d : Dictionary
            The complete dictionary of sympy inputs, sympy outputs, sympy
            expressions, tested input points, and an empty or partially filled
            list of calculated output points
        self.it : Integer
            Tracks the number of time iterations that have been conducted thus
            far so it is known what inputs have not been tested yet
            
        Returns
        -------
        self.d : Dictionary
            The complete dictionary of sympy inputs, sympy outputs, sympy
            expressions, and a completely filled list of tested output points
            that coincides with the input points
        '''
        
        # Loop through each NEW design point in the input space
        ### GOING TO HAVE TO FIX THIS FOR WHEN EACH TIME ITERATION IS NOT LONG
        ### ENOUGH TO PERFORM ONE FUNCTION EVALUATION
        for i in range(self.it,np.shape(self.d['tested_ins'])[0]):
            
            # Make a copy of the analysis equation(s) before replacement
            expr = self.d['fcns'].copy()
            
            # Loop through each input variable
            for j in self.d['ins']:
                
                # Loop through each equation of the discipline
                for k in range(0,len(self.d['fcns'])):
                    
                    # Substitute input value in for variable in equation
                    expr[k] = expr[k].subs(j,\
                                self.d['tested_ins'][i,self.d['ins'].index(j)])
            
            # Solve the equation(s)
            sols = sp.solve(expr)
            
            # Create a numpy zeros arrays for the answers to populate
            temp_array = np.zeros(len(sols))
            
            # Loop through all solutions
            for j in range(0,len(sols)):
                
                # Isolate variable from solution dictionary
                ind_var = list(sols.keys())[j]
                
                # Locate index of variable in discipline's outputs
                ind_num = self.d['outs'].index(ind_var)
                
                # Place output into proper index of temporary array
                temp_array[ind_num] = sols[ind_var]
            
            # Append new point to the tested outputs
            self.d['tested_outs'] = np.append(self.d['tested_outs'],temp_array)
            
            # Reshape the numpy array of calculated output points
            self.d['tested_outs'] = \
                np.reshape(self.d['tested_outs'],(-1,len(self.d['outs'])))
        
        # Return new dictionary with calculated output points
        return self.d
    
    # Calling on black-box programs for other methods instead of equations?

