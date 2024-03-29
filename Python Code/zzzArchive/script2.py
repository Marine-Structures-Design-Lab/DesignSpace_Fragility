"""
DESCRIPTION:
Main script file for simulating the space reduction process of a convergent
design approach (geared towards Set-Based Design).  In this file, a design
problem is presented with various discipline's and design variables.  An
automated process is established to explore and propose reductions for each
discipline's design space, and then the design manager merges these proposed
reductions among interdependent disciplines with the goal of converging on a
final, optimal design.

The design manager has the option to call on a fragility framework to analyze
the vulnerability of remaining design spaces before committing to a reduction
decision.  This script file can call on this framework while also importing
classes and functions to make this set-based design and fragility assessment
process as modular as possible for various design problems.

This script is currently coded to handle the Set-Based Design problem involving
three disciplines and various mathematical equations as described in the
prospectus document that can be accessed through the link provided in this
repository's README file.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from vars_def import setProblem
from uniform_grid import uniformGrid
from exponential_reduction import plotExponential
from point_sorter import sortPoints, sortPoints2
from exploration_check import checkSpace
from merge_constraints import mergeConstraints
from space_prediction import predictSpace
from reduction_change import changeReduction
from fragility_check import checkFragility
from exploration_amount import exploreSpace
from get_constraints import getConstraints, getInequalities
from create_key import createKey, createDict, createNumpy
from input_vals import getInput
from output_vals import getOutput
from calc_rules import calcRules
from output_success import checkOutput
import numpy as np
import copy


"""
USER INPUTS
"""
# List the name of the problem on which the design team is working
### OPTIONS: SBD1,...
problem_name = 'SBD1'

# Establish the allowed timeline for exploring the design problem
### This value determines the number of time iterations that will be executed,
### but it does not necessarily mean each explored point tested will only take
### one iteration to complete.
iters_max = 100    # Must be a positive integer!

# Decide on the strategy for producing random input values - may want to change
### this decision process up and have many selections in user inputs according
### to how the project is going
### OPTIONS: Uniform, LHS (eventually),...
sample = 'uniform'

# Decide the approximate number of points that you want to use to estimate the
### space remaining in each discipline - more points will increase execution
### time of program but provide more accurate approximations of space remaining
### following any space reductions
total_points = 10000

# Decide on the run time (iterations) for each discipline's analysis
### Important to make sure that the length of the list coincides with the
### number of disciplines/equations there are in the design problem
run_time = [2, 3, 4]    # Must all be positive integers!

# Choose desired fragility tracking method

# Decide if the fragility of proposed reductions is to be assessed and the
# number of fragility assessments to allow before accepting a fragile space
# reduction
fragility = True    # True = yes, False = no
fragility_max = 5   # Must be a positive integer!

# Set exponential function parameters dictating minimum space reduction pace
exp_parameters = np.array(\
    [0.2,  # p1: x-intercept (0 <= p1 < p3)
     5.0,  # p2: Steepness (any real, positive number)
     1.0,  # p3: Max percent of time to force reductions (p1 < p3 <=1)
     0.95]) # p4: Percent of space reduced at max reduction time (0 <= p4 <= 1)

# Set initial values for creating and evaluating the suitability of partitions
# ERROR ON THE SIDE OF STARTING THESE LOW AND HAVING ADJUST CRITERIA ALTER THEM
part_params = {
    "cdf_crit": 0.1,
    "fail_crit": 0.0,
    "dist_crit": 0.2,
    "disc_crit": 0.2
    }







"""
COMMANDS
"""

###############################################################################
################################ PROBLEM SETUP ################################
###############################################################################

# Establish disciplines and initial rules for the design problem of interest
prob = setProblem()
Discips, Input_Rules, Output_Rules = getattr(prob,problem_name)()

# Establish a counting variable that keeps track of the amount of time passed
iters = 0

# Loop through each discipline
for i in range(0,len(Discips)):
    
    # Assign run time to each discipline
    Discips[i]['time'] = run_time[i]
    
    # Assign default partition parameters to each discipline
    Discips[i]['part_params'] = copy.deepcopy(part_params)
    
    # Initialize a force reduction boolean value and counter to each discipline
    Discips[i]['force_reduction'] = [False, 0]
    
    # Initialize an array for estimating the space remaining for the discipline
    Discips[i]['space_remaining'], tp_actual = \
        uniformGrid(total_points, len(Discips[i]['ins']))

# Print a visual of the minimum space reduction vs. time remaining pace
plotExponential(exp_parameters)

# Create an empty list for new rules to be added
irules_new = []

# Set the initial forced reduction value to false and establish a counter
### THESE MAY NOT BE NEEDED LATER
force_reduction = False
force_reduction_counter = 0

# Begin the design exploration and reduction process with allotted timeline
while iters < iters_max:
    
    # Break while loop if any discipline has maxed out partition parameters
    break_loop = False
    for dic in Discips:
        part_params = dic["part_params"]
        if all(value >= 1.0 for value in part_params.values()):
            break_loop = True
            break
    if break_loop:
        break
    
    ###########################################################################
    ####################### SPACE REDUCTIONS / FRAGILITY ######################
    ###########################################################################
    
    # Add any new input rules to the list
    if iters > 0 and irules_new: Discips = sortPoints(Discips, irules_new)
    Input_Rules += irules_new
    
    # Reset the input rules to an empty list
    irules_new = []
    
    # Loop through each disicipline
    for i in range(0,len(Discips)):
        
        # Skip reduction considerations if no tested points with which to work
        if 'tested_ins' not in Discips[i] or \
            np.shape(Discips[i]['tested_ins'])[0] == 0: continue
        
        # Initialize an object for the checkSpace class
        space_check = checkSpace(Discips[i]['ins'], max_depth=2)
        
        # Produce array of "good" and "bad" values based on CDF threshold
        gb_array = space_check.goodBad(Discips[i]['Fail_Amount'],\
                       Discips[i]['part_params']['cdf_crit'])
        
        # Build the decision tree
        space_check.buildTree(Discips[i]['tested_ins'], gb_array)
        
        # Gather inequalitie(s) from the decision tree as a potential rule
        pot_rule = space_check.extractRules(\
                     Discips[i]['tested_ins'].astype(np.float32), gb_array)
        
        # Check if the rule meets the current criteria to be proposed
        rule_check = space_check.reviewPartitions(\
            Discips[i]['tested_ins'], pot_rule,\
            Discips[i]['Fail_Amount'],\
            Discips[i]['part_params']['fail_crit'],\
            Discips[i]['part_params']['dist_crit'],\
            Discips[i]['part_params']['disc_crit'])
        
        # Add potential rule to the new rule list if it meets the criteria
        if rule_check:
            irules_new.append(space_check.prepareRule(pot_rule))
    
    # Check up on new rules
    print("Newly proposed input rules: " + str(irules_new))
    
    # Check if new input rules list is filled with any rules
    if irules_new:
        
        # If list not empty, merge proposed reduction(s) together into a
        # cohesive group
        merger = mergeConstraints(irules_new)
        irules_new = merger.removeContradiction()
        
        # Initialize a fragility counter
        fragility_counter = 0
        
        # Run a fragility assessment if desired and while the fragility counter
        # is not maxed out
        while fragility and fragility_counter < fragility_max:
            
            # Loop through each discipline
            for i in range(0, len(Discips)):
                
                # Gather all input and output data thus far
                elim_xray = Discips[i].get('eliminated',{}).get('tested_ins',\
                                 np.empty((0, len(Discips[i]['ins']))))
                elim_ypass = Discips[i].get('eliminated',{}).get('pass?', [])
                x_train = np.concatenate(\
                              (Discips[i]['tested_ins'], elim_xray), axis=0)
                y_train = Discips[i]['pass?'] + elim_ypass
                
                # Initialize Gaussian Process Classifier (GPC) for feasibility
                predictor = predictSpace(Discips[i]['ins'])
                
                # Train GPC with x-input and pass/fail data
                trained_bool = predictor.trainFeasibility(x_train, y_train)
                
                # Check GPC has been trained and space remaining not empty
                if trained_bool and Discips[i]['space_remaining'].shape[0] > 0:
                    
                    # Predict probability of feasibility of points remaining
                    pof = predictor.predictProb(Discips[i]['space_remaining'])
                    
                    # Gather each combination of input variables
                    var_combos = predictor.createCombos()
                    
                    # Gather feasible point stats for each combo of variables
                    var_combos = predictor.feasStats(var_combos, \
                        Discips[i]['space_remaining'], pof, tp_actual)
                    
                    # Create a duplicate discipline (Need to edit code from this point on so only feasStats method is performed twice...not createCombos or predictProb)
                    disc_dup = copy.deepcopy(Discips[i])
                    
                    # Eliminate points from the duplicate discipline
                    disc_dup = sortPoints2(disc_dup, irules_new)
                    
                    # Gather feasible points stats for reduced design space
                    pof2 = predictor.predictProb(disc_dup['space_remaining'])
                    var_combos2 = predictor.createCombos()
                    var_combos2 = predictor.feasStats(var_combos2, disc_dup['space_remaining'], pof2, tp_actual)
                    
                    # Compare feasible designs before and after the reduction
                    var_diff = {key: var_combos[key] - var_combos2[key] for key in var_combos if key in var_combos2}
                    print(var_diff)
                    
                
                
                
            
            # Execute fragility assessment and increase fragility counter by 1
            fragile = checkFragility()
            isfragile = fragile.basicCheck()
            fragility_counter += 1
            
            # If fragility is all good, break fragility loop
            if not isfragile:
                break
            
            # If fragility bad, but reduction not forced, break fragility loop
            elif not force_reduction:
                break
            
            # If fragility bad, and reduction forced, revise and try again
            else:
                # Call another method from checkFragility for determining why fragile
                # Call another method from checkFragility for revising the irules_new reduction
                pass
            
        # If no fragility check, fragility counter maxed out, or not fragile,
        # continue with the proposed/last revised reduction
        if not fragility or fragility_counter>=fragility_max or not isfragile:
            force_reduction = False
            force_reduction_counter = 0
            # Reset criteria for space reduction?
            continue
            
        # If reduction is not forced, check if it should be (Turn code in elif into function call because code repeated below!)
        elif not force_reduction:
            force_reduction = False # Placeholder...change boolean to checkSpace method call
            irules_new = []
            
            # Adjust criteria for proposing space reduction if should be forced
            if force_reduction:
                pass # Placeholder...change to checkSpace method call to adjust criteria
                # DO NOT CHANGE FORCE_REDUCTION BACK TO TRUE HERE
                # DO NOT INCREASE FORCE REDUCTION COUNTER BY 1 HERE
                continue
         
                
    
    ### If no rules, determine if time remaining paired with the design space
    ### remaining warrants a space reduction to be forced
    else:
        
        # Create an object for the changeReduction class
        red_change = changeReduction(Discips)
        
        # Estimate the space remaining in each discipline
        space_rem = red_change.estimateSpace(tp_actual)
        
        # Check if a space reduction should be forced
        Discips = red_change.forceReduction(space_rem, iters, iters_max, exp_parameters)
        
        # Perform the following commands if a space reduction should be forced
        if any(dictionary.get("force_reduction", False)[0] == True\
               for dictionary in Discips):
            
            # Adjust the criteria for the necessary discipline(s)
            Discips = red_change.adjustCriteria()
            
            # DO NOT CHANGE FORCE_REDUCTION BACK TO FALSE HERE
            force_reduction_counter += 1 # This counter is not needed in the fragility loop
            # because a forced reduction will not leave the fragility loop until
            # a space reduction is actually made and committed to 
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
        input_rules = getConstraints(Discips[i]['ins'],Input_Rules)
        
        # Create a key for tested inputs of discipline if it does not exist
        Discips[i] = createKey('tested_ins',Discips[i])
        
        # Get input points according to the desired strategy
        inppts = getInput(Discips[i],input_rules,temp_amount,i)
        Discips[i] = inppts.getUniform()
        
        # Create a key for tested outputs of discipline if it does not exist
        Discips[i] = createKey('tested_outs',Discips[i])
        
        # Get output points from equations or black-box programs
        outpts = getOutput(Discips[i])
        Discips[i] = outpts.getValues()
        
        # Create a key for the output rule inequalities relevant to discipline
        Discips[i] = createDict('out_ineqs',Discips[i])
        
        # Determine current output value rules for the discipline to meet
        output_rules = getConstraints(Discips[i]['outs'],Output_Rules)
        
        # Gather any new inequalities of relevance to the discipline
        Discips[i] = getInequalities(Discips[i],output_rules,'out_ineqs')
        
        # Calculate left-hand side of output rule inequality for each new point
        Discips[i]['out_ineqs'] = calcRules(Discips[i],\
                                            'out_ineqs','tested_outs','outs')

        # Create a key for passing and failing of outputs if it does not exist
        Discips[i] = createKey('pass?',Discips[i])
        
        # Check whether the output points pass or fail
        outchk = checkOutput(Discips[i],output_rules)
        Discips[i] = outchk.basicCheck()
        
        # Create a key for extent of passing/failing if it does not exist
        Discips[i] = createNumpy('Fail_Amount',Discips[i])
        
        # Determine the extent to which failing points fail
        Discips[i] = outchk.rmsFail()
        
        # Reset discipline's reduction counter to 0 and criteria to defaults
        Discips[i]['force_reduction'][1] = 0
        Discips[i]['part_params'] = copy.deepcopy(part_params)
        
        # Reset force reduction to False?
    
    # Increase the time count
    iters += temp_amount
    
    # Reset the reduction counter to 0
    force_reduction_counter = 0
    
    # Reset each discipline's criteria for a space reduction?  Add box to the flowchart?










####################################TEMPORARY##################################
# Visualize the points in the space remaining
import matplotlib.pyplot as plt

# Loop through each discipline
for i in range(0,len(Discips)):
    
    # Print percent of space that remains in discipline
    print(f"Discipline {i+1} has "
      f"{round((np.shape(Discips[i]['space_remaining'])[0]/tp_actual)*100, 2)}"
      f"% of its original design space remaining")

    # Initialize an empty list for storing numpy arrays
    l = []
    
    # Surface plot
    j = np.linspace(0, 1, 4000)
    k = np.linspace(0, 1, 4000)
    j, k = np.meshgrid(j, k)
    
    if i == 0:
        l.append(0.8*j**2 + 2*k**2 - 0.0)
        l.append(0.8*j**2 + 2*k**2 - 0.4)
        l.append(0.8*j**2 + 2*k**2 - 1.2)
        l.append(0.8*j**2 + 2*k**2 - 1.6)
    elif i == 1:
        l.append((12.5*j**3-6.25*j**2+0.5)/1.25)
        l.append((12.5*j**3-6.25*j**2+0.7)/1.25)
        l.append(-k**3+np.sqrt(0.2))
        l.append(-k**3+np.sqrt(0.5))
    else:
        l.append((2*j+0.2*np.sin(25*k)-0.0)**5)
        l.append((2*j+0.2*np.sin(25*k)-0.5)**5)
        l.append((np.cos(3*j)+0.8)**3)
        l.append((np.cos(3*j)+1.6)**3)
    
    # Replace out-of-bounds z_values with np.nan
    l = [np.where((z >= 0) & (z <= 1), z, np.nan) for z in l]
    
    # Initialize plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot every surface
    for m in range(0,len(l)):
        ax.plot_surface(j, k, l[m], alpha=0.5, rstride=100, cstride=100)
    
    # Accumulate the data
    ax.scatter(Discips[i]['space_remaining'][:,0], Discips[i]['space_remaining'][:,1], Discips[i]['space_remaining'][:,2])
    
    # Set axis limits
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.set_zlim([0, 1])
    
    # Set labels and title
    ax.set_xlabel(Discips[i]['ins'][0])
    ax.set_ylabel(Discips[i]['ins'][1])
    ax.set_zlabel(Discips[i]['ins'][2])
    ax.set_title('Discipline '+ str(i+1) + ' Remaining Input Space')
    
    # Show plot
    plt.show()

###############################################################################
# Choose the final design or the final group of designs