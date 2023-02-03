# -*- coding: utf-8 -*-
"""
DESCRIPTION:
Establishes the disciplines and variables associated with each discipline
depending on the title of the problem being solved.  Problems involving
mathematical equations will have functions and variables defined.  Problems
involving black-box marine design programs will only have variables defined.
The functions defined in the dictionaries of discipline's involving
mathematical functions may only be used to produce an output based on inputs
for exploration purposes.  In other words, the designers should still treat
these mathematical functions as black-box programs.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import sympy as sp

"""
CLASSES
"""
# Create dictionaries for each discipline of the specific problem
class setProblem:
    
    # Initialize the class
    def __init__(self):
        pass
    
    # Create dictionary for SBD1 problem
    def SBD1(self):
        
        # Create sympy input and output variables
        x = sp.symbols('x1 x2 x3 x4 x5 x6')
        y = sp.symbols('y1 y2 y3 y4 y5')
        
        # Create dictionary for Discipline 1
        discip1 = {
            "vars": [x[0], x[1], x[2], y[0]],
            "fcns": 0.8*x[0]**2 + 2*x[1]**2 - x[2] - y[0]
        }
        
        # Create dictionary for Discipline 2
        discip2 = {
            "vars": [x[2], x[3], x[4], y[1], y[2]],
            "fcns": [1.25*x[4] - 12.5*x[2]**3 + 6.25*x[2]**2 - y[1],
                     (x[3]**3 + x[4])**2 - y[2]]
        }
        
        # Create dictionary for Discipline 3
        discip3 = {
            "vars": [x[0], x[4], x[5], y[3], y[4]],
            "fcns": [2*x[4] + 0.2*sp.sin(25*x[5]) - x[0]**(1/5) - y[3],
                     x[0]**(1/3) - sp.cos(3*x[4]) - y[4]]
        }
        
        # Return each discipline's dictionary for SBD1 problem
        return discip1, discip2, discip3
    
    # Can define other problems similar to as was done for the SBD1 problem...
    
    
    
    