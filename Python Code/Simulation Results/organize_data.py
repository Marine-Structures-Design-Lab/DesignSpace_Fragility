# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 14:06:34 2024

@author: joeyvan
"""

"""
LIBRARIES
"""
import matplotlib.pyplot as plt
import os
import sys
import numpy as np
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


"""
SECONDARY FUNCTIONS
"""
def sharedIndices(larger_array, smaller_array):
    
    # Initialize an empty list to store indices
    indices = []
    
    # Iterate over each row in the smaller array
    for row in smaller_array:
        
        # Find the index in the larger array where the row matches
        index = np.where((larger_array == row).all(axis=1))[0][0]
        indices.append(index)
    
    return indices






"""
MAIN FUNCTIONS
"""
# Determine all times data was collected for test case - consult console output
def createTimeData(test_case_name):
    
    if test_case_name == 'Test_Case_1' or test_case_name == 'Test_Case_2':
        set_of_times = {0, 40, 68, 91, 107, 118, 127, 135, 143, 151, 159, 167, 
                        175, 183, 191, 199, 200}
    else:
        set_of_times = {0, 200, 344, 462, 542, 596, 644, 679, 711, 731, 749, 
                        766, 782, 797, 811, 819, 827, 835, 843, 851, 859, 867, 
                        875, 883, 891, 899, 907, 915, 923, 931, 939, 947, 955, 
                        963, 971, 979, 987, 995, 1000}
    
    # Return the set of times
    return set_of_times


def fillSpaceRemaining(test_case, set_of_times, Discips):
    
    # Create a list of the times and sort them in ascending order
    list_of_times = sorted(list(set_of_times))
    
    # Initialize an empty dictionary for space remaining data
    space_rem = {}
    
    # Initialize an empty dictionary for percentage of feasible space data
    feas_space = {}
    
    # Loop through each run of the test case
    for run_name, discips in test_case.items():
        
        # Initialize empty dictionaries for the run
        space_rem[run_name] = {}
        feas_space[run_name] = {}
        
        # Loop through each discipline of the run
        for ind_discip, list_discip in enumerate(discips):
            
            # Create a name for the discipline based on the index of the data
            discip_name = f"Discipline_{ind_discip + 1}"
            
            # Initialize empty dictionaries for the discipline
            space_rem[run_name][discip_name] = {}
            feas_space[run_name][discip_name] = {}
            
            # Loop through each value in the list of times
            for time in list_of_times:
                
                # Assign time to a key for the dictionaries
                space_rem[run_name][discip_name][time] = []
                feas_space[run_name][discip_name][time] = []
            
            # Loop through each data point in the list
            for ind_data, dic_data in enumerate(list_discip):
                
                # Add size of the numpy array to the proper iteration list
                space_rem[run_name][discip_name][dic_data['iter']].append\
                    (len(dic_data['space_remaining']))
                
                # Determine shared indices between space remaining arrays
                # matches = sharedIndices(Discips[ind_discip]['tested_outs'], dic_data['space_remaining'])
                
                # Count True and False values for indices in both
                
                
                
                # Feasibility analysis function based on True and False Values!!!
                
                
                
                
                
            
            # Loop back through the list of times
            for ind_time, time in enumerate(list_of_times):
                
                # Check if list is empty
                if not space_rem[run_name][discip_name][time]:
                    
                    # Add minimum time from one earlier time
                    space_rem[run_name][discip_name][time].append(min(\
                        space_rem[run_name][discip_name][list_of_times\
                        [ind_time-1]]))
    
    # Return the dictionary of filled in time information
    return space_rem


def findAverages(space_rem):
    
    # Initialize an empty dictionary for average space remaining data
    average_rem = {}
    
    # Loop through each discipline
    for discip_name, sr_dic in space_rem['Run_1'].items():
        
        # Initialize an empty dictionary for the discipline
        average_rem[discip_name] = {}

        # Loop through each time that space remaining data is accounted for
        for time, sr_set in sr_dic.items():
            
            # Initalize a time key for summation part of averaging
            average_rem[discip_name][time] = 0.0
    
    # Loop through each run of the test case
    for run_name, discips in space_rem.items():
        
        # Loop through each discipline of the run
        for discip_name, sr_dic in discips.items():
            
            # Loop through each time that space remaining data is accounted for
            for time, sr_lis in sr_dic.items():
                
                # Add midpoint of the space remaining to the proper summation
                average_rem[discip_name][time] += (min(sr_lis) + max(sr_lis))/2
        
    # Loop through each discipline
    for discip_name, ar_dic in average_rem.items():
        
        # Loop through each time that space remaining data is accounted for
        for time in ar_dic.keys():
            
            # Divide summation by the number of test cases run
            average_rem[discip_name][time] = \
                average_rem[discip_name][time] / len(space_rem)
            
    # Return the data for the average space remaining at each time
    return average_rem


def findPercentages(average_rem):
    
    # Initialize an empty dictionary for percent of space remaining data
    percent_rem = {}
    
    # Loop through each discipline
    for discip_name, ar_dic in average_rem.items():
        
        # Initialize an empty dictionary for the discipline
        percent_rem[discip_name] = {}
        
        # Loop through each time that average remaining is accounted for
        for time, ar in ar_dic.items():
            
            # Compute the percentage of the average space remaining
            percent_rem[discip_name][time] = ar / ar_dic[0] * 100
    
    # Return the percentage of the average space remaining
    return percent_rem


# I WANT TEST CASES IN LEGEND BY COLOR...AND THEN I'LL EXPLAIN IN CAPTION SOLID VS DASHED VS STARRED LINES FOR SPACE REMAINING, FEASIBLE, INFEASIBLE
def plot_disciplines(all_disciplines_data):
    for discipline, test_cases_data in all_disciplines_data.items():
        plt.figure(figsize=(10, 6))  # Create a new figure for each discipline
        
        for test_case, data_points in test_cases_data.items():
            # Sort the data points by iteration number (x-axis)
            sorted_data_points = sorted(data_points.items(), key=lambda x: x[0])
            
            # Calculate the percentage of time spent
            max_iteration = max(sorted_data_points, key=lambda x: x[0])[0]
            x_values = [iteration / max_iteration * 100 for iteration, _ in sorted_data_points]
            y_values = [value for _, value in sorted_data_points]
            
            # Plot the line for this test case
            plt.plot(x_values, y_values, label=test_case)
        
        plt.title(f'{discipline} - Percentage of Space Remaining Over Time')
        plt.xlabel('Percentage of Time Spent (%)')
        plt.ylabel('Percentage of Space Remaining (%)')
        plt.xlim([0, 100])
        plt.ylim([0, 100])
        plt.legend()
        plt.grid(True)
        plt.show()




# Add list with pass and fail data to each run
# After this is added...can add most recent update to code from chatgpt
# Then can work on adding other test case data...move this function (create_plots) to Simulation_Results
# and have it pull from each folder...leave load data script in each folder though
def determine_feasibility(test_case, test_case_name):
    # MAKE A COPY OF THE FIRST ONE AND DO THE COPYING AND THE INDICES THING AGAIN SO I DON'T HAVE TO KEEP CHECKING FEASIBILITY!!!
    
    
    return










"""
POST-PROCESSING
"""
# Upload saved data
with open('Discips.pkl', 'rb') as f:
    Discips = pickle.load(f)

with open('Test_Case_1.pkl', 'rb') as f:
    Test_Case_1 = pickle.load(f)

with open('Test_Case_2.pkl', 'rb') as f:
    Test_Case_2 = pickle.load(f)

with open('Test_Case_3.pkl', 'rb') as f:
    Test_Case_3 = pickle.load(f)

with open('Test_Case_4.pkl', 'rb') as f:
    Test_Case_4 = pickle.load(f)

# Identify the test cases whose data will be assessed
test_case_names = ['Test_Case_1', 'Test_Case_2', 'Test_Case_3', 'Test_Case_4']
# test_case_names = ['Test_Case_1']

# Initialize a dictionary for data pertinent to each discipline
all_disciplines_data = {
    'Discipline_1': {},
    'Discipline_2': {},
    'Discipline_3': {}
    }

# Loop through each test case / name
for test_case_name in test_case_names:
    
    # Retrieve variable whose name matches the string
    test_case = globals()[test_case_name]
    
    # Determine all of the times when data was recorded
    set_of_times = createTimeData(test_case_name)
    
    # Determine space remaining at each one of those times for each test run
    space_rem = fillSpaceRemaining(test_case, set_of_times, Discips)
    
    # Determine average space remaining at each time over all of the runs
    average_rem = findAverages(space_rem)
    
    # Convert averages into percentages
    percent_rem = findPercentages(average_rem)
    
    # Loop through disciplines
    for discip_name in all_disciplines_data.keys():
        
        # Add results to new key within dictionary
        all_disciplines_data[discip_name][test_case_name] = \
            percent_rem[discip_name]

# Plot the results - This could probably be put elsewhere
plot_disciplines(all_disciplines_data)


