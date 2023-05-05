"""
SUMMARY:


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
    
    # Loop through each inequality
    for ineq in Discip[dict_key1]:
        
        # Gather free symbols of the inequality
        symbs = ineq.free_symbols
        
        # Loop through each NEW design point
        for i in range(outputStart(Discip[dict_key1],ineq),\
                       np.shape(Discip[dict_key2])[0]):
            
            # Gather left-hand side of the inequality
            lhs = ineq.lhs
            
            # Loop through each free symbol
            for symb in symbs:
                
                # Get index in the discipline of the free symbol
                ind = Discip[dict_key3].index(symb)
                
                # Substitute point value into free symbol of lhs of inequality
                lhs = lhs.subs(symb,Discip[dict_key2][i,ind])
                
            # Append design point value to numpy array of inequality
            Discip[dict_key1][ineq] = np.append(Discip[dict_key1][ineq],lhs)
                
    # Return updated discipline with new values for each inequality rule
    return Discip[dict_key1]