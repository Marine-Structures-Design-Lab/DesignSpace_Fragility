"""
SUMMARY:
Contains methods for checking the noneliminated space remaining in each
discipline, determining if a space reduction needs to be forced, and adjusting
the criteria for allowing a proposed space reduction based on the need to force
a reduction.

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
    
    def __init__(self, Discips):
        """
        Parameters
        ----------
        Discips : List of dictionaries
            Contains information specific to each discipline including space
            that has been eliminated thus far, a force reduction counter, and
            parameters for allowing proposed space reductions
        """
        self.d = Discips
        return
    
    
    def estimateSpace(self):
        """
        Description
        -----------
        Approximate the design space remaining in each discipline

        Parameters
        ----------
        None.
        
        Returns
        -------
        space_rem : List of floats
            Fraction of space remaining in each discipline
        """
        
        # Initialize array for tracking approximate space remaining
        space_rem = np.zeros(len(self.d))
        
        # Loop through each discipline
        for i in range(0,len(self.d)):
            
            # Calculate space remaining relative to space at beginning
            space_rem[i] = np.shape(self.d[i]['space_remaining'])[0]/ \
                self.d[i]['tp_actual']
            
        # Return approximate fraction of space remaining for each discipline
        return space_rem
    
    
    def forceReduction(self, space_rem, iters, iters_max, p):
        """
        Description
        -----------
        Determine and indicate if any disciplines should force a space
        reduction depending on the space that has been eliminated thus far
        compared to the project time remaining
        
        Parameters
        ----------
        space_rem : List of floats
            Fraction of space remaining in each discipline
        iters : Integer
            Time spent explorting the design space thus far
        iters_max : Integer
            Maximum time allowed for exploring design spaces
        p : Numpy vector
            Contains four user-defined parameters used in the exponential
            function defintion
        
        Returns
        -------
        self.d : List of dictionaries
            Contains various information specific to each discipline and now
            with a potentially updated force reduction indicator
        """
        
        # Loop through each discipline
        for i in range(0,len(self.d)):
            
            # Calculate minimum design space that should be eliminated thus far
            min_elim = max(calcExponential(iters/iters_max, p), 0.0)
            
            # Set the force reduction value to true or false depending on if
            # the minimum amount of space necessary has been eliminated
            if (1 - space_rem[i]) < min_elim:
                self.d[i]['force_reduction'][0] = True
            else:
                self.d[i]['force_reduction'][0] = False
            
        # Return updated list of dictionaries with new force reduction values
        return self.d
    
    
    def adjustCriteria(self):
        """
        Description
        -----------
        Cycles through the established criteria for allowing a space reduction
        that specifically pertain to the area of a discipline's design space
        being reduced and relaxes one criterion when a space reduction is being
        forced for the discipline
        
        Parameters
        ----------
        None.

        Returns
        -------
        self.d : List of dictionaries
            Contains information relevant to each discipline, now with a
            potentially relaxed criterion for allowing a space reduction
        """
        
        # Loop through each discipline
        for i in range(0,len(self.d)):
            
            # Continue if the discipline does not intend to force a reduction
            if self.d[i]['force_reduction'][0] == False: continue
            
            # Adjust criterion based on number of forced reductions thus far
            if self.d[i]['force_reduction'][1] % 4 == 0:
                self.d[i]['part_params']['cdf_crit'][0] = \
                    min(self.d[i]['part_params']['cdf_crit'][0] + \
                        self.d[i]['part_params']['cdf_crit'][1], 0.5)
            elif self.d[i]['force_reduction'][1] % 4 == 1:
                self.d[i]['part_params']['fail_crit'][0] = \
                    min(self.d[i]['part_params']['fail_crit'][0] + \
                        self.d[i]['part_params']['fail_crit'][1], 0.5)
            elif self.d[i]['force_reduction'][1] % 4 == 2:
                self.d[i]['part_params']['dist_crit'][0] = \
                    min(self.d[i]['part_params']['dist_crit'][0] + \
                        self.d[i]['part_params']['dist_crit'][1], 0.7)
            else:
                self.d[i]['part_params']['disc_crit'][0] = \
                    min(self.d[i]['part_params']['disc_crit'][0] + \
                        self.d[i]['part_params']['disc_crit'][1], 0.7)
            
            # Increase the discipline's forced reduction counter by 1
            self.d[i]['force_reduction'][1] += 1
        
        # Return list of dictionaries with updated critical criteria values
        return self.d
    