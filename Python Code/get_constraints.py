"""
SUMMARY:
Contains functions for gathering information from the set of rules of interest
to the discipline.  This information may involve gathering the relevant rules
as a whole or the individual base inequalities/arguments of which the relevant
rules are comprised.

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
SECONDARY FUNCTION
"""
def extractInequality(rule):
    """
    Description
    -----------
    A recursive function that calls itself until the rule being passed to
    it is a sympy inequality rather than an And or Or relational so that
    the base inequality can be returned regardless of how nested the
    relationals are

    Parameters
    ----------
    rule : Sympy relational/inequality
        Either a sympy And or Or relational or a sympy inequality depending
        on how far the function has gotten within the (potentially nested)
        rule

    Returns
    -------
    arg_list or rule : List of sympy inequalities or single inequality
        Returns either a (potentially nested) list of inequalities or a
        single inequality depending on if the rule is a sympy relational or
        a sympy inequality
    """
    
    # Check if rule is an Or or And relational
    if isinstance(rule, sp.Or) or isinstance(rule, sp.And):
        
        # Create an empty list for the length of the arguments
        arg_list = [None] * len(rule.args)
        
        # Loop through each argument of the rule
        for arg in rule.args:
            
            # Call function again for each argument
            arg_list[rule.args.index(arg)] = extractInequality(arg)
        
        # Return the argument list
        return arg_list
    
    # Perform commands to extract the inequality
    else:
        
        # Return the rule (which should be an inequality)
        return rule


"""
MAIN FUNCTIONS
"""
def getConstraints(var, rules):
    """
    Description
    -----------
    Gathers a list of constraints/rules that must be considered according to
    the variables passed along
    
    Parameters
    ----------
    var : List of sympy symbols
        The particular variables for which rules/constraints must be gathered
    rules : List of sympy relationals
        The current set of constraints/rules by which all disciplines must
        abide
    
    Returns
    -------
    rule_list : List of sympy expressions
        A condensed list of relevant rules to the discipline
    """
    
    # Create an empty list for rules
    rule_list = []
    
    # Loop through the full list of rules
    for i in range(0,len(rules)):
        
        # Determine the variables of the rule
        temp_set = rules[i].free_symbols
        
        # Check if all variables in the temporary set are within variable list
        if all(item in var for item in temp_set):
            
            # Append rule to the temporary rule list
            rule_list.append(rules[i])
    
    # Return the lists of rules for consideration
    return rule_list


def getInequalities(Discip,rules,dict_name):
    """
    Description
    -----------
    Gathers base inequalities from the provided list of rules and then uses
    them as keys for a nested dictionary within the provided key of the
    discipline's dictionary
    
    Parameters
    ----------
    Discip : Dictionary
        Contains various key-value pairs associated with the current details of
        the particular discipline
    rules : List of sympy relationals
        A condensed list of relevant rules to the discipline
    dict_name : String
        Name of the discipline's key in which the nested dictionary of
        inequalities should reside

    Returns
    -------
    Discip : Dictionary
        The same dictionary now updated with any new inequalities within the
        nested dictionary
    """
    
    # Initialize an inequality list
    ineq_list = []
    
    # Loop through each rule in the rule list
    for rule in rules:
        
        # Append inequalities to the inequality list
        ineq_list.append(extractInequality(rule))
    
    # Flatten the inequality list to get rid of any possible nested lists
    ineq_list = list(deepflatten(ineq_list))
        
    # Loop through each inequality in the inequality list
    for ineq in ineq_list:
        
        # Do not add inequality as a dictionary key if it already exists
        if ineq in Discip[dict_name]: continue
    
        # Create a new key-value pair if the inequality does not exist as a key
        Discip[dict_name][ineq] = np.array([])
    
    # Return the complete, newly updated, discipline dictionary
    return Discip
