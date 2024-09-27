"""
SUMMARY:


CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from fragility_script import fragilityCommands
from scipy.optimize import minimize


"""
SECONDARY CLASS
"""
class BestGuessTracker:
    
    def __init__(self):
        self.best_guess = None
        self.smallest_threshold = float('inf')  # Start with infinity
    
    def update(self, guess, threshold):
        if threshold > 0 and threshold < self.smallest_threshold:
            self.smallest_threshold = threshold
            self.best_guess = guess


"""
SECONDARY FUNCTION
"""
def calcAddedRiskRobustness(gradient_factor, pf_fragility, grads_mag,
                            irules_fragility, irules_new, Discips_fragility,
                            pf_combos, pf_std_fragility, passfail,
                            passfail_std, fragility_extensions, total_points,
                            fragility_type, iters, iters_max, exp_parameters,
                            fragility_shift, banned_rules, windreg,
                            running_windfall, running_regret, risk, 
                            final_combo, threshold_tracker = None, 
                            threshold = 1e-3):
    
    # Initialize an empty pass-fail list for each discipline
    pf_fragility_new = [None for _ in pf_fragility]
    
    # Loop through each discipline's passfail values
    for j, pf_discip in enumerate(pf_fragility):
        
        # Decrease pf values by gradient factor times gradient magnitude
        pf_fragility_new[j] = pf_discip - gradient_factor*grads_mag[j]
    
    # Make new fragility input rule list minus newest addition
    irules_fragility2 = [item for item in irules_fragility \
                         if item not in irules_new]
    
    # Initalize new fragility assessment object
    fragnalysis = fragilityCommands(Discips_fragility, irules_fragility2, 
                                    pf_combos, pf_fragility_new, 
                                    pf_std_fragility, passfail, 
                                    passfail_std, fragility_extensions, 
                                    total_points)
    
    # Perform desired fragility assessment
    wr, run_wind, run_reg, ris = getattr(fragnalysis, fragility_type)()
    
    # Assess risk from fragility assessment
    _, _, _, _, _, _, _, _, net_wr, _ = fragnalysis.assessRisk(ris, iters, 
        iters_max, exp_parameters, irules_new, fragility_shift, 
        banned_rules, windreg, wr, running_windfall, run_wind, 
        running_regret, run_reg, risk)
    
    # Determine the added risk robustness
    ### NOTE: ONLY WORKS WITH basicCheck2 IN fragility_script
    risk_rob = fragnalysis.assessRobustness(net_wr[final_combo])
    
    # Isolate discipline with the smallest difference
    smallest_threshold = min([discip['difference'] for discip in risk_rob])
    
    # Update the threshold tracker with the current guess and threshold
    if threshold_tracker is not None:
        threshold_tracker.update(gradient_factor, smallest_threshold)
    
    # Determine the absolute value of the smallest threshold
    smallest_threshold = abs(smallest_threshold)
    
    # Return 0.0 to stop optimizer if difference is less than threshold
    if smallest_threshold < threshold: return 0.0
    
    # Return the absolute value of the smallest difference
    return smallest_threshold


"""
MAIN FUNCTION
"""
def optimizeGradientFactor(Discips_fragility, irules_fragility, pf_combos, 
                           pf_fragility, pf_std_fragility, passfail,
                           passfail_std, fragility_extensions, total_points,
                           grads_mag, fragility_type, iters, iters_max,
                           exp_parameters, irules_new, fragility_shift,
                           banned_rules, windreg, running_windfall, 
                           running_regret, risk, final_combo, 
                           initial_guess = 0.0):
    
    # Initialize the best guess tracker
    tracker = BestGuessTracker()
    
    # Find the maximum gradient factor value
    result = minimize(calcAddedRiskRobustness,
                      initial_guess,
                      args = (pf_fragility, grads_mag, irules_fragility, 
                              irules_new, Discips_fragility, pf_combos, 
                              pf_std_fragility, passfail, passfail_std, 
                              fragility_extensions, total_points,
                              fragility_type, iters, iters_max, 
                              exp_parameters, fragility_shift, banned_rules, 
                              windreg, running_windfall, running_regret, risk, 
                              final_combo, tracker),
                      method='BFGS')
    
    # Check if the optimization was successful
    if result.success:
        optimal_gradient_factor = result.x[0]
    
    # Return best guess
    if tracker.best_guess is not None:
        print(f"Best guess found with smallest threshold: "
              f"{tracker.best_guess[0]} with smallest threshold: "
              f"{tracker.smallest_threshold}")
        return tracker.best_guess[0]
    elif result.success:
        print(f"Optimal gradient factor: {optimal_gradient_factor}")
        return optimal_gradient_factor
    else:
        print("Could not find any optimal gradient factor values.")
        return 0.0