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


"""
USER INPUTS
"""
# List the name of the problem on which the design team is working
### OPTIONS: SBD1,...
problem_name = "SBD1"

# Establish a timeline for exploring the design problem
### This value determines the number of loop iterations that will be executed,
### but it does not necessarily mean each point tested will only take one
### iteration to complete.
iters = 2

# Actually assign a random interval with the other disciplines where each discipline will
# propose a reduction...or assign a Joint preference criterion for when a discipline is allowed
# to request a reduction...and then see if other disciplines might also want to propose
# reductions too, just for a lower criterion?


"""
COMMANDS
"""
# Establish dictionaries for the design problem of interest
prob = setProblem()
Problem, Set_rules = prob.SBD1()

# Set the total project exploration and reduction timeline - change to while loop?
for i in range(0,iters):
        
    # Get random inputs for each input variable
    random = getInput(Problem,Set_rules,iters)
    Problem = random.getUniform()
    print(Problem[0])
    
    # Calculate and record outputs for each design point in the input space
    
    
    














# Randomly sample each design space...track points in discipline dictionary?



# Randomly request a reduction at a point in time?



# Randomly propose a certain number of reductions?








