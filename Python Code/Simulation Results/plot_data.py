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
from matplotlib.lines import Line2D
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize


"""
PLOTS
"""
def plot_disciplines(all_disciplines_data, feas1_disciplines_data, feas2_disciplines_data):
    colors = ['darkorange', 'firebrick', 'violet', 'forestgreen']  # Define four colors for test cases
    line_styles = ['-', '--', ':']  # Define three line styles for data groups
    data_groups = ['Total Space', 'Feasible Space', 'Feasible-to-Remaining']  # Define data group names
    
    for discipline, all_test_cases_data in all_disciplines_data.items():
        plt.figure(figsize=(10, 5))  # Create a new figure for each discipline
        
        # Define custom legend handles for the colors (test cases)
        color_handles = [Line2D([0], [0], marker='o', color='w', label=f'Test Case {i+1}',
                                markerfacecolor=color, markersize=10) for i, color in enumerate(colors)]
        # Define custom legend handles for the line styles (data groups)
        line_style_handles = [Line2D([0], [0], color='black', linewidth=2, linestyle=ls, label=data_groups[i])
                              for i, ls in enumerate(line_styles)]
        
        feas1_test_cases_data = feas1_disciplines_data.get(discipline, {})
        feas2_test_cases_data = feas2_disciplines_data.get(discipline, {})
        color_idx = 0  # Initialize color index
        
        # Helper function to plot data
        def plot_data(data, label_prefix, linestyle):
            nonlocal color_idx  # Use the outer color_idx variable
            for test_case, data_points in data.items():
                sorted_data_points = sorted(data_points.items(), key=lambda x: x[0])
                max_iteration = max(sorted_data_points, key=lambda x: x[0])[0]
                x_values = [iteration / max_iteration * 100 for iteration, _ in sorted_data_points]
                y_values = [value for _, value in sorted_data_points]
                
                # Check if the current linestyle is the dotted one and increase linewidth if it is
                if linestyle == ':':
                    linewidth = 2.0  # Specify the larger size for the dotted line here
                else:
                    linewidth = 1.5  # Default linewidth for other linestyles
                
                plt.plot(x_values, y_values, label=f'{test_case} ({label_prefix})', color=colors[color_idx % len(colors)], linestyle=linestyle, linewidth=linewidth)
                color_idx += 1  # Move to the next color for the next test case

        
        # Plot for all disciplines data with the first line style
        plot_data(all_test_cases_data, 'All', line_styles[0])
        color_idx = 0  # Reset color index for consistency across groups
        # Plot for feas1 disciplines data with the second line style
        plot_data(feas2_test_cases_data, 'Feas2', line_styles[1])
        color_idx = 0  # Reset color index for consistency across groups
        # Plot for feas2 disciplines data with the third line style
        plot_data(feas1_test_cases_data, 'Feas1', line_styles[2])
        
        # Adjust legend to include both custom color and linestyle handles
        plt.legend(handles=color_handles + line_style_handles, loc='upper left')
        
        plt.xlabel('Elapsed Project Time (%)')
        plt.ylabel('Size of Design Space (%)')
        plt.xlim([0, 100])
        plt.ylim([0, 100])
        plt.grid(True)
        plt.show()



def plot_3d_heatmap_for_discipline(test_case_data, discipline_index, ins):
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
    
    # Normalize density for alpha mapping (transparency)
    density_normalized = (density - density.min()) / (density.max() - density.min())
    alphas = 0.005 + 0.045 * density_normalized
    
    # Create figure
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Scatter plot with variable transparency, using a fixed color for simplicity
    colors = np.full(all_points.shape[0], 'tan')  # Use a single color for all points
    scatter = ax.scatter(all_points[:, 0], all_points[:, 1], all_points[:, 2], c=colors, alpha=alphas)
    
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
            ax.plot_surface(j, k, l[m], color=colors[m], alpha=0.8, rstride=100, cstride=100)
        else:
            ax.plot_surface(l[m], j, k, color=colors[m], alpha=0.8, rstride=100, cstride=100)

    # Set axis limits
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.set_zlim([0, 1])
    
    # Set labels and title
    ax.set_xlabel(ins[0])
    ax.set_ylabel(ins[1])
    ax.set_zlabel(ins[2])
    ax.set_title(f"Discipline {discipline_index+1} Design Space")
    
    # Create the graph
    plt.show()





"""
SCRIPT
"""
# Upload saved data
with open('all_disciplines.pkl', 'rb') as f:
    all_disciplines_data = pickle.load(f)
with open('feas1_disciplines.pkl', 'rb') as f:
    feas1_disciplines_data = pickle.load(f)
with open('feas2_disciplines.pkl', 'rb') as f:
    feas2_disciplines_data = pickle.load(f)
with open('Test_Case_3.pkl', 'rb') as f:
    Test_Case_3 = pickle.load(f)
with open('Discips.pkl', 'rb') as f:
    Discips = pickle.load(f)

# Create Heat Map Plot of Test Case 3
# plot_3d_heatmap_for_discipline(Test_Case_3, 0, Discips[0]['ins'])  # For the first discipline
# plot_3d_heatmap_for_discipline(Test_Case_3, 1, Discips[1]['ins'])  # For the second discipline
# plot_3d_heatmap_for_discipline(Test_Case_3, 2, Discips[2]['ins'])  # For the third discipline


# Create line plots for Disciplines 1, 2, and 3
plot_disciplines(all_disciplines_data, feas1_disciplines_data, feas2_disciplines_data)