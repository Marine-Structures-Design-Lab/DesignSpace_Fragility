"""
SUMMARY:


CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from create_key import createDict, createNumpy, createNumpy2, createKey
import numpy as np
import copy

"""
FUNCTIONS
"""
# Create and sort all eliminated points into a dictionary of eliminated stuff
def sortPoints(Discips,irules_new):
    
    # Loop through each new input rule
    for rule in irules_new:
        
        # Determine the variables of the rule
        var = rule.free_symbols
        
        # Loop through each discipline
        for i in range(0,len(Discips)):
            
            # Continue to next discipline if current one not impacted by rule
            if not all(item in Discips[i]['ins'] for item in var): continue
            
            # Create a dictionary for eliminated point info if it does not exist
            Discips[i] = createDict('eliminated',Discips[i])
            
            # Create relevant lists/arrays in the 'eliminated' nested dictionary
            Discips[i]['eliminated'] = createNumpy('Fail_Amount',Discips[i]['eliminated'])
            Discips[i]['eliminated'] = createKey('pass?',Discips[i]['eliminated'])
            Discips[i]['eliminated'] = createNumpy2('space_remaining',Discips[i]['eliminated'],len(Discips[i]['ins']))
            Discips[i]['eliminated'] = createNumpy2('tested_ins',Discips[i]['eliminated'],len(Discips[i]['ins']))
            Discips[i]['eliminated'] = createNumpy2('tested_outs',Discips[i]['eliminated'],len(Discips[i]['outs']))
            
            # Convert set of variables to a list
            var = list(var)
            
            # Create list that tracks tested input indices to eliminate
            tp_elim = []
            
            # Loop through each available input point of discipline
            for j in range(0,np.shape(Discips[i]['tested_ins'])[0]):
                
                # Create a copy of the rule
                rule_copy = copy.deepcopy(rule)
                
                # Loop through each variable of the rule
                for symb in var:
                    
                    # Gather index of the symbol in the discipline's inputs
                    index = Discips[i]['ins'].index(symb)
                    
                    # Substitute index value from point to rule copy
                    rule_copy = rule_copy.subs\
                        (Discips[i]['ins'][index],Discips[i]['tested_ins'][j,index])
                
                # Check if the tested input point does not meet the new rule
                if not rule_copy:
                    
                    # Append index to the list of indices to eliminate
                    tp_elim.append(j)
            
            # Relocate tested input points to the eliminated key
            rows_to_move = np.take(Discips[i]['tested_ins'], tp_elim, axis=0)
            Discips[i]['tested_ins'] = np.delete(Discips[i]['tested_ins'], tp_elim, axis=0)
            Discips[i]['eliminated']['tested_ins'] = np.vstack((Discips[i]['eliminated']['tested_ins'], rows_to_move))
            
            # Relocate tested output points to the eliminated key
            rows_to_move = np.take(Discips[i]['tested_outs'], tp_elim, axis=0)
            Discips[i]['tested_outs'] = np.delete(Discips[i]['tested_outs'], tp_elim, axis=0)
            Discips[i]['eliminated']['tested_outs'] = np.vstack((Discips[i]['eliminated']['tested_outs'], rows_to_move))
            
            # Relocate "Fail_Amount" values to the eliminated key
            moved_values = np.take(Discips[i]['Fail_Amount'], tp_elim)
            Discips[i]['Fail_Amount'] = np.delete(Discips[i]['Fail_Amount'], tp_elim)
            Discips[i]['eliminated']['Fail_Amount'] = np.concatenate((Discips[i]['eliminated']['Fail_Amount'], moved_values))
            
            # Relocate "pass?" values to the eliminated key
            tp_elim.sort(reverse=True)
            moved_values = [Discips[i]['pass?'].pop(index) for index in tp_elim]
            moved_values.reverse()
            Discips[i]['eliminated']['pass?'].extend(moved_values)
            
            # Create list that tracks space remaining indices to eliminate
            sr_elim = []
            
            # Loop through each space remaining point of discipline
            for j in range(0,np.shape(Discips[i]['space_remaining'])[0]):
                
                # Create a new copy of the rule
                rule_copy = copy.deepcopy(rule)
                
                # Loop through each variable of the rule
                for symb in var:
                    
                    # Gather index of the symbol in the discipline's inputs
                    index = Discips[i]['ins'].index(symb)
                    
                    # Substitute index value from point to rule copy
                    rule_copy = rule_copy.subs\
                        (Discips[i]['ins'][index],Discips[i]['space_remaining'][j,index])
                
                # Check if the space remaining point does not meet the new rule
                if not rule_copy:
                    
                    # Append index to the list of indices to eliminate
                    sr_elim.append(j)
            
            # Relocate space remaining values to the eliminated key
            rows_to_move = np.take(Discips[i]['space_remaining'], sr_elim, axis=0)
            Discips[i]['space_remaining'] = np.delete(Discips[i]['space_remaining'], sr_elim, axis=0)
            Discips[i]['eliminated']['space_remaining'] = np.vstack((Discips[i]['eliminated']['space_remaining'], rows_to_move))
    
    # Return the updated list of dictionaries with changes for each discipline
    return Discips