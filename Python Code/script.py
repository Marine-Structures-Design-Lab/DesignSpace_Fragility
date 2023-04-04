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
from new_constraints import newConstraints
from exploration_check import checkSpace
from merge_constraints import mergeConstraints
from fragility_check import checkFragility
from exploration_amount import exploreSpace
from get_constraints import getConstraints
from create_key import createKey
from input_vals import getInput
from output_vals import getOutput
from output_success import checkOutput

"""
USER INPUTS
"""
# List the name of the problem on which the design team is working
### OPTIONS: SBD1,...
problem_name = 'SBD1'

# Establish the allowed timeline for exploring the design problem
### This value determines the number of loop iterations that will be executed,
### but it does not necessarily mean each point tested will only take one
### iteration to complete.
iters_max = 100    # Must be a positive integer!

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
# number of fragility assessments to before accepting a fragile space reduction
fragility = True    # True = yes, False = no
fragility_max = 5   # Must be a positive integer!

"""
COMMANDS
"""
# Establish dictionaries for the design problem of interest
prob = setProblem()
Discips, Rules = getattr(prob,problem_name)()

# Establish a counting variable that keeps track of the amount of time passed
iters = 0

# Assign the user inputted run time to each discipline
for i in range(0,len(run_time)):
    Discips[i]['time'] = run_time[i]

# Create an empty list of object calls for new rules to be added
rules_new = []

# Set the initial forced reduction value to false
force_reduction = False

# Begin the design exploration and reduction process with allotted timeline
while iters < iters_max:
    
    ############ SPACE REDUCTIONS / FRAGILITY ##############
    # Add to or update the current list of rules
    Rules = newConstraints(Rules,rules_new)
    
    # Reset the new rules to an empty list, if not empty already
    rules_new = []
    
    # Determine if any disciplines want to propose a space reduction
    # Call to exploration_check method and return list of all proposed
    # reductions without having merged any together
    space_check = checkSpace()
    rules_new = [] # Placeholder...change empty list to checkSpace method call
    
    # Check if new rules list is empty or not
    if rules_new:
        
        # If list not empty, merge proposed reduction(s) together into a
        # cohesive group
        merger = mergeConstraints(rules_new)
        rules_new = [] # Placeholder...change empty list to mergeConstraints method call
        
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
                # Call another method from checkFragility for revising the rules_new reduction
                pass
            
        # If no fragility check, fragility counter maxed out, or not fragile,
        # continue with the proposed/last revised reduction
        if not fragility or fragility_counter>=fragility_max or not isfragile:
            force_reduction = False
            continue
            
        # If reduction is not forced, check if it should be (Turn code in elif into function call because code repeated below!)
        elif not force_reduction:
            force_reduction = False # Placeholder...change boolean to checkSpace method call
            
            # Adjust criteria for proposing space reduction if should be forced...ADD COUNTER TO IF CONDITION!
            if force_reduction:
                pass # Placeholder...change to checkSpace method call to adjust criteria
                # DO NOT CHANGE FORCE_REDUCTION BACK TO TRUE HERE
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
        ##### reduction and return to the top of this sequence...ADD COUNTER TO IF CONDITION!
        if force_reduction:
            pass # Placeholder...change to checkSpace method call
            # DO NOT CHANGE FORCE_REDUCTION BACK TO TRUE HERE
            continue
        ##### If no, move on to exploring the design space for a determined
        ##### amount of time with an exploration amount method
        ##### Don't need anything here, just let code continue on to the
        ##### exploration section below
            
    
    

    
    
    
    
    
    ############ EXPLORATION ##############
    # Determine the amount of time/iterations for disciplines to explore
    space_amount = exploreSpace(iters,iters_max,run_time)
    temp_amount = space_amount.fixedExplore()
    print(temp_amount)
    
    # Loop through each discipline (maintaining each of their independence)
    for i in range(0,len(Discips)):
        
        # Determine current input value rules for the discipline to meet
        input_rules = getConstraints(Discips[i]['ins'],Rules)
        
        # Create a key for tested inputs of discipline if does not exist
        Discips[i] = createKey('tested_ins',Discips[i])
        
        # Get input points according to the desired strategy
        inppts = getInput(Discips[i],input_rules,temp_amount,i)
        Discips[i] = inppts.getUniform()
        
        # Create a key for tested outputs of discipline if does not exist
        Discips[i] = createKey('tested_outs',Discips[i])
        
        # Get output points from equations or black-box programs
        outpts = getOutput(Discips[i])
        Discips[i] = outpts.getValues()
        
        # Determine current output value rules for the discipline to meet
        output_rules = getConstraints(Discips[i]['outs'],Rules)
        
        # Create a key for passing and failing of outputs if does not exist
        Discips[i] = createKey('pass?',Discips[i])
        
        # Create a key for extent of passing/failing if does not exist?
        
        # Check whether the output points pass or fail (and by how much?)
        outchk = checkOutput(Discips[i],output_rules)
        Discips[i] = outchk.basicCheck()
    
    # Increase the time count
    iters += temp_amount
    
    # Reset each discipline's criteria for a space reduction?  Add box to the flowchart?




# Choose the final design or the final group of designs