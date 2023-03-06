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

"""
FUNCTION
"""
def getConstraints(var,set_rules):
    '''
    Description
    -----------
    Takes strings of all the design rules and converts them into arithmetic
    equations so that sympy can identify the list of rules that a discipline
    needs to consider based on the "free symbols"
    
    Parameters
    ----------
    var : Sympy symbols
        Variables that the discipline wants to be considered when determining
        what rules/constraints they are impacted by
    set_rules : Set containing strings
        The set of constraints/rules that each discipline must abide by when
        determining designs to test in the input space and if those tested
        designs produce passing outputs

    Returns
    -------
    temp_list : TYPE
        The condensed list of rules/constraints that the particular discipline
        needs to satisfy
    '''
    
    # Convert set of rules to a list
    rules_list = list(set_rules)
    
    # Create a temporary empty list
    temp_list = []
    
    # Loop through the list of rules
    for i in range(0,len(rules_list)):
        
        # Turn the rule consisting of a string into an expression for sympy
        temp_rule = sp.sympify(rules_list[i])
        
        # Determine every free symbol in the expression
        temp_exp = temp_rule.free_symbols
        
        # Check if any symbols in set of the rule do not match up with variables
        if all(item in var for item in temp_exp):
            
            # Append rule to the temporary list
            temp_list.append(temp_rule)
    
    # Return the list of rules for discipline to consider
    return temp_list
