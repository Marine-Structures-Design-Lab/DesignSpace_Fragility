"""
SUMMARY:
Performs a basic check on the fragility of all design spaces based on the
endured added risk of all the input rule(s) of a current time stamp, and then
selects an input rule combination to move forward with if multiple ones being
proposed do not create any fragile design spaces.

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
CLASS
"""
class checkFragility:
    
    def __init__(self, risk):
        """
        Parameters
        ----------
        risk : Dictionary
            Added potentials for regret and windfall accompanying a set of
            input rule(s) for the current timestamp
        """
        self.risk = risk
        return
    
    
    def basicCheck(self, iters, iters_max, p, shift):
        """
        Description
        -----------
        Return the maximum endured risk for the input rule combo(s) being
        considered as well as a boolean value indicating whether the endured
        added risk exceeds the maximum threshold at the particular time.

        Parameters
        ----------
        iters : TYPE
            DESCRIPTION.
        iters_max : TYPE
            DESCRIPTION.
        p : TYPE
            DESCRIPTION.
        shift : TYPE
            DESCRIPTION.

        Returns
        -------
        max_risk : TYPE
            DESCRIPTION.

        """
        
        # Establish exponential fragility threshold
        threshold = max(calcExponential(iters/iters_max, p), 0.0) + shift
        
        # Initialize an empty dictionary for tracking max risk values
        max_risk = {}
        
        # Loop through each new rule combination
        for rule, lis in self.risk.items():
            
            # Initialize a max risk value to a large negative value
            max_risk[rule] = {"value": -1000, "fragile": False}
            
            # Loop through each discipline's regret and windfall values
            for dic in lis:
                
                # Subtract windfall from regret
                net_risk = dic['regret'] - dic['windfall']
                
                # Update max risk value
                max_risk[rule]["value"] = max(max_risk[rule]["value"],net_risk)
            
            # Set boolean value depending on max risk value
            if max_risk[rule]["value"] > threshold: 
                max_risk[rule]["fragile"] = True
            else: max_risk[rule]["fragile"] = False
        
        # Return results from the basic fragility assessment
        return max_risk
    
    
    def newCombo(self, net_wr, original_banned_rules):
        """
        Description
        -----------
        Selects one rule combo to move forward from the all of the rule
        combo(s) not leading to any fragile design spaces while adding any
        rule(s) that only lead to fragile design spaces to the banned rule
        list.

        Parameters
        ----------
        net_wr : TYPE
            DESCRIPTION.
        original_banned_rules : TYPE
            DESCRIPTION.

        Returns
        -------
        final_combo : TYPE
            DESCRIPTION.
        original_banned_rules : TYPE
            DESCRIPTION.

        """
        
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
    
