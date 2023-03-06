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
# Get calculated outputs from the input values
class getOutput:
    
    # Initialize the class
    def __init__(self, Problem):
        self.P = Problem
        return
    
    # Calculate the outputs of each input point with provided equation(s)
    def getValues(self):
        
        # Loop through each discipline
        for i in range(0,len(self.P)-1):
            
            # Loop through each design point in the input space
            for j in range(0,np.shape(self.P[i]['tested_ins'][0])):
                
                # Make a copy of the analysis equation(s) before replacement
                expr = self.P[i]['fcns'].copy()
                
                # Loop through each input variable
                for k in range(0,len(self.P)[i]['ins']):
                    
                    # Substitute the input values into expression
                    expr = expr.subs(self.P[i]['ins'][k],self.P[i]['tested_ins'][j,k])
                
                # Solve the expression
                outs = sp.solve(expr)
                
                ############# See class assignOutput from Polynomial_Model4.py!
                # Loop through all outputs
                for k in range(0,len(outs)):
                    
                    # Retrieve y-variable index of the solution
                    outs_var = list(outs.keys())[k]
                    
                    
                
                # Append outputs if discipline has already calculated outputs
                if 'tested_outs' in self.P[i]:
                    print(i)
                # Create a new tested_outs key if no outputs calculated yet
                else:
                    self.P[i]['tested_outs'] = outs
                
            
            
        
        # Return new dictionary with calculated output points
        return self.P
    

