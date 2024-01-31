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
    
    def __init__(self):
        return
    
    
    # Return a true or false boolean value if fragile or not
    def basicCheck(self, risk, iters, iters_max):
        
        # Set threshold
        threshold = iters / iters_max
        
        # Initialize an empty dictionary for tracking max risk values
        max_risk = {}
        
        # Loop through each rule (set) being proposed
        for rule, lis in risk.items():
            
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
    
    
    # Function for evaluating what part(s) of the rule are fragile and maybe breaking that rule up
    
    
    # Function for adding rule to a temporary banned rule list
    
