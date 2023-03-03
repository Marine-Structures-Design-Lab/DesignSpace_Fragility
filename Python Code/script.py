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
from input_vals import getInput
from get_constraints import getConstraints
from exploration_check import checkSpace
from exploration_amount import exploreSpace

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
iters_max = 2

# Decide on the strategy for producing random input values - may want to change
### this decision process up and have many selections in user inputs according
### to how the project is going
### OPTIONS: Uniform, LHS (eventually),...
sample = 'uniform'


"""
COMMANDS
"""
# Establish dictionaries for the design problem of interest
prob = setProblem()
Discips, Set_rules = getattr(prob,problem_name)()

# Establish a counting variable that keeps track of the amount time passed
iters = 1

# Begin the design exploration and reduction process with allotted timeline - 
# NEED TO ADD A BOOLEAN CLASS TO THIS FOR ASSESSING IF DESIGN SPACES HAVE BEEN
# SUFFICIENTLY REDUCED
while iters <= iters_max:
        
        
    temp_amount = 0
    
    # Continue to explore each discipline's design case while condition(s) met
    ### - exploration_check.py - True is a placeholder right now
    temp_bool = True
    space_check = checkSpace() # Establish the first space_check here...but
    # later may want to reinitialize and call a different method depending on
    # the results at the end of the while loop below
    while(temp_bool):
        
        # Determine the amount of time/iterations for disciplines to go through
        ### this go around when generating points - exploration_amount.py
        space_amount = exploreSpace() # Also establishing first space_amount
        # here...but later may want to reinitialize and call a different method
        # depending on the results at the end of the while loop above
        temp_amount += iters_max # This will change to a method call from the
        # exploreSpace class
        
        # Loop through each discipline (maintaining each of their independence)
        for i in range(0,len(Discips)):
            
            # Determine current input value rules for the discipline to meet
            input_rules = getConstraints(Discips[i]['ins'],Set_rules)  
            
            # Create a key for tested inputs of discipline if does not exist
            if 'tested_ins' in Discips[i]:
                continue
            else:
                Discips[i]['tested_ins'] = []
            
            # Loop through each time iteration
            for j in range(0,temp_amount):
                
                # Get input points according to the desired strategy
                inppts = getInput(Discips[i],input_rules,temp_amount)
                ### (Failed attempts for random point creation should not count
                ###  against iteration time)
        
        temp_bool = False
            
                
                    
                    # Prevent infinite while loop from occurring with error message
                    
                    # Get temporary random inputs for each input
                    
                    # Check that temporary random inputs meet the current rules
                    
                    # Add temporary random inputs to tested inputs or 
        
    ###### CODE TO PROPOSE SPACE REDUCTIONS ######
    
    
    ###### OPTIONAL CODE TO BRING FRAGILITY FRAMEWORK INTO PLAY ######
    
    
    ###### OPTIONAL CODE TO INTRODUCE DESIGN CHANGES THAT DO ACTUALLY OCCUR
    ###### AND ARE NOT JUST SIMULATED AS A POSSIBILITY IN FRAGILITY FRAMEWORK
    
    
    
    
    # Increase the time count - THE 1 WILL NEED TO CHANGE DEPENDING ON EXPLORATION TYPE AND AMOUNT
    iters += temp_amount

