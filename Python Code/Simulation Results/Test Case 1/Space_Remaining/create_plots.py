# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 14:06:34 2024

@author: joeyvan
"""

import numpy as np
import matplotlib.pyplot as plt


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



def aggregate_and_average(disciplines_data):
    aggregated_data = {}
    for discipline, data_points in disciplines_data.items():
        if discipline not in aggregated_data:
            aggregated_data[discipline] = {}
        for iter_num, space_remaining in data_points:
            if iter_num not in aggregated_data[discipline]:
                aggregated_data[discipline][iter_num] = []
            aggregated_data[discipline][iter_num].append(space_remaining)
    
    # Calculate average
    average_data = {discipline: [] for discipline in aggregated_data}
    for discipline, iter_data in aggregated_data.items():
        for iter_num, values in iter_data.items():
            average_percentage = np.mean(values)  # Assuming values are percentages
            average_data[discipline].append((iter_num, average_percentage))
    
    # Sort by iteration number
    for discipline in average_data:
        average_data[discipline] = sorted(average_data[discipline], key=lambda x: x[0])
    
    return average_data


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
        plt.legend()
        plt.grid(True)
        plt.show()





with open('load_data.py') as file:
    exec(file.read())





test_case_names = ['Test_Case_1']
all_discipline_data = {}

for test_case_name in test_case_names:
    test_case = globals()[test_case_name]  # Retrieve the test case variable
    processed_data = process_test_case(test_case, test_case_name)
    for discipline, data in processed_data.items():
        if discipline not in all_discipline_data:
            all_discipline_data[discipline] = {}
        for time_percentage, percentages in data.items():
            if time_percentage not in all_discipline_data[discipline]:
                all_discipline_data[discipline][time_percentage] = []
            all_discipline_data[discipline][time_percentage].extend(percentages)

plot_disciplines_separately(all_discipline_data)


