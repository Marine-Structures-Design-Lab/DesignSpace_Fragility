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
    
    # Determine the normalized rmsd of output points that fail from each rule
    def rmsFail(self):
        
        # Get difference in calculated outputs to failing rule
        def get_output_diff(rule,i):
            
            # Check if rule is an Or or And relational
            if isinstance(rule, sp.Or) or isinstance(rule, sp.And):
                
                # Create a numpy zero array for the length of the arguments
                diff_vector = np.zeros(len(rule.args))
                
                # Loop through each argument of the rule
                for arg in rule.args:
                    
                    # Call the function again and assign its value to vector
                    diff_vector[rule.args.index(arg)] = get_output_diff(arg,i)
                
                # Return min of difference array for each point of Or rule
                if isinstance(rule, sp.Or):
                    return np.nanmin(diff_vector)
                
                # Return max of difference array for each point of And rule
                else: 
                    return np.nanmax(diff_vector)
            
            # Perform following commands if rule is not an Or or And relational
            else:
                
                # Make a copy of the inequality
                rule_copy = copy.deepcopy(rule)
                
                # Gather free symbols of the inequality
                symbs = rule.free_symbols
                
                # Loop through each free symbol
                for symb in symbs:
                    
                    # Get index in the discipline's outputs of the free symbol
                    ind = self.d['outs'].index(symb)
                    
                    # Substitute output value into free symbol of rule copy
                    rule_copy=rule_copy.subs(symb,self.d['tested_outs'][i,ind])
                
                # Check if the rule copy is true
                if rule_copy:
                    
                    # Return a not a number value
                    return np.nan
                
                # Perform the following commands if the rule copy is not true
                else:
                    
                    # Determine difference between lhs and rhs of rule
                    diff = abs(self.d['out_ineqs'][rule][i] - rule.rhs)
                    
                    # Check if normalized difference is complex
                    if np.ptp(self.d['out_ineqs'][rule]) == 0:
                        
                        # Return the non-normalized difference
                        return diff
                    
                    # Normalize difference w/range of all values seen by rule
                    ndiff = diff / np.ptp(self.d['out_ineqs'][rule])
                        
                    # Return normalized absolute difference of lhs and rhs
                    return ndiff
        
        # Loop through each NEW design point
        for i in range(outputStart(self.d,'Fail_Amount'),len(self.d['pass?'])):
            
            # Check if point is already passing
            if self.d['pass?'][i] == True:
                
                # Append 0 to the failure amount vector
                self.d['Fail_Amount'] = np.append(self.d['Fail_Amount'],0.0)
            
            # Perform the following commands if the point is not passing
            else:
                
                # Initialize a numpy vector the same length as the rules
                true_val_diff = np.zeros(len(self.outr))
                
                # Loop through each output rule
                for rule in self.outr:
                    
                    # Determine the normalized difference that point fails rule
                    true_val_diff[self.outr.index(rule)]=get_output_diff(rule,i)
                
                # Calculate the NRMSD for the set of relevant output rules
                nrmsd = np.sqrt(np.sum(np.square(true_val_diff))/len(true_val_diff))
                
                # Append the NRMSD value to the failure amount vector
                self.d['Fail_Amount'] = np.append(self.d['Fail_Amount'],nrmsd)
                
        # Return updated dictionary with normalized failure amounts
        return self.d
    


