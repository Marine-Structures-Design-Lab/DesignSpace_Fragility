"""
SUMMARY:
Returns a list of sympy rules that need to be met based on the variables passed
to the function.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import sympy as sp
import numpy as np
from iteration_utilities import deepflatten



"""
FUNCTIONS
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
        The current set of constraints/rules that all disciplines must abide by
        when determining designs to test in the input space and if those tested
        designs produce passing outputs
    
    Returns
    -------
    rule_list : List of sympy expressions
        A condensed list of rules that a discipline must consider according to
        input or output variables within their control
    index_list : List of integers
        A corresponding list of indices that match the indices of the rules
        returned in the condensed list
    """
    
    # Create an empty list for rules
    rule_list = []
    
    # Create and empty list for rule indices
    index_list = []
    
    # Loop through the full list of rules
    for i in range(0,len(rules)):
        
        # Determine the variables of the rule
        temp_set = rules[i].free_symbols
        
        # Check if any symbols in rule set do not match up with variables
        if all(item in var for item in temp_set):
            
            # Append rule to the temporary rule list
            rule_list.append(rules[i])
            
            # Append index to the temporary index list
            index_list.append(i)
    
    # Return the lists of rules and indices for discipline to consider
    return rule_list, index_list


# Add inequalities from rules to dictionary within discipline if they do not already exist
def getInequalities(Discip,rules,dict_name):
    
    # Extract the inequality from each rule
    def extract_inequality(rule):
        
        # Check if rule is an Or or And relational
        if isinstance(rule, sp.Or) or isinstance(rule, sp.And):
            
            # Create a list for the length of the arguments
            arg_list = [None] * len(rule.args)
            
            # Loop through each argument of the rule
            for arg in rule.args:
                
                # Call function again for each argument
                arg_list[rule.args.index(arg)] = extract_inequality(arg)
            
            # Return the argument list
            return arg_list
        
        # Perform commands to extract the inequality
        else:
            
            # Return the rule (which should be an inequality)
            return rule
    
    # Initialize an inequality list
    ineq_list = []
    
    # Loop through each rule in the rule list
    for rule in rules:
        
        # Append inequalities to the inequality list
        ineq_list.append(extract_inequality(rule))
    
    # Flatten the inequality list to get rid of any possible nested lists
    ineq_list = list(deepflatten(ineq_list))
        
    # Loop through each inequality in the inequality list
    for ineq in ineq_list:
        
        # Do not add inequality as a dictionary key if it already exists
        if ineq in Discip[dict_name]: continue
    
        # Create a new key-value pair if the inequality does not exist as a key
        Discip[dict_name][ineq] = np.array([])
    
    # Return the updated discipline dictionary
    return Discip