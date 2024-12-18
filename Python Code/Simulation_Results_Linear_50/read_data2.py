"""
SUMMARY:
Reads all of the gradient factor data from each TC of SenYang problem.

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


"""
READ DATA
"""
# Save the current directory's path
original_dir = os.getcwd()

# # Read in the data from Test Case 2
# os.chdir('./Test Case 2/Gradient_Factor')
# with open('load_data.py') as file:
#     exec(file.read())

# # Change back to the original directory
# os.chdir(original_dir)

# # Read in the data from Test Case 3
# os.chdir('./Test Case 3/Gradient_Factor')
# with open('load_data.py') as file:
#     exec(file.read())

# # Change back to the original directory
# os.chdir(original_dir)

# Read in the data from Test Case 4
os.chdir('./Test Case 4/Gradient_Factor')
with open('load_data.py') as file:
    exec(file.read())

# Change back to the original directory
os.chdir(original_dir)

# Read in the data from Test Case 5
os.chdir('./Test Case 5/Gradient_Factor')
with open('load_data.py') as file:
    exec(file.read())

# Change back to the original directory
os.chdir(original_dir)


"""
SAVE DATA
"""

# with open('Gradient_Factor_2.pkl', 'wb') as f:
#     pickle.dump(Gradient_Factor_2, f)

# with open('Gradient_Factor_3.pkl', 'wb') as f:
#     pickle.dump(Gradient_Factor_3, f)

with open('Gradient_Factor_4.pkl', 'wb') as f:
    pickle.dump(Gradient_Factor_4, f)

with open('Gradient_Factor_5.pkl', 'wb') as f:
    pickle.dump(Gradient_Factor_5, f)
