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
from output_start import outputStart

"""
CLASS
"""
class getOutput:
    
    def __init__(self,discip):
        self.d = discip
        return
    
    # Calculate the outputs of each input point with provided equation(s)
    def getValues(self):
        """
        Description
        -----------
        Calculates the output values based on the provided input values and
        equations and then assigns those values to the proper numpy indices as
        part of the "tested_outs" key
        
        Parameters
        ----------
        self.d : Dictionary
            The complete dictionary of sympy inputs, sympy outputs, sympy
            expressions, execution time, tested input points, and an empty or
            partially filled list of calculated output points
            
        Returns
        -------
        self.d : Dictionary
            The complete dictionary of sympy inputs, sympy outputs, sympy
            expressions, execution time, and a completely filled list of tested
            output points that coincides with the input points
        """
        
        # Loop through each NEW design point in the input space
        for i in range(outputStart(self.d,'tested_outs'),\
                       np.shape(self.d['tested_ins'])[0]):
            
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

