"""
SUMMARY:
Takes the calculated output values and assesses whether or not they meet the
current set of constraints/rules (should there be a difference between the
current set of rules as opposed to the original set of rules?).  If they do not
meet the rules, then it provides different methods for assessing the extent to
which this failure occurs.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from output_start import outputStart
import numpy as np
import copy

"""
CLASS
"""
class checkOutput:
    
    def __init__(self,discip,output_rules):
        self.d = discip
        self.outr = output_rules
        return
    
    # Only check whether the NEW output points pass or fail
    def basicCheck(self):
        
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
            
            # Create boolean variable for tracking - TURN THIS INTO A FUNCTION CALL
            all_good = True
            
            # Loop through each rule
            for j in range(0,len(rules_copy)):
                
                # Create boolean variable for tracking
                good = False
                
                # Loop through each "or" list of rule
                for k in range(0,len(rules_copy[j])):
                    
                    # Check if all rules in "and" list are true
                    if all(rules_copy[j][k]):
                        good = True
                        break
                
                # Perform actions if any of the "or" list are not true
                if (not good):
                    all_good = False
                    break
            
            # Append boolean value to the proper dictionary key
            self.d['pass?'].append(all_good)
        
        # Return new dictionary with boolean pass? values
        return self.d