"""
SUMMARY:
Establishes the disciplines and variables associated with each discipline
depending on the title of the problem being solved.  Problems involving
mathematical equations will have functions and variables defined.  Problems
involving black-box marine design programs will only have variables defined.
The functions defined in the dictionaries of disciplines involving mathematical
functions may only be used to produce an output based on inputs for exploration
purposes.  In other words, the designers should still treat these mathematical
functions as black-box programs.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import sympy as sp

"""
CLASS
"""
class setProblem:
    
    def __init__(self):
        pass
    
    def SBD1(self):
        '''
        Description
        -----------
        Creates the list of dictionaries and set of rules for Set-Based Design
        Problem 1.  Important to make sure that all dictionary values are
        contained within a list regardless of it it is only a single value.
        
        Parameters
        ----------
        None.
        
        Returns
        -------
        [discip1, discip2, discip3] : List of dictionaries
            Contains sympy inputs, outputs, and expressions for each individual
            discipline of the particular design problem
        input_rules : List of class objects
            The initial set of input constraints/rules that each discipline
            must abide by when determining designs to test in the input space
        output_rules : List of class objects
            The initial set of output constraints/rules that each discipline
            must abide by when determining if tested designs produce passing
            outputs in the objective space
        '''
        
        # Create sympy input and output variables
        x = sp.symbols('x:6')
        y = sp.symbols('y:5')
        
        # Create dictionary for Discipline 1
        discip1 = {
            "ins": [x[0], x[1], x[2]],
            "outs": [y[0]],
            "fcns": [0.8*x[0]**2 + 2*x[1]**2 - x[2] - y[0]],
        }
        
        # Create dictionary for Discipline 2
        discip2 = {
            "ins": [x[2], x[3], x[4]],
            "outs": [y[1], y[2]],
            "fcns": [1.25*x[4] - 12.5*x[2]**3 + 6.25*x[2]**2 - y[1],
                     (x[3]**3 + x[4])**2 - y[2]],
        }
        
        # Create dictionary for Discipline 3
        discip3 = {
            "ins": [x[0], x[4], x[5]],
            "outs": [y[3], y[4]],
            "fcns": [2*x[4] + 0.2*sp.sin(25*x[5]) - x[0]**(1/5) - y[3],
                     x[0]**(1/3) - sp.cos(3*x[4]) - y[4]],
        }
        
        ### ALL VARIABLES OF RULE MUST BE ON LEFT HAND SIDE OF INEQUALITY
        ### FREE-STANDING NUMBERS SHOULD BE ON THE RIGHT HAND SIDE
        ### CAN ONLY HAVE SYMPY AND, OR RELATIONALS
        # Create initial input rules for the design problem
        input_rules = []
        for i in range(0,len(x)):
            input_rules.append(sp.And(x[i]>=0.0,x[i]<=1.0))
            
        # Create initial output rules for the design problem
        output_rules = []
        output_rules.append(sp.Or(sp.And(y[0]>=0.0,y[0]<=0.4), sp.And(y[0]>=1.2,y[0]<=1.6)))
        output_rules.append(sp.And(y[1]>=0.5,y[1]<=0.7))
        output_rules.append(sp.And(y[2]>=0.2,y[2]<=0.5))
        output_rules.append(sp.And(y[3]>=0.0,y[3]<=0.5))
        output_rules.append(sp.And(y[4]>=0.8,y[4]<=1.6))
        
        # Return each discipline's dictionary for SBD1 problem and rules lists
        return [discip1, discip2, discip3], input_rules, output_rules
    
    # Can define other problems similar to as was done for the SBD1 problem...
    