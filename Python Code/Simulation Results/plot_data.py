# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 14:00:45 2024

@author: joeyvan
"""

"""
LIBRARIES
"""
import pickle
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde




"""
PLOTS
"""
# I WANT TEST CASES IN LEGEND BY COLOR...AND THEN I'LL EXPLAIN IN CAPTION SOLID VS DASHED VS STARRED LINES FOR SPACE REMAINING, FEASIBLE, INFEASIBLE
def plot_disciplines(all_disciplines_data, feas_disciplines_data):
    for discipline, all_test_cases_data in all_disciplines_data.items():
        plt.figure(figsize=(10, 6))  # Create a new figure for each discipline
        feas_test_cases_data = feas_disciplines_data.get(discipline, {})
        
        # Plot for all_disciplines_data
        for test_case, data_points in all_test_cases_data.items():
            sorted_data_points = sorted(data_points.items(), key=lambda x: x[0])
            max_iteration = max(sorted_data_points, key=lambda x: x[0])[0]
            x_values = [iteration / max_iteration * 100 for iteration, _ in sorted_data_points]
            y_values = [value for _, value in sorted_data_points]
            plt.plot(x_values, y_values, label=f'{test_case} (All)', linestyle='-')
        
        # Plot for feas_disciplines_data
        for test_case, data_points in feas_test_cases_data.items():
            sorted_data_points = sorted(data_points.items(), key=lambda x: x[0])
            max_iteration = max(sorted_data_points, key=lambda x: x[0])[0]
            x_values = [iteration / max_iteration * 100 for iteration, _ in sorted_data_points]
            y_values = [value for _, value in sorted_data_points]
            plt.plot(x_values, y_values, label=f'{test_case} (Feas)', linestyle='--')
        
        plt.title(f'{discipline} - Percentage of Space Remaining Over Time')
        plt.xlabel('Percentage of Time Spent (%)')
        plt.ylabel('Percentage of Space Remaining (%)')
        plt.xlim([0, 100])
        plt.ylim([0, 100])
        plt.legend()
        plt.grid(True)
        plt.show()


def plot_3d_heatmap_for_discipline(test_case_data, discipline_index):
    """
    Plots a 3D heatmap for the specified discipline across all runs at the 1000th iteration.

    :param test_case_data: The dictionary containing the test case data.
    :param discipline_index: The index of the discipline to plot (0, 1, or 2).
    """
    all_points = []

    # Extracting points from the 1000th iter of each run for the specified discipline
    for run, disciplines in test_case_data.items():
        for data_point in disciplines[discipline_index]:
            if data_point['iter'] == 1000:
                space_remaining = data_point['space_remaining']
                all_points.extend(space_remaining)

    # Converting list of points to a numpy array for processing
    all_points = np.array(all_points)

    # Calculating point densities
    kde = gaussian_kde(all_points.T)
    density = kde(all_points.T)

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Initialize an empty list for storing numpy arrays
    l = []
    
    # Surface plot
    j = np.linspace(0, 1, 4000)
    k = np.linspace(0, 1, 4000)
    j, k = np.meshgrid(j, k)
    
    if discipline_index == 0:
        l.append(0.8*j**2 + 2*k**2 - 0.0)
        l.append(0.8*j**2 + 2*k**2 - 0.4)
        l.append(0.8*j**2 + 2*k**2 - 1.2)
        l.append(0.8*j**2 + 2*k**2 - 1.6)
    elif discipline_index == 1:
        l.append((12.5*j**3-6.25*j**2+0.5)/1.25)
        l.append((12.5*j**3-6.25*j**2+0.7)/1.25)
        l.append(-k**3+np.sqrt(0.2))
        l.append(-k**3+np.sqrt(0.5))
    else:
        l.append((2*j+0.2*np.sin(25*k)-0.0)**5)
        l.append((2*j+0.2*np.sin(25*k)-0.5)**5)
        l.append((np.cos(3*j)+0.8)**3)
        l.append((np.cos(3*j)+1.6)**3)
    
    # Replace out-of-bounds z_values with np.nan
    l = [np.where((z >= 0) & (z <= 1), z, np.nan) for z in l]
    
    # Initialize colors for plots
    colors = ['teal', 'teal', 'magenta', 'magenta']
    
    # Plot every surface
    for m in range(0, len(l)):
        if discipline_index < 2:
            ax.plot_surface(j, k, l[m], color=colors[m], alpha=0.1, rstride=100, cstride=100)
        else:
            ax.plot_surface(l[m], j, k, color=colors[m], alpha=0.1, rstride=100, cstride=100)
    
    # Scatter plot with density as color
    scatter = ax.scatter(all_points[:, 0], all_points[:, 1], all_points[:, 2], c=density, cmap='inferno')

    # Adding color bar to indicate density
    plt.colorbar(scatter, ax=ax, label='Density')

    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')
    plt.title(f'3D Heat Map for Discipline {discipline_index + 1}')
    plt.show()





"""
SCRIPT
"""
# Upload saved data
# with open('all_disciplines.pkl', 'rb') as f:
#     all_disciplines_data = pickle.load(f)
# with open('feas1_disciplines.pkl', 'rb') as f:
#     feas1_disciplines_data = pickle.load(f)
# with open('feas2_disciplines.pkl', 'rb') as f:
#     feas2_disciplines_data = pickle.load(f)
with open('Test_Case_3.pkl', 'rb') as f:
    Test_Case_3 = pickle.load(f)

# Create Heat Map Plot of Test Case 3
plot_3d_heatmap_for_discipline(Test_Case_3, 0)  # For the first discipline
plot_3d_heatmap_for_discipline(Test_Case_3, 1)  # For the second discipline
plot_3d_heatmap_for_discipline(Test_Case_3, 2)  # For the third discipline


# Create line plots for Disciplines 1, 2, and 3






# Plot the results
#plot_disciplines(all_disciplines_data, feas1_disciplines_data)