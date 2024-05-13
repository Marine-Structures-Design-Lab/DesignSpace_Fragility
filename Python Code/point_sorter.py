"""
SUMMARY:
The main function moves information within each discipline of the design
problem over to an "eliminated" dictionary within the discipline's dictionary
while the secondary and tertiary functions help break down that process in a
series of steps to make the code more modular and easy to follow.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from create_key import createDict, createKey, createNumpy, createNumpy2
import numpy as np
import copy

"""
TERTIARY FUNCTIONS
"""
def checkPoints(discipline, rule, var, key):
    """
    Description
    -----------
    Check each point of the relevant array to see if they satisfy the new rule
    and collects the index of the point in a list if the point does not

    Parameters
    ----------
    discipline : Dictionary
        Contains all information on miscellaneous items pertaining to a
        particular discipline
    rule : Sympy relational or inequality
        Free-standing sympy inequality or inequalities nested with a sympy Or
        relational depending on the makeup of the rule
    var : Set of sympy symbols
        All free symbols that make up a particular rule
    key : String
        The name of the key indicating the relevant array to check

    Returns
    -------
    indices : List of integers
        All the array indices that do not satisfy the rule
    """
    
    # Initialize an empty list of indices for elimination
    indices = []
    
    # Loop through each point
    for j in range(np.shape(discipline[key])[0]):
        
        # Create a copy of the rule
        rule_copy = copy.deepcopy(rule)
        
        # Loop through each variable of the rule
        for symb in var:
            
            # Gather index of the symbol in the discipline's inputs
            index = discipline['ins'].index(symb)
            
            # Substitute index value from point to rule copy
            rule_copy = rule_copy.subs(discipline['ins'][index], \
                                       discipline[key][j,index])
            
        # Check if the tested input point does not meet the new rule
        if not rule_copy:
            
            # Append the index to the list of indices to eliminate
            indices.append(j)
            
    # Return a list of indices to eliminate
    return indices


def updatePoints(discipline, indices, keys):
    """
    Descripton
    ----------
    Moves information from the indices of the relevant keys to the "eliminated"
    dictionary within the discipline

    Parameters
    ----------
    discipline : Dictionary
        Contains all information on miscellaneous items pertaining to a
        particular discipline before moving more "eliminated" information
    indices : List of integers
        All the array indices that do not satisfy the rule
    keys : List of strings
        The name of all the key(s) needing to transfer information over to the
        nested "eliminated" dictionary

    Returns
    -------
    discipline : Dictionary
        Contains all information on miscellaneous items pertaining to a
        particular discipline after moving more "eliminated" information
    """
    
    # Loop through each key
    for key in keys:
        
        # Check if key is a list
        if isinstance(discipline[key], list):
            
            # Sort the indices in descending order
            indices.sort(reverse=True)
            
            # Remove the list element of each index and store in a new list
            moved_values = [discipline[key].pop(index) for index in indices]
            
            # Reverse the new list
            moved_values.reverse()
            
            # Resort the indices back in ascending order
            indices.sort()
            
            # Relocate the new list values to the eliminated key
            discipline['eliminated'][key].extend(moved_values)
        
        # Perform the following commands if the key is not a list
        else:
            
            # Take rows from array according to the indices
            moved_values = np.take(discipline[key], indices, axis=0)
            
            # Delete froms from array according to the indices
            discipline[key] = np.delete(discipline[key], indices, axis=0)
            
            # Add the moved values to the array
            discipline['eliminated'][key] = \
                np.concatenate((discipline['eliminated'][key], moved_values), \
                               axis=0)
    
    # Return the discipline having (potentially updated) eliminated values
    return discipline


"""
SECONDARY FUNCTIONS
"""
def elimDicts(discipline):
    """
    Description
    -----------
    Creates an "eliminated" dictionary within a discipline's dictionary along
    with relevant keys within the nested dictionary if none of these things
    already exist within the discipline

    Parameters
    ----------
    discipline : Dictionary
        All information pertaining to a discipline that may not have a nested
        "eliminated" dictionary

    Returns
    -------
    discipline : Dictionary
        All information pertaining to a discipline that absolutely has an
        "eliminated" dictionary along with relevant keys within that dictioanry
    """
    
    # Create a dictionary for eliminated information if it does not exist
    discipline = createDict('eliminated', discipline)
    
    # Determine keys to be apart of the nested eliminated dictionary
    keys_to_create = ['Fail_Amount',
                      'pass?',
                      'Pass_Amount',
                      'space_remaining',
                      'space_remaining_ind',
                      'tested_ins',
                      'tested_outs']
    
    # Loop through each eliminated key
    for key in keys_to_create:
        
        # Create an empty list for particular key
        if key in ['pass?', 'space_remaining_ind']:
            discipline['eliminated'] = createKey(key, discipline['eliminated'])
            
        # Create 2D numpy array for the particular keys
        elif key == 'tested_outs':
            discipline['eliminated'] = createNumpy2(\
                key, discipline['eliminated'], len(discipline['outs']))
            
        # Create a 2D numpy array for the particular keys
        elif key in ['space_remaining', 'tested_ins']:
            discipline['eliminated'] = createNumpy2(\
                key, discipline['eliminated'], len(discipline['ins']))
        
        # Create a 1D numpy vector for the remaining key(s)
        else:
            discipline['eliminated'] = \
                createNumpy(key, discipline['eliminated'])
    
    # Return the discipline with the (potentially new) eliminated keys
    return discipline


def testPoints(discipline, var, rule):
    """
    Description
    -----------
    Cycles through the tested input points and space remaining points within a
    discipline and moves values along with accompanying information to the
    nested "eliminated" dictionary based on the new input rule(s)

    Parameters
    ----------
    discipline : Dictionary
        Contains all information on miscellaneous items pertaining to a
        particular discipline
    var : Set of sympy symbols
        All free symbols that make up a particular rule
    rule : Sympy relational or inequality
        Free-standing sympy inequality or inequalities nested with a sympy Or
        relational depending on the makeup of the rule

    Returns
    -------
    discipline : Dictionary
        Contains all information on miscellaneous items pertaining to a
        particular discipline with relevant information moved to the nested
        "eliminated" dictionary of that discipline depending on the rule
    """
    
    # Gather indices of tested input points that do not meet rule
    tp_elim = checkPoints(discipline, rule, var, 'tested_ins')
    
    # Move indices with failing input information to eliminated dictionary
    discipline = updatePoints(discipline, tp_elim,\
                     ['tested_ins', 'tested_outs', 'Fail_Amount', \
                      'Pass_Amount', 'pass?'])
    
    # Gather indices of space remaining points that do not meet rule
    sr_elim = checkPoints(discipline, rule, var, 'space_remaining')
    
    # Move indices with failing space remaining values to eliminated dictionary
    discipline = updatePoints(discipline, sr_elim, ['space_remaining', 
                                                    'space_remaining_ind'])
    
    # Return the discipline with the (potentially updated) eliminated keys
    return discipline


"""
MAIN FUNCTION
"""
def sortPoints(Discips, irules_new):
    """
    Description
    -----------
    Move previously established values from the necessary discipline keys to an
    eliminated key within the discipline based on the new input rule(s) being
    added

    Parameters
    ----------
    Discips : List of dictionaries
        Each dictionary contains information specific to a discipline on
        previously tested input values, corresponding output values, and other
        items
    irules_new : List of sympy relationals
        All the new input rules that are being added to the cumulative input
        rule set based on the previous round of space reductions

    Returns
    -------
    Discips : List of dictionaries
        The same list of dictionaries that now has information moved to an
        "eliminated" key within the dictionary based on what information was
        made obsolete by the new set of input rules
    """
    
    # Loop through each new input rule
    for rule in irules_new:
        
        # Determine the variables of the rule
        var = rule.free_symbols
        
        # Loop through each discipline
        for i in range(0,len(Discips)):
            
            # Continue to next discipline if current one not impacted by rule
            if not all(item in Discips[i]['ins'] for item in var): continue
            
            # Create dictionaries for eliminated info if they do not exist
            Discips[i] = elimDicts(Discips[i])
            
            # Move proper points and other information to eliminated dictionary
            Discips[i] = testPoints(Discips[i], var, rule)
    
    # Return the updated list of dictionaries with changes for each discipline
    return Discips

