# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 14:06:34 2024

@author: joeyvan
"""

import numpy as np
import matplotlib.pyplot as plt
import os


# Determine all times when data was collected for the test case
def createTimeData(test_case):
    
    # Create empty set for all the times
    set_of_times = set()
    
    # Loop through each run of the test case
    for run_name, discips in test_case.items():
        
        # Loop through each instance of data being collected
        for data_ind, data_dic in enumerate(discips[0]):
            
            # Add to set of times that data was collected
            set_of_times.add(data_dic['iter'])
    
    # Return the set of times
    return set_of_times


def fillSpaceRemaining(test_case, set_of_times):
    
    # Create a list of the times and sort them in ascending order
    list_of_times = sorted(list(set_of_times))
    
    # Initialize an empty dictionary for space remaining data
    space_rem = {}
    
    # Loop through each run of the test case
    for run_name, discips in test_case.items():
        
        # Initialize an empty dictionary for the run
        space_rem[run_name] = {}
        
        # Loop through each discipline of the run
        for ind_discip, list_discip in enumerate(discips):
            
            # Create a name for the discipline based on the index of the data
            discip_name = f"Discipline_{ind_discip + 1}"
            
            # Initialize an empty dictionary for the discipline
            space_rem[run_name][discip_name] = {}
            
            # Loop through each value in the list of times
            for time in list_of_times:
                
                # Assign time to a key for the dictionary
                space_rem[run_name][discip_name][time] = set()
            
            # Loop through each data point in the list
            for ind_data, dic_data in enumerate(list_discip):
                
                # Add size of the numpy array to the proper iteration set
                space_rem[run_name][discip_name][dic_data['iter']].add\
                    (len(dic_data['space_remaining']))
            
            # Loop back through the list of times
            for ind_time, time in enumerate(list_of_times):
                
                # Check if set is empty
                if not space_rem[run_name][discip_name][time]:
                    
                    # Add minimum time from one earlier time
                    space_rem[run_name][discip_name][time].add(min(space_rem\
                        [run_name][discip_name][list_of_times[ind_time-1]]))
    
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
            for time, sr_set in sr_dic.items():
                
                # Add midpoint of the space remaining to the proper summation
                average_rem[discip_name][time] += (min(sr_set) + max(sr_set))/2
        
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
def plot_disciplines_separately(aggregate_data):
    for discipline, time_data in aggregate_data.items():
        plt.figure(figsize=(10, 6))
        test_cases = set()
        for time_percentage, data_points in time_data.items():
            for test_case_name, _ in data_points:
                test_cases.add(test_case_name)
        
        for test_case_name in sorted(test_cases):
            time_percentages = sorted(time_data.keys())
            percentages = [np.mean([percentage_space_remaining for tc_name, percentage_space_remaining in time_data[time_percentage] if tc_name == test_case_name]) for time_percentage in time_percentages]
            plt.plot(time_percentages, percentages, label=test_case_name)
        
        plt.title(f'Average Percentage of Space Remaining vs. Percentage of Time Spent for {discipline}')
        plt.xlabel('Percentage of Time Spent (%)')
        plt.ylabel('Average Percentage of Space Remaining (%)')
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
DATA COLLECTION
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

# Read in the data from Test Case 4
os.chdir('./Test Case 4/Space_Remaining')
with open('load_data.py') as file:
    exec(file.read())

# Change back to the original directory
os.chdir(original_dir)


"""
DATA ORGANIZATION
"""
# Identify the test cases whose data will be assessed
test_case_names = ['Test_Case_1', 'Test_Case_2', 'Test_Case_3', 'Test_Case_4']

# Loop through each test case / name
for test_case_name in test_case_names:
    
    # Retrieve variable whose name matches the string
    test_case = globals()[test_case_name]
    
    # Determine all of the times when data was recorded
    set_of_times = createTimeData(test_case)
    
    # Determine space remaining at each one of those times for each test run
    space_rem = fillSpaceRemaining(test_case, set_of_times)
    
    # Determine average space remaining at each time over all of the runs
    average_rem = findAverages(space_rem)
    
    # Convert averages into percentages
    percent_rem = findPercentages(average_rem)
    
        
        
    
    
            
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # # Create pass / fail booleans for test case!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    # # [What is this function doing?]
    # processed_data = process_test_case(test_case, test_case_name)
    
    # # 
    # for discipline, data in processed_data.items():
    #     if discipline not in all_discipline_data:
    #         all_discipline_data[discipline] = {}
    #     for time_percentage, percentages in data.items():
    #         if time_percentage not in all_discipline_data[discipline]:
    #             all_discipline_data[discipline][time_percentage] = []
    #         all_discipline_data[discipline][time_percentage].extend(percentages)

#plot_disciplines_separately(all_discipline_data)


