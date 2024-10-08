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
from windfall_regret import createBins
import random
import numpy as np


"""
FUNCTION
"""
def adaptiveFactor(combo, Df, total_points):
    """
    Description
    -----------
    Calculates the fraction of a (sub)space's remaining design space size
    relative to its original size.

    Parameters
    ----------
    combo : Tuple of sympy variables
        Design variables making up the subspace being assessed
    Df : Dictionary
        All information pertaining to a discipline at the beginning of the
        newest space reduction cycle
    total_points : Integer
        Total number of space remaining points created at the beginning of the
        simulation

    Returns
    -------
    space_rem : Float
        Fraction of (sub)space remaining relative to the original (sub)space
        size
    """
    
    # Determine the dimensions of the (sub)space being assessed
    indices_rem = [Df['ins'].index(symbol) for symbol in combo]
    
    # Check if index list is as long as the discipline's design variable list
    if len(indices_rem) >= len(Df['ins']):
        
        # Calculate fraction of total design space remaining to starting size
        space_rem = (Df['space_remaining'].shape[0] / Df['tp_actual'])
        
    # Perform the following commands for the subspace
    else:
        
        # Find unique bins and corresponding indices
        unique_bins, inverse_indices = createBins(Df,indices_rem,total_points)
        
        # Determine remaining subspace size
        sub_rem = unique_bins.shape[0]
        
        # Determine original subspace size
        npoints_dim = int(round(total_points ** (1. / len(Df['ins']))))
        sub_orig = npoints_dim ** len(indices_rem)
        
        # Calculate fraction of total subspace remaining to starting size
        space_rem = sub_rem / sub_orig
        
    # Return the fraction of subspace remaining to starting subspace size
    return space_rem


