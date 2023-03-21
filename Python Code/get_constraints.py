"""
SUMMARY:
Converts the string of rules into sympy inequalities and returns the current
list of these inequalities that need to be met as it pertains to rules
involving independent and shared variables of a particular discipline.

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
FUNCTION
"""
# Return the rules list that the discipline must consider
### depending on the input or output variable provided
def getConstraints(var,rules):
    
    # Create a temporary empty list
    temp_list = []
    
    # Loop through the list of rules
    for i in range(0,len(rules)):
        
        # Determine every free symbol in the rule
        temp_rule = rules[i].breakup()
        
        # Create a temporary set of variables
        temp_set = set()
        
        # Loop through the temporary rule list
        for j in range(0,len(temp_rule)):
            for k in range(0,len(temp_rule[j])):
                
                # Add variable(s) to the set if it does not already exist there
                temp_set.update(temp_rule[j][k].free_symbols)
        
        # Check if any symbols in rule set do not match up with variables
        if all(item in var for item in temp_set):
            
            # Append rule to the temporary list
            temp_list.append(temp_rule)
    
    # Return the list of rules for discipline to consider
    return temp_list
