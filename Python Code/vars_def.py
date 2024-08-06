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
        """
        Description
        -----------
        Creates the list of dictionaries and set of rules for Set-Based Design
        Problem 1.  Important to make sure that all dictionary values are
        contained within a list regardless of if it is only a single value.
        
        Parameters
        ----------
        None.
        
        Returns
        -------
        [discip1, discip2, discip3] : List of dictionaries
            Contains sympy inputs, outputs, and expressions for each individual
            discipline of the particular design problem
        input_rules : List of sympy relationals
            The initial set of input constraints/rules that each discipline
            must abide by when determining designs to test in the input space
        output_rules : List of sympy relationals
            The initial set of output constraints/rules that each discipline
            must abide by when determining if tested designs produce passing
            outputs in the objective space
        """
        
        # Create sympy input and output variables
        x = sp.symbols('x1:7')
        y = sp.symbols('y1:6')
        
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
        
        # Create a list for the initial input rules
        ### ALL VARIABLES OF INEQUALITY MUST BE ON LEFT-HAND SIDE
        ### FREE-STANDING NUMBERS MUST BE ON THE RIGHT-HAND SIDE
        ### CAN ONLY HAVE SYMPY AND/OR RELATIONALS
        ### LEFT-HAND SIDE OF RULE MUST BE SAME THROUGHOUT AND/OR RELATIONALS
        input_rules = [sp.And(x[i] >= 0.0, x[i] <= 1.0) for i in range(len(x))]
        
        # Create a list for the initial output rules
        ### SAME STRUCTURE AS THE INPUT RULES
        ### sp.And should be reserved when trying to define an area that is
        ### cut off on both sides for one variable...if the user finds
        ### themselves creating a rule such as y[0] > 1 AND y[1] > 1, then it
        ### should be split up into two separate rules on the list
        output_rules = [sp.Or(sp.And(y[0]>=0.0,y[0]<=0.4),\
                              sp.And(y[0]>=1.2,y[0]<=1.6)),
                        sp.And(y[1]>=0.5,y[1]<=0.7),
                        sp.And(y[2]>=0.2,y[2]<=0.5),
                        sp.And(y[3]>=0.0,y[3]<=0.5),
                        sp.And(y[4]>=0.8,y[4]<=1.6)]

        # Return discipline dictionaries for SBD1 problem and rule lists
        return [discip1, discip2, discip3], input_rules, output_rules
    
    
    def SenYang(self):
        
        def X(x_norm, index):
            
            # Define each design variable's upper and lower bounds
            bounds = {
                0: (195.2, 362.0), # Example bounds for x[0] --> Length
                1: (10.3, 21.7),   # Example bounds for x[1] --> Draft
                2: (13.1, 30.0),   # Example bounds for x[2] --> Depth
                3: (0.63, 0.75),   # Example bounds for x[3] --> Block coeff.
                4: (5.0, 60.0),    # Example bounds for x[4] --> Breadth
                5: (14.0, 18.0)    # Example bounds for x[5] --> Speed
            }
            
            # Assign proper upper and lower bounds based on design variable
            lower, upper = bounds[index]
            
            # Denormalize the design variable
            x_denorm = x_norm*(upper - lower) + lower
            
            # Return the denormalized design variable
            return x_denorm
        
        
        # Create sympy input and output variables
        ### REMINDER THAT THE "x" SYMBOLS REPRESENT NORMALIZED VALUES!
        x = sp.symbols('x1:7') # L, T, D, C_B, B, V
        y = sp.symbols('y1:4') # F_n, GM, DW
        
        # Create dictionary for Hydrodynamics division
        hydro = {
            "ins": [x[0], x[1], x[2], x[3], x[4], x[5]],
            "outs": [y[0]],
            "fcns": [X(x[5],5) / (9.8065*X(x[0],0))**0.5 - y[0]],
        }
        
        # Create dictionary for Stability division
        stability = {
            "ins": [x[0], x[1], x[2], x[3], x[4], x[5]],
            "outs": [y[1]],
            "fcns": [0.53*X(x[1],1) + \
                     ((0.085*X(x[3],3)-0.002)*X(x[4],4)**2)/\
                         (X(x[1],1)*X(x[3],3)) - \
                     (1.0+0.52*X(x[2],2)) - y[1]],
        }
        
        # Create dictionary for Weights division
        weights = {
            "ins": [x[0], x[1], x[2], x[3], x[4], x[5]],
            "outs": [y[2]],
            "fcns": [1.025*X(x[0],0)*X(x[4],4)*X(x[1],1)*X(x[3],3) - \
                     (0.034*X(x[0],0)**1.7*X(x[4],4)**0.7*X(x[2],2)**0.4\
                          *X(x[3],3)**0.5 + \
                        1.0*X(x[0],0)**0.8*X(x[4],4)**0.6*X(x[2],2)**0.3\
                          *X(x[3],3)**0.1 + \
                        0.17*((1.025*X(x[0],0)*X(x[4],4)*X(x[1],1)\
                            *X(x[3],3))**(2.0/3.0)*X(x[5],5)**3\
                          *(1/((-10847.2*X(x[3],3)**2+12817\
                            *X(x[3],3)-6960.32)*\
                          (X(x[5],5)/(9.8065*X(x[0],0))**0.5)+\
                          (4977.06*X(x[3],3)**2-8105.61*X(x[3],3)+4456.51))))\
                            **0.9) - \
                     y[2]],
        }
        
        # Create a list for the initial input rules
        ### ALL VARIABLES OF INEQUALITY MUST BE ON LEFT-HAND SIDE
        ### FREE-STANDING NUMBERS MUST BE ON THE RIGHT-HAND SIDE
        ### CAN ONLY HAVE SYMPY AND/OR RELATIONALS
        ### LEFT-HAND SIDE OF RULE MUST BE SAME THROUGHOUT AND/OR RELATIONALS
        in_rules = [sp.And(x[i] >= 0.0, x[i] <= 1.0) for i in range(len(x))] +\
                   [X(x[0],0)/X(x[4],4) >= 6.0, X(x[0],0)/X(x[1],1) <= 19.0, 
                    X(x[0],0)/X(x[2],2) <= 15.0, 
                    X(x[1],1) - 0.7*X(x[2],2) <= 0.7,
                    (-10847.2*X(x[3],3)**2+12817*X(x[3],3)-6960.32)*(X(x[5],5)\
                      /(9.8065*X(x[0],0))**0.5)+(4977.06*X(x[3],3)**2-8105.61*\
                      X(x[3],3)+4456.51) > 0.0]
        
        # Create a list for the initial output rules
        ### SAME STRUCTURE AS THE INPUT RULES
        ### sp.And should be reserved when trying to define an area that is
        ### cut off on both sides for one variable...if the user finds
        ### themselves creating a rule such as y[0] > 1 AND y[1] > 1, then it
        ### should be split up into two separate rules on the list
        output_rules = [y[0] <= 0.32, y[1] - 0.07*X(x[4],4) >= 0.0, 
                        sp.And(y[2] >= 3000, y[2] <= 500000),
                        y[2] - (X(x[1],1)/0.45)**(1.0/0.31) >= 0.0]
        
        # Return discipline dictionaries for Sen-Yang problem and rule lists
        return [hydro, stability, weights], in_rules, output_rules

