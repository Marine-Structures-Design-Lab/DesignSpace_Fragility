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





"""
CLASS
"""
class checkFragility:
    
    def __init__(self, risk):
        self.risk = risk
        return
    
    
    # Return a true or false boolean value if fragile or not
    def basicCheck(self, iters, iters_max, p, shift):
        
        # Establish exponential threshold for declaring a design space fragile after a space reduction
        threshold = max(calcExponential(iters/iters_max, p), 0.0) + shift
        
        # Initialize an empty dictionary for tracking max risk values
        max_risk = {}
        
        # Loop through each rule combination
        for rule, lis in self.risk.items():
            
            # Initialize a max risk value to a large negative value
            max_risk[rule] = {"value": -1000, "fragile": False}
            
            # Loop through each discipline's regret and windfall values
            for dic in lis:
                
                # Subtract windfall from regret
                net_risk = dic['regret'] - dic['windfall']
                
                # Update max risk value
                max_risk[rule]["value"] = max(max_risk[rule]["value"], net_risk)
            
            # Set boolean value depending on max risk value
            if max_risk[rule]["value"] > threshold: max_risk[rule]["fragile"] = True
            else: max_risk[rule]["fragile"] = False
        
        
        # This is temporary!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        fragile = False
        
        return fragile, max_risk
    
    
    def newRules(self, max_risk):
        
        # Initialize an empty list of rule combinations
        rule_combos = []
        
        # Loop through each rule combination
        for rule, lis in self.risk.items():
            rule
            
            # Add rule combination to list if it is not fragile
            #if lis
            
            
            
            
        
        
        
        
        return 
    
    
    def newBanned(self):
        
        # Loop through each rule combination and add individual rule(s) to
        # banned set if it is Fraile
        
        
        return
    
    
    
    # Function for adding rule to a temporary banned rule list
    