"""
CLASS
"""
class checkFragility:
    
    def __init__(self, risk, Discips_fragility):
        """
        Parameters
        ----------
        risk : Dictionary
            Added potentials for regret and windfall accompanying a set of
            input rule(s) for the current timestamp
        Discips_fragility : Dictionary
            All the information pertaining to each discipline at the start of a
            new space reduction cycle
        """
        self.risk = risk
        self.Df = Discips_fragility
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
        iters : Integer
            Current time iteration of design problem.
        iters_max : Integer
            Amount of time iterations allotted to carry out design problem.
        p : Numpy array
            Exponential function parameters dictating space reduction pace.
        shift : Float
            Amount to shift exponential function for adaptation to setting
            maximum risk threshold

        Returns
        -------
        max_risk : Dictionary
            Endured risk for space reduction and boolean indicating whether the
            maximum risk threshold has been exceeded
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
                
                # Loop through each subspace being assessed
                for combo, dic2 in dic.items():
                    
                    # Subtract windfall from regret
                    net_risk = dic[combo]['regret'] - dic[combo]['windfall']
                    
                    # Update max risk value
                    max_risk[rule]["value"] = max(max_risk[rule]["value"], 
                                                  net_risk)
            
            # Set boolean value depending on max risk value
            if max_risk[rule]["value"] > threshold:
                max_risk[rule]["fragile"] = True
            else: max_risk[rule]["fragile"] = False
        
        # Return results from the basic fragility assessment
        return max_risk
    
    
    def basicCheck2(self, iters, iters_max, p, scale_weight, total_points):
        """
        Description
        -----------
        Asymptotic method for setting maximum risk threshold that adjusts
        according to time remaining and amount of each discipline's design
        space that has already been reduced.

        Parameters
        ----------
        iters : Integer
            Current time iteration of design problem.
        iters_max : Integer
            Amount of time iterations allotted to carry out design problem.
        p : Numpy array
            Exponential function parameters dictating space reduction pace.
        scale_weight : Float
            Amount to scale asymptotic function's maximum risk threshold.
        total_points : Integer
            An approximate total number of evenly spaced points the user
            desires for tracking the space remaining in a discipline's design
            space

        Returns
        -------
        max_risk : Dictionary
            Endured risk for space reduction and boolean indicating whether the
            maximum risk threshold has been exceeded
        """
        
        # Initialize an empty dictionary for tracking max risk values
        max_risk = {}
        
        # Loop through each new rule combination
        for rule, lis in self.risk.items():
            
            # Initialize a max dictionary with a false fragile value
            max_risk[rule] = {"fragile": False}
            
            # Loop through each discipline's regret and windfall values
            for ind_dic, dic in enumerate(lis):
                
                # Initialize a small max risk-to-threshold ratio
                risk_threshold = -np.inf
                
                # Loop through each subspace being assessed
                for combo, dic2 in dic.items():
                    
                    # Establish maximum fragility threshold for (sub)space
                    threshold = scale_weight * \
                        (adaptiveFactor(combo, self.Df[ind_dic], total_points)\
                        / (1-calcExponential(iters/iters_max, p))) * \
                        (1/(1-(iters/iters_max))) if iters != iters_max \
                        else np.inf
                    
                    # Subtract windfall from regret
                    net_risk = dic2['regret'] - dic2['windfall']
                    
                    # Check if net risk is infinite
                    if np.isinf(net_risk):
                        
                        # Reassign risk information for discipline
                        max_risk[rule][ind_dic] = {
                            'value': net_risk,
                            'threshold': 0.0,
                            'sub-space': combo
                        }
                    
                    # Check if risk-to-threshold ratio is greater than maximum
                    elif net_risk / threshold > risk_threshold:
                        
                        # Reassign risk information for discipline
                        max_risk[rule][ind_dic] = {
                            'value': net_risk,
                            'threshold': threshold,
                            'sub-space': combo
                        }
                        
                        # Set new max risk-to-threshold value
                        risk_threshold = net_risk / threshold
                    
                # Check if added risk exceeds maximum threshold
                if max_risk[rule][ind_dic]['value'] > \
                    max_risk[rule][ind_dic]['threshold']:
                    
                    # Set fragile tracker to true for the rule
                    max_risk[rule]['fragile'] = True
            
            # Create a list of each discipline's risk values
            risk_list = []
            for key in max_risk[rule]:
                if key == 'fragile': continue
                risk_list.append(max_risk[rule][key]['value'])
                
            # Check if all added risk values are 0.0 because no space removed
            if all(abs(val) < 1e-8 for val in risk_list):
                
                # Set fragile tracker to true for the rule
                max_risk[rule]['fragile'] = True
        
        # Return results from the fragility assessment
        return max_risk
    
    
    def newCombo(self, net_wr, original_banned_rules):
        """
        Description
        -----------
        Selects one rule combo to move forward with from the all of the rule
        combo(s) not leading to any fragile design spaces while adding any
        rule(s) that only lead to fragile design spaces to the banned rule
        list.
        
        Parameters
        ----------
        net_wr : Dictionary
            Endured risk for space reduction and boolean indicating whether the
            maximum risk threshold has been exceeded
        original_banned_rules : Set
            Sympy And or Or relationals or inequalities that make up the input
            rule set that cannot be proposed by any disciplines for the current
            time stamp
        
        Returns
        -------
        final_combo : Tuple
            Sympy And or Or relationals or inequalities that make up the input
            rule(s) that the design manager is moving forward with
        original_banned_rules : Set
            Sympy And or Or relationals or inequalities that make up the
            updated input rule set that cannot be proposed by any disciplines
            for the current time stamp
        """
        
        # Create an empty set for banned rules
        banned_rules = set()
        
        # Create empty set for rule combos not leading to fragile design space
        good_combos = set()
        
        # Loop through each rule combination
        for rule_tup, net_dic in net_wr.items():
            
            # Check if rule combination leads to fragile design space
            if net_dic['fragile'] == True:
                
                # Loop through each rule in the tuple
                for rule in rule_tup:
                    
                    # Add each rule to the set of banned rules
                    banned_rules.add(rule)
            
            # Do following as rule combo does not lead to fragile design space
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
    
