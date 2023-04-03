"""
SUMMARY:
Produces a base method that merges all of the reduction requests into one list
and then subsequent methods to negotiate these potentially conflicting
reduction propositions into one collective, non-repeating, set

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""

"""
CLASS
"""
class mergeConstraints:
    
    def __init__(self,rules_new):
        self.rn = rules_new
        return
    
    # A method for evaluating how well other disciplines may perceive reduction
    ### requests of another discipline?
    
    # Different methods/strategies for how the design manager may want to
    ### merge all of the constraint requests into one cohesive bunch especially
    ### when there is conflict of propositions or same variable propositions
    
    # Returns the combined list of cohesive rules