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
import numpy as np


"""
USER INPUTS
"""
# List the name of the problem on which the design team is working
### OPTIONS: SBD1,...
problem_name = 'SBD1'

# Establish a timeline for exploring the design problem
### This value determines the number of loop iterations that will be executed,
### but it does not necessarily mean each point tested will only take one
### iteration to complete.
iters = 2

# Decide on the strategy for producing random input values
### OPTIONS: Uniform, LHS (eventually),...
sample = 'uniform'


"""
COMMANDS
"""
# Establish dictionaries for the design problem of interest
prob = setProblem()
Discips, Set_rules = prob.SBD1()

# Set the total project exploration and reduction timeline - change to while loop?
for i in range(0,iters):
    
    # Loop through each discipline (maintaining each of their independence)
    for j in range(0,len(Discips)):
        
        # Determine the current input value rules for the discipline to meet
        input_rules = getConstraints(Discips[j]['ins'],Set_rules)  
        print(input_rules)
        
        # Create a key for tested inputs of discipline if does not exist
        if 'tested_ins' in Discips[j]:
            continue
        else:
            Discips[j]['tested_ins'] = []
        
        # Get input points according to the desired strategy
        
        
        
        # While loop for point creation
        ### (Failed attempts for random point creation should not count
        ###  against iteration time)
        
            
                
                # Prevent infinite while loop from occurring with error message
                
                # Get temporary random inputs for each input
                
                # Check that temporary random inputs meet the current rules
                
                # Add temporary random inputs to tested inputs or 
        
        
        
        
        
        
        
        
        
        
        
    # Get random inputs for each input variable of the discipline
    # random = getInput(Discips,Set_rules,iters)
    # Problem = random.getUniform()
    # print(Discips[0])
    
    # Calculate and record outputs for each design point in the input space
    
    
    














# Randomly sample each design space...track points in discipline dictionary?



# Randomly request a reduction at a point in time?



# Randomly propose a certain number of reductions?








