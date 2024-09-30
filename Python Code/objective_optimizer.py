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
from merge_constraints import getPerceptions
from scipy.optimize import minimize
import numpy as np
import copy


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
def calcAddedRiskRobustness(gradient_factor, Discips_fragility, 
                            pf_combos, pf_std_fragility, Grads,
                            fragility_extensions, total_points, X_explored, 
                            Y_explored, passfail, passfail_std, 
                            Space_Remaining, gpr_params, irules_fragility, 
                            irules_new, fragility_type, iters, iters_max, 
                            exp_parameters, fragility_shift, banned_rules, 
                            windreg, running_windfall, running_regret, risk, 
                            final_combo, threshold_tracker = None, 
                            threshold = 1e-3):
    
    # Initialize lists for new passfail predictions
    passfail_new = copy.deepcopy(passfail)
    passfail_std_new = copy.deepcopy(passfail_std)
    
    # Update time history of passfail predictions
    for i in range(0, len(passfail)):
        
        # Skip if None key does not exist in the dictionary
        if None not in passfail[i]: continue
        
        # Gather current time iteration
        iter_cur = passfail[i]['time']
        
        # Loop through each discipline
        for j in range(0, len(passfail[i][None])):
            
            # Determine proper explored data key
            for k in range(0, len(X_explored)):
                if X_explored[k]['time'] == iter_cur:
                    explored_ind = k
            
            # Determine the magnitude of the gradient of each explored point
            grad_mag = np.linalg.norm(Grads[explored_ind][None][j], axis=1)
            
            # Update pass-fail predictions
            Y_explored_new = Y_explored[explored_ind][None][j]['non_reduced'] \
                - gradient_factor*grad_mag
            
            # Determine proper space remaining data key
            for k in range(0, len(Space_Remaining[j])):
                past_time = Space_Remaining[j][k]['iter']
                if past_time < iter_cur:
                    spacerem_ind = k
                else:
                    break
            
            # Place data with updated pass-fail training values in dictionary
            diction = {
                'tested_ins': X_explored[explored_ind][None][j]['non_reduced'],
                'Pass_Amount': Y_explored_new,
                'Fail_Amount': np.zeros(len(Y_explored_new)),
                'space_remaining': Space_Remaining[j][spacerem_ind]\
                    ['space_remaining'],
                'ins': Discips_fragility[j]['ins']
            }
            
            # Make new pass-fail predictions from updated training points
            normalized_predictions, adjusted_std_devs, _, _, _ = \
                getPerceptions(diction, gpr_params)
            
            # Place updated pass-fail predictions in proper new lists
            passfail_new[i][None][j]['non_reduced'] = normalized_predictions
            passfail_std_new[i][None][j]['non_reduced'] = adjusted_std_devs
    
    # Make new fragility input rule list minus newest addition
    irules_fragility2 = [item for item in irules_fragility \
                         if item not in irules_new]
    
    # Determine present non-reduced design space's updated predictions
    pf_fragility_new = [None for _ in Discips_fragility]
    for i in range(len(passfail_new) - 1, -1, -1):
        if not None in passfail_new[i]: continue
        for j in range(0, len(passfail_new[i][None])):
            pf_fragility_new[j] = passfail_new[i][None][j]['non_reduced']
        break
    
    # Initalize new fragility assessment object
    fragnalysis = fragilityCommands(Discips_fragility, irules_fragility2, 
                                    pf_combos, pf_fragility_new, 
                                    pf_std_fragility, passfail_new, 
                                    passfail_std_new, fragility_extensions, 
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
                           pf_std_fragility, passfail,
                           passfail_std, fragility_extensions, total_points,
                           fragility_type, iters, iters_max,
                           exp_parameters, irules_new, fragility_shift,
                           banned_rules, windreg, running_windfall, 
                           running_regret, risk, final_combo, Grads,
                           X_explored, Y_explored, Space_Remaining, gpr_params,
                           initial_guess = 0.0):
    
    # Initialize the best guess tracker
    tracker = BestGuessTracker()
    
    # Find the maximum gradient factor value
    result = minimize(calcAddedRiskRobustness,
                      initial_guess,
                      args = (Discips_fragility, pf_combos, 
                              pf_std_fragility, Grads, fragility_extensions, 
                              total_points, X_explored, Y_explored, passfail, 
                              passfail_std, Space_Remaining, gpr_params, 
                              irules_fragility, irules_new, fragility_type, 
                              iters, iters_max, exp_parameters, 
                              fragility_shift, banned_rules, windreg, 
                              running_windfall, running_regret, risk, 
                              final_combo, tracker),
                      method='L-BFGS-B',
                      bounds=[(0.0, np.inf)])
    
    # Check if the optimization was successful
    if result.success:
        optimal_gradient_factor = result.x[0]
    
    # Return best guess
    if tracker.best_guess is not None:
        final_threshold = tracker.smallest_threshold
        print(f"Best guess found with smallest threshold: "
              f"{tracker.best_guess[0]} with smallest threshold: "
              f"{tracker.smallest_threshold}")
        return tracker.best_guess[0], final_threshold
    elif result.success:
        final_threshold = tracker.smallest_threshold
        print(f"Optimal gradient factor: {optimal_gradient_factor}")
        return optimal_gradient_factor, final_threshold
    else:
        print("Could not find any optimal gradient factor values.")
        return 0.0, None