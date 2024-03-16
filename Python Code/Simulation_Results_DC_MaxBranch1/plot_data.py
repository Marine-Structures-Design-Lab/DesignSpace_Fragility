"""
SUMMARY:
Create various plots for visualizing the acquired data.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import pickle
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
from matplotlib.lines import Line2D


"""
SECONDARY FUNCTION
"""
def plotData(data, label_prefix, linestyle, colors, color_idx, max_iteration):
    """
    Plots data points for each test case within a given dataset, considering
    different maximum iterations for "BC" and "AC" categories.

    Parameters
    ----------
    data : Dictionary
        Each key is an iteration number (as a string or integer) and each value is another dictionary
        mapping iteration numbers to data points.
    label_prefix : String
        A prefix for the label that will be added before each test case's
        identifier in the plot legend.
    linestyle : String
        Style of line for plotting.
    colors : List
        Color of line for plotting.
    color_idx : Integer
        Current position in the `colors` list from which to start coloring the
        plotted lines.
    max_iteration : Integer
        The maximum iteration number for the dataset, used to scale the x-axis.

    Returns
    -------
    color_idx : Integer
        Updated position in the `colors` list.
    """
    
    # Ensure iteration keys are sorted numerically
    sorted_data = sorted(data.items(), key=lambda x: int(x[0]))
    
    # Generate x and y values
    x_values = [int(iteration) / max_iteration * 100 for iteration, _ in sorted_data]
    y_values = [value for _, value in sorted_data]
    
    # Plotting logic
    plt.plot(x_values, y_values, label=f'{label_prefix}',
             color=colors[color_idx % len(colors)], linestyle=linestyle, linewidth=2)
    
    # Increment color index for next call
    color_idx += 1
    
    return color_idx


def find_max_iteration(phase_data):
    max_iter = 0
    for test_case, phases in phase_data.items():
        for phase in ['BC', 'AC']:
            if phase in phases:
                iterations = list(map(int, phases[phase].keys()))
                if iterations:
                    max_iter = max(max_iter, max(iterations))
    return max_iter





"""
FUNCTIONS
"""
def plotDisciplines(all_disciplines_data, feas1_disciplines_data):
    colors = ['darkorange', 'firebrick', 'violet']
    line_styles = ['-', ':']
    data_groups = ['Total Space', 'Feasible-to-Remaining Space']

    for discipline in all_disciplines_data:
        plt.figure(figsize=(10, 5))
        max_iteration_bc = find_max_iteration(all_disciplines_data[discipline])
        max_iteration_ac = find_max_iteration(all_disciplines_data[discipline])
        
        for category, phase_data in [("BC", max_iteration_bc), ("AC", max_iteration_ac)]:
            color_idx = 0
            for test_case in all_disciplines_data[discipline]:
                if category in all_disciplines_data[discipline][test_case]:
                    # Example call to a modified plotData function, pass phase-specific max_iteration
                    color_idx = plotData(all_disciplines_data[discipline][test_case][category], 
                                         f'{test_case} ({category})', line_styles[0], colors, color_idx, phase_data)
            for test_case in feas1_disciplines_data[discipline]:
                if category in feas1_disciplines_data[discipline][test_case]:
                    # Example call to a modified plotData function, pass phase-specific max_iteration
                    color_idx = plotData(feas1_disciplines_data[discipline][test_case][category], 
                                         f'{test_case} ({category})', line_styles[1], colors, color_idx, phase_data)
        
        plt.legend(handles=[Line2D([0], [0], color=colors[i], lw=2, label=f'Test Case {i+1}') for i in range(len(colors))] +
                   [Line2D([0], [0], color='black', lw=2, linestyle=ls, label=dg) for ls, dg in zip(line_styles, data_groups)])
        plt.xlabel('Elapsed Project Time (%)')
        plt.ylabel('Size of Design Space (%)')
        plt.xlim([0, 100])
        plt.ylim([0, 100])
        plt.grid(True)
        plt.show()



def plotHeatmaps(test_case_data, discipline_index, ins):
    """
    Description
    -----------
    Plots a heat map of the last iteration of space remaining data in each
    discipline's input space for all of the simulations of Test Case 3.

    Parameters
    ----------
    test_case_data : Dictionary
        Contains all of the space remaining data with 1000th iteration of Test
        Case 3
    discipline_index : Integer
        Index of discipline from which data is being extracted
    ins : Sympy symbols
        Input variables for which the discipline can manipulate variables
    """
    
    # Initialize an empty list for all of the points
    all_points = []

    # Extracting points from the 1000th iter of each run
    for run, disciplines in test_case_data.items():
        for data_point in disciplines[discipline_index]:
            if data_point['iter'] == 1000:
                space_remaining = data_point['space_remaining']
                all_points.extend(space_remaining)

    # Convert list of points to a numpy array
    all_points = np.array(all_points)

    # Calculate point densities
    kde = gaussian_kde(all_points.T)
    density = kde(all_points.T)
    
    # Normalize density for transparency mapping
    density_normalized = (density-density.min())/(density.max()-density.min())
    alphas = 0.005 + 0.045 * density_normalized
    
    # Create figure
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Scatter plot with variable transparency
    colors = np.full(all_points.shape[0], 'tan')
    scatter = ax.scatter(all_points[:, 0], all_points[:, 1], all_points[:, 2],
                         c=colors, alpha=alphas)
    
    # Initialize an empty list for storing numpy arrays
    l = []
    
    # Create surface plots
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
            ax.plot_surface(j, k, l[m], color=colors[m], alpha=0.8,
                            rstride=100, cstride=100)
        else:
            ax.plot_surface(l[m], j, k, color=colors[m], alpha=0.8,
                            rstride=100, cstride=100)

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
# with open('Test_Case_3.pkl', 'rb') as f:
#     Test_Case_3 = pickle.load(f)
with open('Discips.pkl', 'rb') as f:
    Discips = pickle.load(f)
with open('Discips2.pkl', 'rb') as f:
    Discips2 = pickle.load(f)

# Create line plots for Disciplines 1, 2, and 3
plotDisciplines(all_disciplines_data, feas1_disciplines_data)

# Create Heat Map Plot of Test Case 3 for each discipline
# plotHeatmaps(Test_Case_3, 0, Discips[0]['ins'])
# plotHeatmaps(Test_Case_3, 1, Discips[1]['ins'])
# plotHeatmaps(Test_Case_3, 2, Discips[2]['ins'])
