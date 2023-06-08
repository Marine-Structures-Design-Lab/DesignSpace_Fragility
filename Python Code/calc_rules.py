"""
SUMMARY:
Calculates the left-hand side of input or output rules using the input or
output values at the particular point in the design process so that failure
amounts with respect to the rules can be normalized later

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import numpy as np
from output_start import outputStart

"""
FUNCTION
"""
def calcRules(Discip,dict_key1,dict_key2,dict_key3):
    """
    Description
    -----------
    Works within a discipline's nested dictionary to calculate and populate the
    keys associated with each relevant rule with values for the left-hand side
    of those rules based on the input or output values of the discipline

    Parameters
    ----------
    Discip : Dictionary
        Contains various key-value pairs associated with the current details of
        the particular discipline
    dict_key1 : String
        Discipline's dictionary key where nested dictionary of rule and
        calculated rule values are to be located
    dict_key2 : String
        Discipline's dictionary key from where variable values for calculating
        the rule values are to be gathered
    dict_key3 : String
        Discipline's dictionary key where the variables pertaining to the rules
        are located

    Returns
    -------
    Discip[dict_key1] : Dictionary
        Updated nested dictionary withtin the discipline that is now updated
        with new values for its nested dictionary containing keys for the
        current rules and values for the left-hand side of those rules
    """
    
    # Loop through each inequality
    for ineq in Discip.get(dict_key1, {}):
        
        # Gather free symbols of the inequality
        symbs = ineq.free_symbols
        
        # Variable definitions to improve readability
        start = outputStart(Discip[dict_key1], ineq)
        value_array = Discip.get(dict_key2, np.array([]))
        
        # Loop through each NEW design point
        for i in range(start, value_array.shape[0]):
            
            # Gather left-hand side of the inequality
            lhs = ineq.lhs
            
            # Loop through each free symbol
            for symb in symbs:
                
                # Get index in the discipline of the free symbol
                ind = Discip.get(dict_key3, []).index(symb)
                
                # Substitute point value into free symbol of lhs of inequality
                lhs = lhs.subs(symb, value_array[i, ind])
                
            # Append design point value to numpy array of inequality
            Discip[dict_key1][ineq] = \
                np.append(Discip[dict_key1].get(ineq, np.array([])), lhs)
                
    # Return updated discipline with new values for each inequality rule
    return Discip[dict_key1]