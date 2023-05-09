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
from exploration_check import checkSpace
from merge_constraints import mergeConstraints
from fragility_check import checkFragility
from exploration_amount import exploreSpace
from get_constraints import getConstraints, getInequalities
from create_key import createKey, createDict, createNumpy
from input_vals import getInput
from output_vals import getOutput
from calc_rules import calcRules
from output_success import checkOutput
#from save_data import save_dicts_to_files

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
iters_max = 1000    # Must be a positive integer!

# Decide on the strategy for producing random input values - may want to change
### this decision process up and have many selections in user inputs according
### to how the project is going
### OPTIONS: Uniform, LHS (eventually),...
sample = 'uniform'

# Decide on the run time (iterations) for each discipline's analysis
### Important to make sure that the length of the list coincides with the
### number of disciplines/equations there are in the design problem
run_time = [2, 3, 4]    # Must all be positive integers!

# Decide if the fragility of proposed reductions is to be assessed and the
# number of fragility assessments to allow before accepting a fragile space
# reduction
fragility = True    # True = yes, False = no
fragility_max = 5   # Must be a positive integer!

# Decide the number of forced reductions to be attempted before minimizing any
# criteria for a space reduction to be proposed
force_reduction_max = 5

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

# Assign the user input run time to each discipline
for i in range(0,len(run_time)):
    Discips[i]['time'] = run_time[i]

# Create an empty list for new rules to be added
irules_new = []

# Set the initial forced reduction value to false and establish a counter
force_reduction = False
force_reduction_counter = 0

# Begin the design exploration and reduction process with allotted timeline
while iters < iters_max:
    ###########################################################################
    ####################### SPACE REDUCTIONS / FRAGILITY ######################
    ###########################################################################
    # Add any new input rules to the list
    Input_Rules += irules_new
    
    # Reset the input rules to an empty list
    irules_new = []
    
    # Determine if any disciplines want to propose a space reduction
    # Call to exploration_check method and return list of all proposed
    # reductions without having merged any together
    space_check = checkSpace(Discips)
    # if iters > 0:
    #     irules_new =\
    #         space_check.getPartitions()
    #     print(irules_new)
    #     Clusters = space_check.createClusters(force_reduction_max)
        
    irules_new = [] # Placeholder...change empty list to checkSpace method call
    
    # Check if new input rules list is empty or not
    if irules_new:
        
        # If list not empty, merge proposed reduction(s) together into a
        # cohesive group
        merger = mergeConstraints(irules_new)
        irules_new = [] # Placeholder...change empty list to mergeConstraints method call
        
        # Initialize a fragility counter
        fragility_counter = 0
        
        # Run a fragility assessment if desired and while the fragility counter
        # is not maxed out
        while fragility and fragility_counter < fragility_max:
            
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
         
        ##### If reduction is not to be forced, continue on to exploring the design space for a determined
        ##### amount of time with an exploration amount method
        ##### Don't need anything here, just let code continue on to the
        ##### exploration section below
                
    
    ### If not, determine if the time remaining paired with the design space
    ### remaining warrants a space reduction to be forced
    ### Call to different method in exploration_check
    else:
        
        # If list is empty, determine if a space reduction should be forced
        # based on the time and design spaces that remain
        force_reduction = False # Placeholder...change boolean to checkSpace method call
        
        ##### If space reduction should be forced, adjust each discipline's criteria for proposing a space
        ##### reduction and return to the top of this sequence
        if force_reduction:
            pass # Placeholder...change to checkSpace method call to adjust criteria
            # DO NOT CHANGE FORCE_REDUCTION BACK TO FALSE HERE
            force_reduction_counter += 1 # This counter is not needed in the fragility loop
            # because a forced reduction will not leave the fragility loop until
            # a space reduction is actually made and committed to 
            continue
        ##### If no, move on to exploring the design space for a determined
        ##### amount of time with an exploration amount method
        ##### Don't need anything here, just let code continue on to the
        ##### exploration section below
            
    
    

    
    
    
    
    ###########################################################################
    ############################### EXPLORATION ###############################
    ###########################################################################
    # Determine the amount of time/iterations for disciplines to explore
    space_amount = exploreSpace(iters,iters_max,run_time)
    temp_amount = space_amount.fixedExplore()
    print("Current Exploration Time: " + str(temp_amount) +\
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
    
    # Increase the time count
    iters += temp_amount
    
    # Reset the reduction count to 0
    force_reduction_counter = 0
    
    # Reset each discipline's criteria for a space reduction?  Add box to the flowchart?



# Choose the final design or the final group of designs