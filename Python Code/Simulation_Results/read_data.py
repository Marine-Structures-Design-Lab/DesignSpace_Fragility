"""
SUMMARY:
Reads all of the space remaining data from each test case and gathers passing
and failing information of original space remaining arrays for each discipline
from SBD1 problem.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
# Import python libraries
import os
import sys
import pickle

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.append(parent_dir)

# Import desired functions / classes
from output_success import checkOutput
from vars_def import setProblem
from create_key import createKey
from get_constraints import getConstraints
from output_vals import getOutput
from design_changes import changeDesign


"""
READ DATA
"""
# Save the current directory's path
original_dir = os.getcwd()

# Read in the data from Test Case 1
os.chdir('./Test Case 1/Space_Remaining')
with open('load_data.py') as file:
    exec(file.read())

# Change back to the original directory
os.chdir(original_dir)

# Read in the data from Test Case 2
os.chdir('./Test Case 2/Space_Remaining')
with open('load_data.py') as file:
    exec(file.read())

# Change back to the original directory
os.chdir(original_dir)

# Read in the data from Test Case 3
os.chdir('./Test Case 3/Space_Remaining')
with open('load_data.py') as file:
    exec(file.read())

# Change back to the original directory
os.chdir(original_dir)


"""
POST-PROCESS
"""
# Establish disciplines and rules for the design problem of interest
prob = setProblem()
Discips, Input_Rules, Output_Rules = prob.SBD1()

# Loop through each discipline of the design problem
for i in range(0, len(Discips)):
    
    # Create a key for tested inputs of discipline if it does not exist
    Discips[i] = createKey('tested_ins', Discips[i])
    
    # Populate tested inputs with each initial space remaining array
    Discips[i]['tested_ins'] = Test_Case_1['Run_1'][i][0]['space_remaining']
    
    # Create a key for tested outputs of discipline if it does not exist
    Discips[i] = createKey('tested_outs', Discips[i])
    
    # Get output points from equations
    outpts = getOutput(Discips[i])
    Discips[i] = outpts.getValues()
    
    # Determine current output value rules for the discipline to meet
    output_rules = getConstraints(Discips[i]['outs'], Output_Rules)
    
    # Create a key for passing and failing of outputs if it does not exist
    Discips[i] = createKey('pass?', Discips[i])
    
    # Check whether the output points pass or fail
    outchk = checkOutput(Discips[i], output_rules)
    Discips[i] = outchk.basicCheck()


"""
SAVE DATA
"""
# Saving the objects
with open('Discips.pkl', 'wb') as f:
    pickle.dump(Discips, f)

with open('Test_Case_1.pkl', 'wb') as f:
    pickle.dump(Test_Case_1, f)

with open('Test_Case_2.pkl', 'wb') as f:
    pickle.dump(Test_Case_2, f)

with open('Test_Case_3.pkl', 'wb') as f:
    pickle.dump(Test_Case_3, f)
