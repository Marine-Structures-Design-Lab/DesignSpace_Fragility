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
import sympy as sp

"""
CLASS
"""
class mergeConstraints:
    
    def __init__(self,rules_new):
        self.rn = rules_new
        return
    
    # Minimum merge method - PROBABLY NEED TO ADJUST THIS AS WAS DONE IN EXPLORATION_CHECK!!
    def minMerge(self):
        
        # Convert all rules to Or
        rules = [rule if rule.func == sp.Or else sp.Or(rule) for rule in self.rn]
    
        # Initialize list of non-redundant rules
        non_redundant_rules = []
    
        for i, rule1 in enumerate(rules):
            redundant = False
            for j, rule2 in enumerate(rules):
                if i != j:
                    # Check if rule1 is implied by rule2
                    implies = sp.simplify(sp.Implies(rule2, rule1))
                    if implies is True:
                        redundant = True
                        break
    
            if not redundant:
                non_redundant_rules.append(rule1)
    
        return non_redundant_rules
    
    # Save dominance for the fragility framework???
    
    
    
    
    
    
    
    
    
    
    
    # No dominance until at least 50% of spaces have been eliminated
    ### One option is to have the requests pop up with stats and I decide
    ### Or program decides with stats
    ### Stats: How many disciplines are requesting what vs. the other
    ### How each side would be affected by the other discipline's proposal
    
    
    ### Could call a getInput method here...but not have it be a uniform method
    ### Could also do this for the fragility or other methods that may need to
    ### search points further
    
    
    