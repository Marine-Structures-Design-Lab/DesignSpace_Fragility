"""
DESCRIPTION:
Main script file for simulating the space reduction process of a convergent
design approach (geared towards Set-Based Design).  In this file, a design
problem is presented with various discipline's and design variables.  An
automated process explores and propose reductions for each discipline's design
space, and then the design manager merges these proposed reductions among 
interdependent disciplines with the goal of converging on a set of final design
solutions.

The design manager has the option to call on a fragility framework to analyze
the vulnerability of remaining design spaces before committing to a reduction
decision.  This script file calls on this framework while also importing
classes and functions to make this set-based design and fragility assessment
process as modular as possible for various design problems.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from vars_def import setProblem
from uniform_grid import uniformGrid
# from exponential_reduction import plotExponential
from point_sorter import sortPoints
from design_changes import changeDesign
from exploration_check import checkSpace
from merge_constraints import mergeConstraints, getPerceptions
from connect_perceptions import connectPerceptions
from reduction_change import changeReduction
from fragility_script import fragilityCommands
from objective_optimizer import optimizeGradientFactor
from exploration_amount import exploreSpace
from get_constraints import getConstraints, getInequalities
from create_key import createKey, createDict, createNumpy
from input_vals import getInput
from output_vals import getOutput
from calc_rules import calcRules
from output_success import checkOutput
import numpy as np
import copy
import itertools
import argparse
import datetime
import os
import sys
import h5py


"""
PREPARE DATA
"""
# Establish Test Case
test_id = "TC1"

# Prepare for capturing console outputs and saving simulation data
parser=argparse.ArgumentParser(description="Simulation run unique identifier.")
parser.add_argument('--run_id', 
                    type=str, help="Unique identifier for this run.", 
                    default=None)
args = parser.parse_args()

# Set up unique identifier
current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
run_id = args.run_id if args.run_id else str(os.getpid())
unique_identifier = f"{test_id}_{current_time}_{run_id}"

# Redirect to stdout file
original_stdout = sys.stdout
log_file_path = f"console_output_{unique_identifier}.txt"
sys.stdout = open(log_file_path, 'w')


###############################################################################
################################ PROBLEM SETUP ################################
###############################################################################
"""
USER INPUTS
"""
# List the name of the problem on which the design team is working
### OPTIONS: SBD1, SenYang,...
problem_name = 'SenYang'

# Establish the allowed timeline for exploring the design problem
### This value determines the number of time iterations that will be executed,
### but it does not necessarily mean each explored point tested will only take
### one iteration to complete.
iters_max = 200    # Must be a positive integer!

# Decide on the strategy for producing random input values
### OPTIONS: Uniform, LHS (eventually),...
sample = 'uniform'

# Decide on number of points to attempt sampling in space remaining before
### moving on (a larger amount will help ensure a point is found during uniform
### sampling as remaining input spaces get smaller, but it will also lead to an
### increased run time during the search)
search_factor = 100

# Decide the approximate number of points that you want to use to estimate the
### space remaining in each discipline - more points will increase execution
### time of program but provide more accurate approximations of space remaining
### following any space reductions
total_points = 10000

# Decide on the run time (iterations) for each discipline's analysis
### Important to make sure that the length of the list coincides with the
### number of disciplines/equations there are in the design problem
run_time = [2, 3, 4]    # Must all be positive integers!

# Set exponential function parameters dictating minimum space reduction pace
exp_parameters = np.array(\
    [0.2,   # p1: x-intercept (0 <= p1 < p3)
     2.2,   # p2: Steepness (any real, positive number)
     1.0,   # p3: Max percent of time to force reductions (p1 < p3 <=1)
     0.95]) # p4: Percent of space reduced at max reduction time (0 <= p4 <= 1)

# Decide if ANY reduction proposed by discipline should be accepted by default
auto_accept = False     # True = yes, False = no

# Decide if the fragility of proposed reductions is to be assessed and the 
# shift in the exponential curve for determining maximum threshold
fragility = True       # True = yes, False = no
fragility_type = 'EFM' # PFM = Probability-based; EFM = Entropy-based
fragility_shift = 0.4  # Should be a positive float

# Decide on which elements of the extended fragility framework to pursue
### Options: sub_spaces, interdependencies, objective_changes
### For sub-spaces, inputs in the list should be integers ranging between 1 to
### the maximum number of dimensions in a design space.  It will end up
### removing dimensions from the design space and assessing the fragility of
### the design space without that dimension.  1 => Look at fragility of
### subspaces only consisting of 1 design variable, 2 => Look at fragility of
### subspaces consisting of 2 design variables, and so on.  Needs to have at
### least 1 integer in there by default
fragility_extensions = {
    "sub_spaces": [6], # Design sub-space dimensions to consider
    "interdependencies": False,       # Consider design space interdependencies
    "objective_changes": True         # Consider changes to req's and analyses
}

# Indicate when and to what design space(s) a design change should occur
### Keep these in list form and have each design change type match up with a
### time for it to occur...times must be in ascending order!
change_design = []  # Options: Inputs, Analyses, Outputs, Reqs
change_time = []          # Fraction of elapsed time(s) before change occurs

# Set initial values for creating and evaluating the suitability of partitions
# (1st value) as well as the amount that each criteria should be increased by
# when forcing a space reduction (2nd value)
# START THESE LOW AS THEY WILL BE INCREASED TO FORCE A SPACE REDUCTION
part_params = {
    "cdf_crit": [0.1, 0.1],
    "fail_crit": [0.0, 0.05],
    "dist_crit": [0.2, 0.1],
    "disc_crit": [0.2, 0.1]
    }

# Set parameters for decision tree classifier used to propose space reductions
dtc_kwargs = {
    'max_depth': 1,
    # Add other parameters as needed
}

# Parameters for Gaussian kernel when forming perceptions of design space
gpr_params = {
    'length_scale_bounds': (1e-2, 1e3),
    'alpha': 0.00001
    # Add other parameters as needed
}

# Parameters for control points of quadratic bezier curve when merging proposed
# constraints
bez_point = {
    'P0': (0.0, 1.0),
    'P1': (0.5, 0.8),
    'P2': (1.0, 0.0)
    # Adjust these parameters as needed
    }


"""
COMMANDS
"""
# Establish disciplines and initial rules for the design problem of interest
prob = setProblem()
Discips, Input_Rules, Output_Rules = getattr(prob,problem_name)()

# Establish a counting variable that keeps track of the amount of time passed
iters = 0
temp_amount = 0

# Initialize design change counter to 0
change_counter = 0

# Initialize empty lists for data collection
Space_Remaining = [[] for _ in Discips]
Gradient_Factor = []

# Loop through each discipline
for i in range(0,len(Discips)):
    
    # Assign run time to each discipline
    Discips[i]['time'] = run_time[i]
    
    # Assign default partition parameters to each discipline
    Discips[i]['part_params'] = copy.deepcopy(part_params)
    
    # Initialize a force reduction boolean value and counter to each discipline
    Discips[i]['force_reduction'] = [False, 0]
    
    # Initialize an array for estimating the space remaining for the discipline
    Discips[i]['space_remaining'], Discips[i]['tp_actual'], \
        Discips[i]['space_remaining_ind'] = uniformGrid(total_points, 
                                                        Discips[i]['ins'],
                                                        Input_Rules)
        
    # Collect space remaining information for the discipline
    Space_Remaining[i].append({
        'iter': 0,
        'space_remaining': copy.deepcopy(Discips[i]['space_remaining'])
        })

# Print a visual of the minimum space reduction vs. time remaining pace
# plotExponential(exp_parameters)

# Create empty lists for new rules and index of discipline proposing each rule
irules_new = []
irules_fragility = []
irules_discip = []

# Initialize lists for windfall and regret calculations
passfail = []
passfail_std = []
Grads = []
X_explored = []
Y_explored = []
windreg = []
running_windfall = []
running_regret = []
risk = []

# Create a copy of the disciplines for fragility tracking
Discips_fragility = copy.deepcopy(Discips)

# Initialize an empty set of banned rules
banned_rules = {}

# Begin the design exploration and reduction process with allotted timeline
while iters <= iters_max:
    
    # Check if time is greater than 0 and new input rules are being proposed
    if iters > 0 and irules_new: 
        
        # Move data within each discipline according to the new rule
        Discips = sortPoints(Discips, irules_new)
        
        # Gather points for space remaining data
        for ind_discip, dic_discip in enumerate(Discips):
            Space_Remaining[ind_discip].append({
                'iter': copy.deepcopy(iters),
                'space_remaining': copy.deepcopy(dic_discip['space_remaining'])
                })
    
    # Add any new input rules to the list
    Input_Rules += irules_new
    
    # Reset the input rules to an empty list
    irules_new = []
    irules_discip = []
    
    # Check if time has been reached for a design change to occur
    if change_counter < len(change_time) and \
        (iters/iters_max) > change_time[change_counter]:
        
        # Set the change type
        change_type = change_design[change_counter]
        
        # Establish an object for the design change
        change = changeDesign(Discips, Input_Rules, Output_Rules)
        
        # Call the proper method based on the type of design change
        Discips, Input_Rules, Output_Rules = getattr(change, change_type)()
        
        # Reevaluate and update ALL previously explored points
        Discips = change.reevaluatePoints()
        
        # Increase change counter by 1!
        change_counter += 1
    
    
    # Override to exploration if any discipline maxed out partition parameters
    just_explore = False
    for ind_dic, dic in enumerate(Discips):
        part_params_check = dic["part_params"]
        if all(value[0] >= 0.5 for value in part_params_check.values()):
            just_explore = True
            print(
                f"Exploring because space reduction cannot be forced for "
                f"Discipline {ind_dic+1}!"
            )
            break
    
    # Check that we are not to jump straight to exploration
    if not just_explore:
        
        
        #######################################################################
        ##################### INDIVIDUAL SPACE REDUCTIONS #####################
        #######################################################################
        
        # Loop through each disicipline
        for i in range(0, len(Discips)):
            
            # Skip reduction considerations if no tested points to work with
            if 'tested_ins' not in Discips[i] or \
                np.shape(Discips[i]['tested_ins'])[0] == 0: continue
            
            # Initialize an object for the checkSpace class
            space_check = checkSpace(Discips[i]['ins'], **dtc_kwargs)
            
            # Produce array of "good" and "bad" values based on CDF threshold
            gb_array = space_check.goodBad(Discips[i]['Fail_Amount'],\
                           Discips[i]['part_params']['cdf_crit'][0])
            
            # Build the decision tree
            space_check.buildTree(Discips[i]['tested_ins'], gb_array)
            
            # Gather inequalitie(s) from the decision tree as a potential rule
            pot_rule = space_check.extractRules(\
                         Discips[i]['tested_ins'].astype(np.float32), gb_array)
            
            # Check if the rule meets the current criteria to be proposed
            rule_check = space_check.reviewPartitions(\
                Discips[i]['tested_ins'], pot_rule,\
                Discips[i]['Fail_Amount'],\
                Discips[i]['part_params']['fail_crit'][0],\
                Discips[i]['part_params']['dist_crit'][0],\
                Discips[i]['part_params']['disc_crit'][0])
            
            # Prepare the new rule
            newest_rule = space_check.prepareRule(pot_rule)
            
            # Add potential rule to the new rule list if it meets the criteria
            ### and not currently banned
            if rule_check and newest_rule not in banned_rules:
                irules_new.append(newest_rule)
                irules_discip.append(i)
            
        # Check up on new rules
        print(f"Individually proposed input rules: {irules_new}")
        
        # Check if any newly proposed rules are to be automatically accepted
        if irules_new and auto_accept:
            
            # Indicate that design manager automatically accepted rules
            print("Rules automatically accepted by design manager!")
            
            # Reset back to while loop for time iterations - no exploring
            continue
            
        #######################################################################
        ###################### UNIVERSAL SPACE REDUCTIONS #####################
        #######################################################################
        
        # Check if new input rules list is filled with any rules
        if irules_new:
            
            # Initialize an object for the mergeConstraints class
            merger = mergeConstraints(irules_new, Discips, gpr_params, 
                                      bez_point)
            
            # Have each discipline form an opinion on the rule
            rule_opinions, pf, pf_std = merger.formOpinion()
            
            # Check if discipline can veto proposal or if dominance forces it
            irules_new, pf, pf_std = \
                merger.domDecision(rule_opinions, irules_discip, pf, pf_std)
            
            # Check if new rules are still being proposed
            if irules_new:
                
                # Append passfail data to list
                passfail.append(copy.deepcopy(pf))
                passfail_std.append(copy.deepcopy(pf_std))
                
                # Check if any new rules have been proposed in this cycle yet
                if irules_fragility == [] and fragility:
                    
                    # Check if fragility to consider interdependencies
                    if fragility_extensions['interdependencies']:
                        
                        # Form passfail predictions considering interdependence
                        pf_fragility, pf_std_fragility = \
                            connectPerceptions(Discips)
                        
                    # Do following because interdependenices ignored
                    else:
                    
                        # Gather INITIAL passfail data of NON-REDUCED arrays
                        pf_fragility = []
                        pf_std_fragility = []
                        first_key = next(iter(pf.keys()))
                        for item1, item2 in zip(pf[first_key], 
                                                pf_std[first_key]):
                            pf_fragility.append(item1['non_reduced'])
                            pf_std_fragility.append(item2['non_reduced'])
                
                # Append time to passfail data
                passfail[-1]['time'] = iters
                passfail_std[-1]['time'] = iters
                
        # Check up on new rules
        print(f"Universally proposed input rules: {irules_new}")
        
        #######################################################################
        ######################### FRAGILITY ASSESSMENT ########################
        #######################################################################
        
        # Check if new input rules list is STILL filled with any rules
        if irules_new:
            
            # Initialize a fragility counter
            fragility_counter = 0
            
            # Run a fragility assessment if desired
            while fragility:
                
                # Determine the current rule combination length being checked
                combo_len = len(irules_new) - fragility_counter
                
                # Check if while loop rule combination length is less than 1
                if combo_len < 1: 
                    
                    # Add input rules to set of banned rules
                    banned_rules.update(irules_new)
                    
                    # Reset the input rules to an empty list
                    irules_new = []
                    
                    # Break the fragility loop
                    break
                
                # Gather rule combo(s) of current length in a list of tuples
                rule_combos=list(itertools.combinations(irules_new, combo_len))
                
                # Increase fragility counter by one
                fragility_counter += 1

                # Gather passfail data from independent GPR predictions
                pf_combos = {key: pf[key] for key in rule_combos}
                pf_std_combos = {key: pf_std[key] for key in rule_combos}
                
                # Initialize fragility assessment object
                fragnalysis = fragilityCommands(Discips_fragility, 
                    irules_fragility, pf_combos, pf_fragility,
                    pf_std_fragility, passfail, passfail_std, 
                    fragility_extensions, total_points)
                
                # Perform desired fragility assessment
                wr, run_wind, run_reg, ris = \
                    getattr(fragnalysis, fragility_type)()
                
                # Assess risk from fragility assessment
                banned_rules, windreg, running_windfall, running_regret, risk,\
                    irules_new, irules_fragility, break_loop, net_wr, \
                    final_combo = fragnalysis.assessRisk(ris, iters, iters_max, 
                                    exp_parameters, irules_new, 
                                    fragility_shift, banned_rules, windreg, wr, 
                                    running_windfall, run_wind, running_regret, 
                                    run_reg, risk)
                
                # Check if user wants to gauge objective space changes and if
                ### no design spaces are fragile
                if fragility_extensions['objective_changes'] and break_loop:
                    
                    # Indicate that objective change check is initiating
                    print("Initiating objective space fragility check.")
                    
                    # Find added risk robustness for final rule combo
                    ### NOTE: ONLY WORKS WITH basicCheck2 IN fragility_script
                    risk_rob = \
                        fragnalysis.assessRobustness(net_wr[final_combo])
                    
                    # Make new fragility input rule list minus newest addition
                    irules_fragility2 = [item for item in irules_fragility \
                                         if item not in irules_new]
                    
                    # Determine gradient factor value that eliminates the added
                    ### risk robustness
                    gradient_factor, threshold = optimizeGradientFactor(Discips_fragility, 
                        irules_fragility, pf_combos, 
                        pf_std_fragility, passfail, passfail_std, 
                        fragility_extensions, total_points, fragility_type, 
                        iters, iters_max, exp_parameters, irules_new, 
                        fragility_shift, banned_rules, windreg, 
                        running_windfall, running_regret, risk, final_combo, 
                        Grads, X_explored, Y_explored, Space_Remaining, 
                        gpr_params)
                    
                    # Store the gradient factor and its current time stamp
                    Gradient_Factor.append({
                        'iter': copy.deepcopy(iters),
                        'gradient_factor': copy.deepcopy(gradient_factor),
                        'Threshold_value': copy.deepcopy(threshold)
                    })
                    
                    # Indicate that objective change check is complete
                    print("Completed objective space fragility check.")
                
                # Break fragility loop if fragility assessment passed
                if break_loop: break
                
            # Check up on final input rules if fragility check executed
            if fragility:
                print(f"Final input rules after fragility check: {irules_new}")
            else:
                print("No fragility check executed!")
            
            # Reset back to while loop for time iterations - no exploring
            continue
            
        # If no new input rules, determine if time remaining paired with the
        ### design space remaining warrants a space reduction to be forced
        else:
            
            # Create an object for the changeReduction class
            red_change = changeReduction(Discips)
            
            # Estimate the space remaining in each discipline
            space_rem = red_change.estimateSpace()
            
            # Check if a space reduction should be forced
            Discips = red_change.forceReduction(space_rem, iters, iters_max, 
                                                exp_parameters, part_params)
            
            # Perform following commands if a space reduction should be forced
            if any(dictionary.get("force_reduction", False)[0] == True \
                   for dictionary in Discips):
                
                # Adjust the criteria for the necessary discipline(s)
                Discips = red_change.adjustCriteria()
                
                # Reset back to while loop for time iterations - no exploring
                continue
            
    
    ###########################################################################
    ############################### EXPLORATION ###############################
    ###########################################################################
    
    # Determine the amount of time/iterations for disciplines to explore
    space_amount = exploreSpace(iters,iters_max,run_time)
    temp_amount = space_amount.fixedExplore()
    print("\nCurrent Exploration Time: " + str(temp_amount) +\
          ", Total Exploration Time: " + str(temp_amount+iters))
    
    # Loop through each discipline (maintaining each of their independence)
    for i in range(0,len(Discips)):
        
        # Determine current input value rules for the discipline to meet
        input_rules = getConstraints(Discips[i]['ins'], Input_Rules)
        
        # Create a key for tested inputs of discipline if it does not exist
        Discips[i] = createKey('tested_ins',Discips[i])
        
        # Get input points according to the desired strategy
        inppts = getInput(Discips[i], input_rules, temp_amount, i)
        Discips[i] = inppts.getUniform(search_factor)
        
        # Create a key for tested outputs of discipline if it does not exist
        Discips[i] = createKey('tested_outs', Discips[i])
        
        # Get output points from equations or black-box programs
        outpts = getOutput(Discips[i])
        Discips[i] = outpts.getValues()
        
        # Create a key for the output rule inequalities relevant to discipline
        Discips[i] = createDict('out_ineqs', Discips[i])
        
        # Determine current output value rules for the discipline to meet
        output_rules = getConstraints(Discips[i]['outs'] + Discips[i]['ins'], 
                                      Output_Rules)
        
        # Gather any new inequalities of relevance to the discipline
        Discips[i] = getInequalities(Discips[i], output_rules, 'out_ineqs')
        
        # Calculate left-hand side of output rule inequality for each new point
        Discips[i]['out_ineqs'] = calcRules(Discips[i], 'out_ineqs', 
                                            'tested_outs', 'outs', 
                                            'tested_ins', 'ins')
        
        # Create a key for passing and failing of outputs if it does not exist
        Discips[i] = createKey('pass?', Discips[i])
        
        # Check whether the output points pass or fail
        outchk = checkOutput(Discips[i], output_rules)
        Discips[i] = outchk.basicCheck()
        
        # Create a key for extent of passing/failing if it does not exist
        Discips[i] = createNumpy('Fail_Amount', Discips[i])
        Discips[i] = createNumpy('Pass_Amount', Discips[i])
        
        # Determine the extent to which points pass and fail
        Discips[i] = outchk.rmsFail()
        
        # Reset discipline's reduction counter to 0 and criteria to defaults
        Discips[i]['force_reduction'][0] = False
        Discips[i]['force_reduction'][1] = 0
        Discips[i]['part_params'] = copy.deepcopy(part_params)
    
    # Reset all of the fragility input rules back to an empty list
    irules_fragility = []
    
    # Make a copy of the disciplines for fragility-tracking purposes
    Discips_fragility = copy.deepcopy(Discips)
    
    # Track the time of the fragility copy
    time_fragility = iters
    
    # Increase the time count
    iters += temp_amount
    
    # Initialize dictionaries for pass-fail information
    pf = {None: [{'non_reduced': np.empty(0)} for _ in Discips]}
    pf_std = {None: [{'non_reduced': np.empty(0)} for _ in Discips]}
    
    # Initialize a dictionary for capturing gradients at explored points
    grads = {None: [None for _ in Discips]}
    
    # Initialize a dictionary for capturing explored points in each discipline
    x_explored = {None: [{'non_reduced': np.empty(0)} for _ in Discips]}
    y_explored = {None: [{'non_reduced': np.empty(0)} for _ in Discips]}
    
    # Form pass-fail predictions for remaining design space with new points
    if not fragility_extensions['interdependencies']:
        for i, discip in enumerate(Discips):
            pf[None][i]['non_reduced'], pf_std[None][i]['non_reduced'], \
                grads[None][i], x_explored[None][i]['non_reduced'], \
                y_explored[None][i]['non_reduced'] = \
                    getPerceptions(discip, gpr_params)
            pf[None][i]['indices'] = \
                copy.deepcopy(discip['space_remaining_ind'])
            pf_std[None][i]['indices'] = \
                copy.deepcopy(discip['space_remaining_ind'])
    else:
        pf_none, pf_std_none = connectPerceptions(Discips)
        for i, discip in enumerate(Discips):
            pf[None][i]['non_reduced'] = copy.deepcopy(pf_none[i])
            pf_std[None][i]['non_reduced'] = copy.deepcopy(pf_std_none[i])
            pf[None][i]['indices'] = \
                copy.deepcopy(discip['space_remaining_ind'])
            pf_std[None][i]['indices'] = \
                copy.deepcopy(discip['space_remaining_ind'])
    
    # Append all relevant information to time history
    passfail.append(copy.deepcopy(pf))
    passfail[-1]['time'] = iters
    passfail_std.append(copy.deepcopy(pf_std))
    passfail_std[-1]['time'] = iters
    Grads.append(copy.deepcopy(grads))
    Grads[-1]['time'] = iters
    X_explored.append(copy.deepcopy(x_explored))
    X_explored[-1]['time'] = iters
    Y_explored.append(copy.deepcopy(y_explored))
    Y_explored[-1]['time'] = iters
    
    # Reset the just explore value to False
    just_explore = False
    
    # Reset temporarily banned rules to an empty set
    banned_rules = set()


# Final check if any new input rules are being proposed
if irules_new: 
    
    # Move data within each discipline according to the new rule
    Discips = sortPoints(Discips, irules_new)
    
    # Gather points for space remaining data
    for ind_discip, dic_discip in enumerate(Discips):
        Space_Remaining[ind_discip].append({
            'iter': copy.deepcopy(iters),
            'space_remaining': copy.deepcopy(dic_discip['space_remaining'])
            })

# Add any new input rules to the list
Input_Rules += irules_new

# Write Space_Remaining data to an .hdf5 file
space_remaining_file_path = f"space_remaining_{unique_identifier}.hdf5"
with h5py.File(space_remaining_file_path, 'w') as hdf_file:
    for i, discipline_list in enumerate(Space_Remaining):
        for j, data_point in enumerate(discipline_list):
            iter_group=hdf_file.create_group(f"Discipline_{i}/Data_Point_{j}")
            iter_group.attrs['iter'] = data_point['iter']
            iter_group.create_dataset("space_remaining", 
                                      data=data_point['space_remaining'], 
                                      compression="gzip")

# Write Gradient_Factor to an .hdf5 file
gradient_factor_file_path = f"gradient_factor_{unique_identifier}.hdf5"
with h5py.File(gradient_factor_file_path, 'w') as hdf_file:
    for i, data_point in enumerate(Gradient_Factor):
        iter_group = hdf_file.create_group(f"Data_Point_{i}")
        iter_group.attrs['iter'] = data_point['iter']
        iter_group.create_dataset("gradient_factor", 
                                  data=data_point['gradient_factor'])

# Printing completion message to the redirected stdout
print(f"Simulation completed. Space remaining data saved to "
      f"{space_remaining_file_path}")

# Reset stdout to its original value and close the file
sys.stdout.close()
sys.stdout = original_stdout

# Print a message to console after resetting stdout
print(f"Simulation run completed successfully. "
      f"Unique ID: {unique_identifier}.")


