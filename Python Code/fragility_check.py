"""
SUMMARY:


CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""




"""
CLASS
"""
class checkFragility:
    
    def __init__(self, risk):
        self.risk = risk
        return
    
    
    # Return a true or false boolean value if fragile or not
    def basicCheck(self, iters, iters_max):
        
        # Establish threshold for declaring a design space fragile after a space reduction
        # If I do an exponential...can I set different parameters for 200 vs. 1000 run test cases?
        # I want to set the threshold low enough so that the fragility is actually in play, but not so low that no space reductions are ever made
        threshold = 0.5*(iters/iters_max)     # Fixed value ?????  Exponential value from function already established????  time aware LSTM model????
        
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
    
