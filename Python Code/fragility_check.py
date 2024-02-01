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
import random


"""
FUNCTIONS
"""




"""
CLASS
"""
class checkFragility:
    
    def __init__(self, Discips, risk):
        self.D = Discips
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
        
        # Return results from the basic fragility assessment
        return max_risk
    
    
    def newCombo(self, net_wr, original_banned_rules):
        
        # Create an empty set for banned rules
        banned_rules = set()
        
        # Create an empty set for tracking rule combinations that do not lead to fragile design space
        good_combos = set()
        
        # Loop through each rule combination
        for rule_tup, net_dic in net_wr.items():
            
            # Check if rule combination leads to fragile design space
            if net_dic['fragile'] == True:
                
                # Loop through each rule in the tuple
                for rule in rule_tup:
                    
                    # Add each rule to the set of banned rules
                    banned_rules.add(rule)
            
            # Do following because rule combination does not lead to fragile design space
            else:
                
                # Add tuple to the set of good combinations
                good_combos.add(rule_tup)
        
        # Choose a random good combo as the the final combo
        final_combo = random.choice(list(good_combos))
        
        # Loop through each good rule combination
        for rule_tup in good_combos:
            
            # Loop through each rule in the tuple
            for rule in rule_tup:
                
                # Remove rule from banned rule set if there
                banned_rules.discard(rule)
        
        # Add the newest banned rules to the original set of banned rules
        original_banned_rules |= banned_rules
        
        # Return the non-fragile rule combination and ALL banned relationals
        return final_combo, original_banned_rules
    
    
    def throwOut(self, rule_combos):
        
        # Loop through each rule combination
        for rule_tup in rule_combos:
            
            # Initialize a set tracking variables of tuple
            symb_set = set()
            
            # Loop through each rule in the tuple
            for rule in rule_tup:
                
                # Get free symbols of the rule
                free_symbs = rule.free_symbols
                
                # Add these symbols to the set for the tuple
                symb_set |= free_symbs
            
            # Initialize a set tracking indices of disciplines involved
            frag_set = set()
            
            # Loop through each discipline
            for ind_discip, dic_discip in enumerate(self.D):
                
                # Check if any symbols of the rule tuple are in list of
                # inputs of the discipline
                if any(symb_var in dic_discip['ins'] for symb_var in symb_set):
                    
                    # Add index to the fragility set list
                    frag_set.add(ind_discip)
            
            # Flag to determine whether to skip to the next rule_tup
            skip_rule_tup = False
            
            # Loop through set of disciplines involved with rule tuple
            for ind_discip in frag_set:
                
                # Check if discipline IS forcing a space reduction
                if self.D[ind_discip]['force_reduction'][0] == True:
                    
                    # Set flag and break to move to next rule tuple
                    skip_rule_tup = True
                    break
            
            # Check if flag was set and continue to next rule tuple
            if skip_rule_tup:
                continue
            
            # Remove the tuple from the rule combos
            rule_combos.remove(rule_tup)
        
        
        
        
        
        return rule_combos
