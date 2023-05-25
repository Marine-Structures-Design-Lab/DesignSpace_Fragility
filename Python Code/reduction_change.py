"""
SUMMARY:


CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from exponential_reduction import calcExponential
import numpy as np



"""
CLASS
"""
class changeReduction:
    
    # Initialize the class
    def __init__(self,Discips):
        self.d = Discips
        return
    
    # Estimate space remaining for each discipline
    def estimateSpace(self, tp_actual):
        
        # Initialize array for tracking approximate space remaining
        space_rem = np.zeros(len(self.d))
        
        # Loop through each discipline
        for i in range(0,len(self.d)):
            
            # Calculate decimal for space remaining
            space_rem[i] = np.shape(self.d[i]['space_remaining'])[0] / tp_actual
            
        # Return approximate space remaining for each discipline
        return space_rem
    
    
    # Determine if any disciplines should force a space reduction
    def forceReduction(self, space_rem, iters, iters_max, p):
        
        # Loop through each discipline
        for i in range(0,len(self.d)):
            
            # Calculate minimum amount of design space that should be eliminated thus far
            min_elim = max(calcExponential(iters/iters_max,p),0.0)
            
            # Set the force reduction value to true or false depending on the
            # amount of space that has been eliminated thus far
            if (1 - space_rem[i]) < min_elim:
                self.d[i]['force_reduction'][0] = False # Change this back to True later
            else:
                self.d[i]['force_reduction'][0] = False
            
        # Return updated list of dictionaries with new force reduction values
        return self.d
    
    
    def adjustCriteria(self):
        ### MIGHT NEED TO CAP SOME OF THESE OFF
        
        # Loop through each discipline
        for i in range(0,len(self.d)):
            
            # Continue if the discipline does not intend to force a reduction
            if self.d[i]['force_reduction'][0] == False: continue
            
            # Adjust criterion based on number of forced reductions thus far
            if self.d[i]['force_reduction'][1] % 4 == 0:
                self.d[i]['part_params']['cdf_crit'] += 0.1
            elif self.d[i]['force_reduction'][1] % 4 == 1:
                self.d[i]['part_params']['fail_crit'] += 0.05
            elif self.d[i]['force_reduction'][1] % 4 == 2:
                self.d[i]['part_params']['dist_crit'] += 0.1
            else:
                self.d[i]['part_params']['disc_crit'] += 0.1
            
            # THIS MAY GO IN ITS OWN METHOD
            # Increase the discipline's forced reduction counter by 1
            self.d[i]['force_reduction'][1] += 1
        
        # Return list of dictionaries with updated critical criteria values
        return self.d
    