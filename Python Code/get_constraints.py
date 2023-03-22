"""
SUMMARY:
Returns a list of sympy rules that need to be met based on the the variables
passed to the function.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
FUNCTION
"""
def getConstraints(var,rules):
    """
    Description
    -----------
    Gathers a list of constraints/rules that must be considered according to
    the variables passed along
    
    Parameters
    ----------
    var : List of sympy symbols
        The particular variables for which rules/constraints must be gathered
    rules : List of class objects
        The current set of constraints/rules that each discipline must abide by
        when determining designs to test in the input space and if those tested
        designs produce passing outputs
    
    Returns
    -------
    temp_list : Nested list of sympy expressions
        A condensed list of rules that a discipline must consider according to
        input or output variables within their control
    """
    
    # Create an empty list
    rule_list = []
    
    # Loop through the full list of rules
    for i in range(0,len(rules)):
        
        # Determine every free symbol in the rule
        temp_rule = rules[i].breakup()
        
        # Create a temporary empty set of variables
        temp_set = set()
        
        # Loop through the temporary rule list
        for j in range(0,len(temp_rule)):
            for k in range(0,len(temp_rule[j])):
                
                # Add variable(s) to the set if it does not already exist there
                temp_set.update(temp_rule[j][k].free_symbols)
        
        # Check if any symbols in rule set do not match up with variables
        if all(item in var for item in temp_set):
            
            # Append rule to the temporary list
            rule_list.append(temp_rule)
    
    # Return the list of rules for discipline to consider
    return rule_list
