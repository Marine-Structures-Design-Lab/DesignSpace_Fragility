"""
SUMMARY:
Uses an iterative process to determine the gradient factor value that reduces
the added risk robustness to zero when a proposed space reduction is not
fragile.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from fragility_script import fragilityCommands
from merge_constraints import getPerceptions
import numpy as np
import copy


"""
SECONDARY CLASS
"""
class BestGuessTracker:
    
    def __init__(self):
        self.best_guess = None
        self.smallest_threshold = float('inf')
    
    def update(self, guess, threshold):
        """
        Description
        -----------
        Tracks the best guess gradient factor guess and its associated 
        added risk robustness value.

        Parameters
        ----------
        guess : Float
            Current gradient factor value
        threshold : Float
            Associated added risk robustness value
        """
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
                            final_combo, threshold_tracker = None):
    """
    Description
    -----------
    Executes a fragility assessment for the current gradient factor guess and
    determines that guess's added risk robustness.

    Parameters
    ----------
    Discips_fragility : Dictionary
        All information pertaining to each discipline at the beginning of
        the newest space reduction cycle
    pf_combos : Dictionary
        Each discipline's pass-fail predictions for each design space of
        each new rule combination being considered
    pf_std_fragility : List
        Each discipline's pass-fail standard deviations for the non-reduced
        design space at the beginning of the space reduction cycle
    Grads : List of dictionaries
        Time history of each explored design point's gradient vector
    fragility_extensions : Dictionary
        Different extensions to the initial fragility framework extension
        that a design manager wants to include in the assessment
    total_points : Integer
        An approximate total number of evenly spaced points the user
        desires for tracking the space remaining in a discipline's design
        space
    X_explored : List of dictionaries
        Time history of explored design points' x-training data
    Y_explored : List of dictionaries
        Time history of explored design points' y-training data (pass-fail)
    passfail : List of dictionaries
        History of each discipline's pass-fail predictions up to a certain
        point in time
    passfail_std : List of dictionaries
        History of each discipline's pass-fail standard deviatiokns up to a
        certain point in time
    Space_Remaining : List of dictionaries
        Time history of discretized space remaining
    gpr_params : Dictionary
        Parameters for GPR kernels
    irules_fragility : List
        Sympy and/or relationals detailing all of the new space reduction
        rules of the current space reduction cycle
    irules_new : List
        Sympy relationals dictating the newest set of space reduction rules
        being considered
    fragility_type : String
        Type of fragility assessment desired (e.g. PFM or EFM)
    iters : Integer
        Amount of time that has been spent exploring design spaces already
    iters_max : Integer
        Total time allotted to explore design spaces
    exp_parameters : Numpy array
        Various exponential function parameters dictating minimum space
        reduction pace for each discipline
    fragility_shift : Float
        Amount to either translate the exponential function (basicCheck) or
        set as a weighted coefficient (basicCheck2) for manipulating the
        fragility threshold via the design manager
    banned_rules : Set
        Sympy relationals detailing the input rule(s) no longer being
        considered for the current round of space reductions
    windreg : List of dictionaries
        Contains the complete history of gathered windfall and regret data
        for each discipline's design space
    running_windfall : List of dictionaries
        Contains the complete history of gathered windfall totals for each
        discipline's design space
    running_regret : List of dictionaries
        Contains the complete history of gathered regret totals for each
        discipline's design space
    risk : List of dictionaries
        Contains the complete history of gathered risk data for each
        discipline
    final_combo : Tuple
        Final combination of input rules that a designer is moving forward
        with as a space reduction
    threshold_tracker : Object, optional
        Object for the BestGuessTracker The default is None.

    Returns
    -------
    smallest_threshold : Float
        Added risk robustness value of the current gradient factor guess.
    """
    
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
    
    # Return the value of the smallest difference
    return smallest_threshold


"""
MAIN FUNCTION
"""
def optimizeGradientFactor(Discips_fragility, irules_fragility, pf_combos, 
                           pf_std_fragility, passfail, passfail_std, 
                           fragility_extensions, total_points, fragility_type, 
                           iters, iters_max, exp_parameters, irules_new, 
                           fragility_shift, banned_rules, windreg, 
                           running_windfall, running_regret, risk, 
                           final_combo, Grads, X_explored, Y_explored, 
                           Space_Remaining, gpr_params, initial_guess=0.1,
                           max_iter = 50, tol = 1e-2, ptol = 1e-5):
    """
    Description
    -----------
    Conducts a search for the gradient factor value that reduces the added risk
    robustness to zero for a non-fragile space reduction.

    Parameters
    ----------
    Discips_fragility : Dictionary
        All information pertaining to each discipline at the beginning of
        the newest space reduction cycle
    irules_fragility : List
        Sympy and/or relationals detailing all of the new space reduction
        rules of the current space reduction cycle
    pf_combos : Dictionary
        Each discipline's pass-fail predictions for each design space of
        each new rule combination being considered
    pf_std_fragility : List
        Each discipline's pass-fail standard deviations for the non-reduced
        design space at the beginning of the space reduction cycle
    passfail : List of dictionaries
        History of each discipline's pass-fail predictions up to a certain
        point in time
    passfail_std : List of dictionaries
        History of each discipline's pass-fail standard deviatiokns up to a
        certain point in time
    fragility_extensions : Dictionary
        Different extensions to the initial fragility framework extension
        that a design manager wants to include in the assessment
    total_points : Integer
        An approximate total number of evenly spaced points the user
        desires for tracking the space remaining in a discipline's design
        space
    fragility_type : String
        Type of fragility assessment desired (e.g. PFM or EFM)
    iters : Integer
        Amount of time that has been spent exploring design spaces already
    iters_max : Integer
        Total time allotted to explore design spaces
    exp_parameters : Numpy array
        Various exponential function parameters dictating minimum space
        reduction pace for each discipline
    irules_new : List
        Sympy relationals dictating the newest set of space reduction rules
        being considered
    fragility_shift : Float
        Amount to either translate the exponential function (basicCheck) or
        set as a weighted coefficient (basicCheck2) for manipulating the
        fragility threshold via the design manager
    banned_rules : Set
        Sympy relationals detailing the input rule(s) no longer being
        considered for the current round of space reductions
    windreg : List of dictionaries
        Contains the complete history of gathered windfall and regret data
        for each discipline's design space
    running_windfall : List of dictionaries
        Contains the complete history of gathered windfall totals for each
        discipline's design space
    running_regret : List of dictionaries
        Contains the complete history of gathered regret totals for each
        discipline's design space
    risk : List of dictionaries
        Contains the complete history of gathered risk data for each
        discipline
    final_combo : Tuple
        Final combination of input rules that a designer is moving forward
        with as a space reduction
    Grads : List of dictionaries
        Time history of each explored design point's gradient vector
    X_explored : List of dictionaries
        Time history of explored design points' x-training data
    Y_explored : List of dictionaries
        Time history of explored design points' y-training data (pass-fail)
    Space_Remaining : List of dictionaries
        Time history of discretized space remaining
    gpr_params : Dictionary
        Parameters for GPR kernels
    initial_guess : Float, optional
        Initial guess for the gradient factor value. The default is 0.1.
    max_iter : Integer, optional
        Maximum number of gradient factor guesses allowed. The default is 50.
    tol : Float, optional
        Maximum added risk robustness value indicating convergence. The default
        is 1e-2.
    ptol : Float, optional
        Maximum difference between consecutive positive added risk robustness 
        values indicating convergence. The default is 1e-5.

    Returns
    -------
    gradient_factor : Float
        Gradient factor value that reduces added risk robustness to zero
    threshold : Float
        Added risk robustness of associated gradient factor value
    """
    
    # Initialize the best guess tracker and initial guess
    tracker = BestGuessTracker()
    gradient_factor = initial_guess
    
    # Establish upper and lower guesses
    gf_lower = 0.0
    gf_upper = np.inf
    
    # Create a list to track positive differences between risk and threshold
    pos_diff = []
    
    # Loop through max iterations
    for iteration in range(max_iter):
        
        # Print current gradient factor
        print(f"Current gradient factor guess: {gradient_factor}")
        
        # Calculate the current objective value function
        current_threshold = calcAddedRiskRobustness(gradient_factor, 
            Discips_fragility, pf_combos, pf_std_fragility, Grads, 
            fragility_extensions, total_points, X_explored, Y_explored, 
            passfail, passfail_std, Space_Remaining, gpr_params, 
            irules_fragility, irules_new, fragility_type, iters, iters_max, 
            exp_parameters, fragility_shift, banned_rules, windreg, 
            running_windfall, running_regret, risk, final_combo, tracker)
        
        # Print current threshold
        print(f"Current difference between value and threshold: "
              f"{current_threshold}")
        
        # Check convergence based on difference between risk and risk threshold
        if current_threshold < tol and current_threshold >= 0:
            print(f"Converged at iteration {iteration}")
            break
        
        # Check convergence based on positive thresholds not changing
        if len(pos_diff) > 1 and abs(pos_diff[-1] - pos_diff[-2]) < ptol:
            print(f"Converged at iteration {iteration}")
            break
        
        # Add to positive threshold list if threshold is positive
        if current_threshold > 0: pos_diff.append(current_threshold)
        
        # Set new upper or lower gradient_factor bounds
        if gradient_factor < gf_upper and current_threshold < 0:
            gf_upper = gradient_factor
        elif gradient_factor > gf_lower and current_threshold > 0:
            gf_lower = gradient_factor
        
        # Set new gradient factor as the midpoint
        if not np.isinf(gf_upper):
            gradient_factor = (gf_upper - gf_lower)/2 + gf_lower
        
        # Double the gradient factor
        else:
            gradient_factor *= 2
    
    # Return best guess
    if tracker.best_guess is not None:
        final_threshold = tracker.smallest_threshold
        print(f"Best guess found with smallest threshold: "
              f"{tracker.best_guess} with smallest threshold: "
              f"{tracker.smallest_threshold}")
        return tracker.best_guess, final_threshold
    else:
        print(f"Final gradient factor: {gradient_factor}")
        return gradient_factor, current_threshold

