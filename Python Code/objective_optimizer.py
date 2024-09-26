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
import numpy as np


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
                           initial_guess = 0.1, learning_rate = 0.1, 
                           tol = 1e-5, max_iter = 5):
    
    # Set gradient factor as the initial guess
    gradient_factor = initial_guess
    
    # Loop through iterations
    for i in range(0, max_iter):
        
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
        
        # Break loop if the added risk robustness of every discipline is positive 
        ### and one of them is close enough to zero
        # First check that all disciplines are passing
        # Then check if any discipline is within tolerance
        if not net_wr[final_combo]['fragile'] and \
            any(discip['difference'] < tol for discip in risk_rob): break
        
        # Update gradient factor guess -- RETURN THE SMALLEST POSITIVE(?) GRADIENT FACTOR IN TIME SERIES?
    
    # Return the final gradient factor
    return gradient_factor