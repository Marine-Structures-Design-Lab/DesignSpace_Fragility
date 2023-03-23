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
from rule_check import ruleCheck
import numpy as np
import copy

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
                    
                    # Loop through each part of the rule
                    for l in range(0,len(rules_copy[j])):
                        for m in range(0,len(rules_copy[j][l])):
                            
                            # Substitute output value for the variable in rule
                            rules_copy[j][l][m] = rules_copy[j][l][m].subs(k,\
                                    self.d['tested_outs'][i,self.d['outs']\
                                                          .index(k)])
            
            # Check whether all output values meet necessary rules
            all_good = ruleCheck(rules_copy)
            
            # Append boolean value to the proper dictionary key
            self.d['pass?'].append(all_good)
            
        # Return new dictionary with boolean pass? values
        return self.d