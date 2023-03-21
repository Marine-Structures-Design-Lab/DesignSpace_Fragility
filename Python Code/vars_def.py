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
from var_rule import varRule

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
        set_rules : Set containing strings
            The initial set of constraints/rules that each discipline must
            abide by when determining designs to test in the input space and
            if those tested designs produce passing outputs
        '''
        
        # Create sympy input and output variables
        x = sp.symbols('x1 x2 x3 x4 x5 x6')
        y = sp.symbols('y1 y2 y3 y4 y5')
        
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
        
        # Create a list containing the initial rules for the design problem
        ### Put rules that go together with an "and" in the same string
        ### Put rules that go together with an "or" into separate strings
        ### All rules must be in a list even if only a single string
        ### Use comma to separate rules in a string along with no spaces at all
        rules = []
        rules.append(varRule(['x1>=0.0,x1<=1.0']))
        rules.append(varRule(['x2>=0.0,x2<=1.0']))
        rules.append(varRule(['x3>=0.0,x3<=1.0']))
        rules.append(varRule(['x4>=0.0,x4<=1.0']))
        rules.append(varRule(['x5>=0.0,x5<=1.0']))
        rules.append(varRule(['x6>=0.0,x6<=1.0']))
        rules.append(varRule(['y1>=0.0,y1<=0.4','y1>=1.2,y1<=1.6']))
        rules.append(varRule(['y2>=0.5,y2<=0.7']))
        rules.append(varRule(['y3>=0.2,y3<=0.5']))
        rules.append(varRule(['y4>=0.0,y4<=0.5']))
        rules.append(varRule(['y5>=0.8,y5<=1.6']))
        
        # Return each discipline's dictionary for SBD1 problem
        return [discip1, discip2, discip3], rules
    
    # Can define other problems similar to as was done for the SBD1 problem...
    
    
    
    