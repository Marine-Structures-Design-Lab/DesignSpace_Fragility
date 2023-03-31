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
from get_constraints import getConstraints
from create_key import createKey
from exploration_amount import exploreSpace
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

# Begin the design exploration and reduction process with allotted timeline - 
### Later I may want to also end exploration if happy design spaces have been
### sufficiently reduced
while iters < iters_max:
    
    ################### WHILE LOOP WITH CONTINUE STATEMENTS ###################
    # Determine if any disciplines want to propose a space reduction
    # Call to exploration_check method and return a true or false value
    ### If yes, collect proposed reduction(s) from each discipline and merge
    ### them together into a cohesive group
    ### Call to merge constraints class/method
    ##### Determine if design manager wants to run a fragility assessment
    ##### (probably with just a true or false user input value and a counter)
    ####### If yes, insert fragility framework here and try different methods!
    ######### If fragility all good, continue with proposed reduction and
    ######### update the rules by calling the new constraints class/method
    ######### If fragility not good and the reduction was not forced, forgo the
    ######### reduction and continue to asking if a reduction should be forced
    ######### If fragility not good and the reduction was forced, then need to
    ######### revise the proposed reduction and check fragility again...will
    ######### need to fail safe here for ensuring an infinite while loop does
    ######### not occur
    ####### If no, continue with the proposed reduction and update the rules by
    ####### calling the new constraints class/method
    ### If not, determine if the time remaining paired with the design space
    ### remaining warrants a space reduction to be forced
    ### Call to different method in exploration_check
    ##### If yes, adjust each discipline's criteria for proposing a space
    ##### reduction and return to the top of this sequence
    ##### Call to another different method in exploration check
    ##### If no, continue on to exploring the design space for a determined
    ##### amount of time with a exploration amount method

    
    ######## UPDATE THE FLOWCHART WITH ALL OF THE ABOVE!!!!!!########
    ######## SCRIPT FILE WILL NEED A UTEST TO MAKE SURE ALL OF THE DIFFERENT
    ######## BRANCHES ARE GOING IN THE CORRECT DIRECTION
    
    
    # Establish variables for keeping track of total iteration time
    temp_amount = 0
    full_amount = 0
    
    # Continue to explore each discipline's design case while condition(s) met
    temp_bool = True
    space_check = checkSpace() # Establish the first space_check here...but
    # later may want to reinitialize and call a different method depending on
    # the results at the end of the while loop below
    while(temp_bool):
        
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
            
            # Determine what (if any) space reductions the discipline proposes
            
        
        # Add time spent exploring to the count
        full_amount += temp_amount
        temp_bool = False
        
        
        
    
    
    ###### OPTIONAL CODE TO INTRODUCE DESIGN CHANGES THAT DO ACTUALLY OCCUR
    ###### AND ARE NOT JUST SIMULATED AS A POSSIBILITY IN FRAGILITY FRAMEWORK
    
    
    
    
    # Increase the time count
    iters += full_amount




# Choose the final design or the final group of desings