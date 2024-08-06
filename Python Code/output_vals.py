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
        """
        Parameters
        ----------
        discip : Dictionary
            Contains various key-value pairs associated with the current 
            details of the particular discipline
        """
        self.d = discip
        return
    
    def getValues(self):
        """
        Description
        -----------
        Calculates the output values based on the provided input values and
        equations and then assigns those values to the proper numpy indices in
        the "tested_outs" key
        
        Parameters
        ----------
        None.
        
        Returns
        -------
        self.d : Dictionary
            The same dictionary now updated with new output values as
            calculated from the input points and provided equations
        """
        
        # Initial definitions to make code more readable
        start = outputStart(self.d, 'tested_outs')
        tested_ins = self.d['tested_ins']
        
        # Loop through each NEW design point in the input space
        for i in range(start, tested_ins.shape[0]):
            
            # Make a copy of the analysis equation(s) before replacement
            expr = self.d['fcns'].copy()
            
            # Loop through each input variable
            for j in self.d['ins']:
                
                # Loop through each equation of the discipline
                for k in range(0,len(self.d['fcns'])):
                    
                    print(self.d['tested_ins'][i,self.d['ins'].index(j)])
                    # Substitute input value in for variable in equation
                    expr[k] = expr[k].subs(j,\
                                self.d['tested_ins'][i,self.d['ins'].index(j)])
            
            # Solve the equation(s)
            sols = sp.solve(expr)
            
            # Create a numpy zeros arrays for the answers to populate
            temp_array = np.zeros(len(sols))
            
            # Loop through all solutions
            for j, ind_var in enumerate(sols.keys()):
                
                # Locate index of variable in discipline's outputs
                ind_num = self.d['outs'].index(ind_var)
                
                # Place output into proper index of temporary array
                temp_array[ind_num] = sols[ind_var]
            
            # Append new point to the tested outputs
            self.d['tested_outs'] = np.append(self.d['tested_outs'],temp_array)
            
        # Reshape the numpy array of calculated output points
        self.d['tested_outs'] = \
            self.d['tested_outs'].reshape(-1, len(self.d['outs']))
        
        # Return new dictionary with calculated output points
        return self.d
    
    # Calling on black-box programs for other methods instead of equations?

