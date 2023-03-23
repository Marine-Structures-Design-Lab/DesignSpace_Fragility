# -*- coding: utf-8 -*-
"""
SUMMARY:
Checks the nested list of rules/constraints passed to the function consisting
of "and" and "or" rules and methodically checks their boolean values to
eventually determine whether the design point as a whole passes or fails all of
the current set of relevant rules

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
FUNCTION
"""
def ruleCheck(rules_copy):
    """
    Description
    -----------
    Determine whether all of the rules/constraints are met for the particular
    set of rules

    Parameters
    ----------
    rules_copy : Boolean
        Condensed list of previous sympy inequalities that have had values
        substituted for all variables to the point that each item is now only
        a true or false boolean value

    Returns
    -------
    all_good : Boolean
        Tracks if all the necessary constraints are met for the particular set
        of rules consisted of "or" and "and" statements based on their
        formatting within the nested list of the copy of rules

    """
    
    # Create boolean variable for tracking
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
    
    # Return whether or not the rules/constraints are met
    return all_good