# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 14:06:34 2024

@author: joeyvan
"""

import numpy as np
import matplotlib.pyplot as plt
import os





# Add list with pass and fail data to each run
# After this is added...can add most recent update to code from chatgpt
# Then can work on adding other test case data...move this function (create_plots) to Simulation_Results
# and have it pull from each folder...leave load data script in each folder though
def determine_feasibility(test_case, test_case_name):
    # MAKE A COPY OF THE FIRST ONE AND DO THE COPYING AND THE INDICES THING AGAIN SO I DON'T HAVE TO KEEP CHECKING FEASIBILITY!!!
    
    
    return













def process_test_case(test_case, test_case_name):
    discipline_results = {}
    initial_sizes = {}
    iteration_scale = 200 if test_case_name in ['Test_Case_1', 'Test_Case_2'] else 1000  # Determine scaling factor

    for run_name, disciplines in test_case.items():
        for discipline_index, discipline_data in enumerate(disciplines):
            discipline_name = f"Discipline_{discipline_index + 1}"
            if discipline_name not in discipline_results:
                discipline_results[discipline_name] = {}
            if discipline_name not in initial_sizes:
                initial_sizes[discipline_name] = None
            for data_point in discipline_data:
                iter_num = data_point['iter']
                time_percentage = (iter_num / iteration_scale) * 100  # Calculate percentage of time spent
                space_remaining = len(data_point['space_remaining'])  # Get current size
                if iter_num == 0:
                    initial_sizes[discipline_name] = space_remaining  # Set initial size
                percentage_space_remaining = (space_remaining / initial_sizes[discipline_name]) * 100
                if time_percentage not in discipline_results[discipline_name]:
                    discipline_results[discipline_name][time_percentage] = []
                discipline_results[discipline_name][time_percentage].append((test_case_name, percentage_space_remaining))
    return discipline_results



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


# Save the current directory's path
original_dir = os.getcwd()

# Read in the data from each test case
os.chdir('./Test Case 1/Space_Remaining')
with open('load_data.py') as file:
    exec(file.read())

# Change back to the original directory
os.chdir(original_dir)

os.chdir('./Test Case 2/Space_Remaining')
with open('load_data.py') as file:
    exec(file.read())

# Change back to the original directory
os.chdir(original_dir)


test_case_names = ['Test_Case_1', 'Test_Case_2']
all_discipline_data = {}

for test_case_name in test_case_names:
    test_case = globals()[test_case_name]  # Retrieve the test case variable
    # Create pass / fail booleans for test case
    processed_data = process_test_case(test_case, test_case_name)
    for discipline, data in processed_data.items():
        if discipline not in all_discipline_data:
            all_discipline_data[discipline] = {}
        for time_percentage, percentages in data.items():
            if time_percentage not in all_discipline_data[discipline]:
                all_discipline_data[discipline][time_percentage] = []
            all_discipline_data[discipline][time_percentage].extend(percentages)

plot_disciplines_separately(all_discipline_data)


