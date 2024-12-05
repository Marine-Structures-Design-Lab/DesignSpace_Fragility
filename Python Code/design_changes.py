"""
SUMMARY:
Set up for SenYang problem specifically!!!

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from output_start import outputStart
from get_constraints import getConstraints, getInequalities
from calc_rules import calcRules
from output_success import outputDiff
import numpy as np
import sympy as sp
import copy


"""
CLASS
"""
class changeDesign:
    
    def __init__(self, Discips, Input_Rules, Output_Rules):
        """
        Parameters
        ----------
        Discips : Dictionary
            DESCRIPTION.
        Output_Rules : 
            DESCRIPTION
        """
        self.D = Discips
        self.In_Rules = Input_Rules
        self.Out_Rules = Output_Rules
        return
    
    
    # Addition or subtraction of any input variables for a discipline
    def Inputs(self):
        
        
        return self.D, self.In_Rules, self.Out_Rules
    
    
    # Changes to the analyses used to calculate output points from input points
    def Analyses(self):
        
        
        return self.D, self.In_Rules, self.Out_Rules
    
    
    # Addition or subtraction of any output variables for a discipline
    def Outputs(self):
        
        
        return self.D, self.In_Rules, self.Out_Rules
    
    
    # Changes to objective space requirements
    def Reqs(self):
        
        def X(x_norm, index):
            """
            Description
            -----------
            Creates an expression that denormalizes an input variable.

            Parameters
            ----------
            x_norm : Sympy variable
                The normalized input variable.
            index : Integer
                Index of the particular input variable.

            Returns
            -------
            x_denorm : Sympy expression
                The denormalized input variable expression.
            """
            
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
        
        # Create sympy design and output variables
        x = sp.symbols('x1:7') # L, T, D, C_B, B, V
        y = sp.symbols('y1:4') # F_n, GM, DW
        
        # Adjust the list of output rules - ~50% FEASIBLE SPACE REDUCTION!
        output_rules = [y[0] <= 0.292, y[1] - 0.092*X(x[4],4) >= 0.0, 
                        sp.And(y[2] >= 94000, y[2] <= 190000),
                        y[2] - (X(x[1],1)/0.45)**(1.0/0.31) >= 0.0]
        
        # Assign new output rules to the problem
        self.Out_Rules = output_rules
        
        # Return the discipline and rule information for the problem
        return self.D, self.In_Rules, self.Out_Rules
    
    
    
    
    
    # Reevaluate ALL previously explored points and update results...
    ### If analyses change CANNOT REEVALUATE THAT BECAUSE THAT WOULD TAKE UP TIME AGAIN!!!
    ### ALL WE CAN EVER DO IS SEE HOW MUCH A POINT CHANGES
    ### IN THE POST-PROCESSING, WE CAN LOOK AT THE RESULTS AS IF WE KNEW THE END RESULTS THE ENTIRE WAY!!!
    def reevaluatePoints(self):
        
        # Loop through each discipline
        for discip in self.D:
            
            # Determine current output value rules for the discipline to meet
            output_rules = getConstraints(discip['outs'], self.Out_Rules)
            
            # Gather any new inequalities of relevance to the discipline
            discip = getInequalities(discip, output_rules, 'out_ineqs')
            
            # Calculate left-hand side of output rule inequality for each new point
            discip['out_ineqs'] = calcRules(discip,'out_ineqs','tested_outs','outs')
            
            # Remove all of the pass?, fail amount, and pass amount data
            discip['pass?'] = []
            discip['Fail_Amount'] = np.array([], dtype=float)
            discip['Pass_Amount'] = np.array([], dtype=float)
            
            # Initial definitions to make code more readable
            start = outputStart(discip, 'pass?')
            tested_outs = discip['tested_outs']
            
            # Loop through each NEW design point in the output space
            for i in range(start, tested_outs.shape[0]):
                
                # Make a copy of the output rules
                rules_copy = copy.deepcopy(output_rules)
                
                # Loop through each output rule
                for j in range(0,len(output_rules)):
                    
                    # Loop through each output variable of the discipline
                    for k in discip['outs']:
                        
                        # Substitute output value for the variable in rule
                        rules_copy[j] = rules_copy[j].subs(k,\
                            tested_outs[i,discip['outs'].index(k)])
                        
                # Append boolean value to the proper dictionary key
                discip['pass?'].append(all(rules_copy))
            
            # Initial definitions to make code more readable
            start = outputStart(discip, 'Fail_Amount')
            pass_ = discip['pass?']
            
            # Loop through each NEW design point
            for i in range(start,len(pass_)):
                
                # Initialize a numpy vector the same length as the rules
                tv_diff = np.zeros(len(output_rules))
                
                # Loop through each output rule
                for rule in output_rules:
                    
                    # Determine normalized difference of point to rule's threshold
                    tv_diff[output_rules.index(rule)] = \
                        outputDiff(rule, i, discip)
                
                # Check if point is already passing
                if pass_[i] == True:
                    
                    # Append 0.0 to the failure amount vector
                    discip['Fail_Amount'] = np.append(discip['Fail_Amount'], 0.0)
                    
                    # Calculate minimum difference for set of relevant output rules
                    min_d = np.nanmin(tv_diff)
                    
                    # Append min difference value to the pass amount vector
                    discip['Pass_Amount'] = np.append(discip['Pass_Amount'], min_d)
                    
                # Perform the following commands if the point is not passing
                else:
                    
                    # Append 0.0 to the pass amount vector
                    discip['Pass_Amount'] = np.append(discip['Pass_Amount'], 0.0)
                    
                    # Calculate the NRMSD for the set of relevant output rules
                    nrmsd = np.sqrt(np.sum(np.square(tv_diff))/len(tv_diff))
                    
                    # Append the NRMSD value to the failure amount vector
                    discip['Fail_Amount'] = np.append(discip['Fail_Amount'], nrmsd)
            
            # Check if an eliminated key exists in the dictionary
            if 'eliminated' in discip:
                
                # Remove all of the pass?, fail amount, and pass amount data
                discip['pass?'] = []
                discip['Fail_Amount'] = np.array([], dtype=float)
                discip['Pass_Amount'] = np.array([], dtype=float)
                
                # Initial definitions to make code more readable
                start = outputStart(discip, 'pass?')
                tested_outs = discip['tested_outs']
                
                # Loop through each NEW design point in the output space
                for i in range(start, tested_outs.shape[0]):
                    
                    # Make a copy of the output rules
                    rules_copy = copy.deepcopy(output_rules)
                    
                    # Loop through each output rule
                    for j in range(0,len(output_rules)):
                        
                        # Loop through each output variable of the discipline
                        for k in discip['outs']:
                            
                            # Substitute output value for the variable in rule
                            rules_copy[j] = rules_copy[j].subs(k,\
                                tested_outs[i,discip['outs'].index(k)])
                            
                    # Append boolean value to the proper dictionary key
                    discip['pass?'].append(all(rules_copy))
                
                # Initial definitions to make code more readable
                start = outputStart(discip, 'Fail_Amount')
                pass_ = discip['pass?']
                
                # Loop through each NEW design point
                for i in range(start,len(pass_)):
                    
                    # Initialize a numpy vector the same length as the rules
                    tv_diff = np.zeros(len(output_rules))
                    
                    # Loop through each output rule
                    for rule in output_rules:
                        
                        # Determine normalized difference of point to rule's threshold
                        tv_diff[output_rules.index(rule)] = \
                            outputDiff(rule, i, discip)
                    
                    # Check if point is already passing
                    if pass_[i] == True:
                        
                        # Append 0.0 to the failure amount vector
                        discip['Fail_Amount'] = np.append(discip['Fail_Amount'], 0.0)
                        
                        # Calculate minimum difference for set of relevant output rules
                        min_d = np.nanmin(tv_diff)
                        
                        # Append min difference value to the pass amount vector
                        discip['Pass_Amount'] = np.append(discip['Pass_Amount'], min_d)
                        
                    # Perform the following commands if the point is not passing
                    else:
                        
                        # Append 0.0 to the pass amount vector
                        discip['Pass_Amount'] = np.append(discip['Pass_Amount'], 0.0)
                        
                        # Calculate the NRMSD for the set of relevant output rules
                        nrmsd = np.sqrt(np.sum(np.square(tv_diff))/len(tv_diff))
                        
                        # Append the NRMSD value to the failure amount vector
                        discip['Fail_Amount'] = np.append(discip['Fail_Amount'], nrmsd)
        
        # Return the update information for each discipline
        return self.D
    
    
    
