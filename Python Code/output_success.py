"""
SUMMARY:
Takes the calculated output values and assesses whether or not they meet the
current set of constraints/rules.  If they do not meet the rules, then it
provides different methods for assessing the extent to which this failure
occurs.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from output_start import outputStart
from scipy.optimize import minimize
import numpy as np
import sympy as sp
import copy
import math

"""
CLASS
"""
class checkOutput:
    
    def __init__(self,discip,output_rules):
        """
        Parameters
        ----------
        discip : Dictionary
            The complete dictionary of sympy inputs, sympy outputs, sympy
            expressions, execution time, tested input points, calculated
            output points, and an empty or partially filled boolean list that
            checks whether output rules/constraints are passed
        output_rules : List of symbolic inequalities
            A condensed list of rules that will dictate whether the output
            values of the particular discipline passed to this method pass or
            fail
        """
        self.d = discip
        self.outr = output_rules
        return
    
    def basicCheck(self):
        """
        Description
        -----------
        Checks whether the output values pass or fail the current set of output
        rules and adds this information to the discipline's dictionary of
        information
        
        Parameters
        ----------
        None.

        Returns
        -------
        self.d : Dictionary
            The complete dictionary of sympy inputs, sympy outputs, sympy
            expressions, execution time, tested input points, calculated
            output points, and a completely filled boolean list that checks
            whether output rules/constraints are passed
        """
        
        # Loop through each NEW design point in the output space
        for i in range(outputStart(self.d,'pass?'),\
                       np.shape(self.d['tested_outs'])[0]):
            
            # Make a copy of the output rules
            rules_copy = copy.deepcopy(self.outr)
            
            # Loop through each output rule
            for j in range(0,len(self.outr)):
                
                # Loop through each output variable of the discipline
                for k in self.d['outs']:
                    
                    # Substitute output value for the variable in rule
                    rules_copy[j] = rules_copy[j].subs(k,\
                            self.d['tested_outs'][i,self.d['outs'].index(k)])
                    
            # Append boolean value to the proper dictionary key
            self.d['pass?'].append(all(rules_copy))
            
        # Return new dictionary with boolean pass? values
        return self.d
    
    
    # Normalized RMSD of calculated output from constraints
    def rmsFail(self):
        
        # Get difference in calculated output to proper constraint
        def get_output_diff(rule,i):
            
            # Check if rule is an Or or And relational
            if isinstance(rule, sp.Or) or isinstance(rule, sp.And):
                
                # Create a numpy zero vector for the length of the arguments
                diff_vector = np.zeros(len(rule.args))
                
                # Loop through each argument of the rule
                for arg in rule.args:
                    
                    # Loop back through the function and assign the rule
                    # difference to the proper index in the vector
                    diff_vector[rule.args.index(arg)] = get_output_diff(arg,i)
                    
                # Set base rule tracker to True
                base_rule = True
                
                # Loop through each argument of the rule
                for arg in rule.args:
                    
                    # Check if argument is an Or or And relational
                    if not isinstance(arg,sp.Or) and\
                        not isinstance(arg,sp.And):
                        
                        # Continue to check next argument of rule
                        continue
                    
                    # Perform commands if argument is an Or or And relational
                    else:
                        
                        # Change base rule tracker to true
                        base_rule = False
                        
                        # Stop checking arguments of the rule
                        break
                
                # Check that no arguments of rule are an Or or And relational
                if base_rule:
                    
                    # Return the minimum of the difference vector for rule
                    return min(diff_vector)
                
                # Peform the following commands if at least one argument is an
                # Or or And relational
                else:
                    
                    # Return the minimum of the difference vector for Or rule
                    if isinstance(rule, sp.Or): return min(diff_vector)
                    
                    # Return the maximum of the difference vector for And rule
                    else: return max(diff_vector)
                
            # Perform commands to find the difference of actual expression
            else:
                
                # Gather left- and right-hand side of inequality
                lhs = rule.lhs
                rhs = rule.rhs
                
                # Loop through each output variable of the discipline
                for var in self.d['outs']:
                    
                    # Gather index of the symbol in the discipline's outputs
                    index = self.d['outs'].index(var)
                    
                    # Substitute output value of variable into lhs inequality
                    lhs = lhs.subs(var,self.d['tested_outs'][i,index])
                
                # Assign distance to propper index of argument vector
                diff = abs(lhs - rhs)
                
                # Return the difference of the output from the rule
                return diff
        
        # Loop through each NEW design point in the output space
        for i in range(outputStart(self.d,'Fail_Amount'),\
                       np.shape(self.d['tested_outs'])[0]):
            
            # Check if output point is already passing
            if self.d['pass?'][i] == True:
                
                self.d['Fail_Amount'].append(0.0)
                
            # Peform following commands if the output point is not passing
            else:
                
                # Create a numpy vector the same length as the output rules
                true_val_diff = np.zeros(len(self.outr))
                
                # Loop through each output rule
                for rule in self.outr:
                    
                    # Get difference between calculated value and rule
                    true_val_diff[self.outr.index(rule)] = \
                        get_output_diff(rule,i)
                
                # Calculate the RMSD for the set of relevant output rules
                ### Need to normalize this eventually!!!
                rmsd = math.sqrt(sum(np.square(true_val_diff))/len(true_val_diff))
                
                # Append the RMSD value to the fail amount list
                self.d['Fail_Amount'].append(rmsd)
        
        # Return the discipline's dictionary with updated failure amount values
        return self.d
    
    
    # Distance of point from passing constraints
    def failAmount(self):
        
        # Loop through each NEW design point in the output space
        for i in range(outputStart(self.d,'Fail_Amount'),\
                       np.shape(self.d['tested_outs'])[0]):
            
            # Check if output point is already passing
            if self.d['pass?'][i] == True:
                
                self.d['Fail_Amount'].append(0.0)
                
            # Peform following commands if the output point is not passing
            else:
                
                i
                
        return self.d
