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
def plotData(data, label_prefix, linestyle, colors, color_idx, marker):
    """
    Description
    -----------
    Plots data points for each test case within a given dataset.
    
    Parameters
    ----------
    data : Dictionary
        Each key is a test case identifier, and each value is another
        dictionary mapping iteration numbers to data points
    label_prefix : String
        A prefix for the label that will be added before each test case's
        identifier in the plot legend
    linestyle : String
        Style of line for plotting. Use 'None' for no line
    colors : List
        List of colors for plotting lines
    color_idx : Integer
        Current position in the `colors` list from which to start coloring the
        plotted lines
    marker : List
        Marker styles

    Returns
    -------
    color_idx : Integer
        Updated position in the `colors` list
    """
    
    # Loop through each test case's data
    for i, (test_case, data_points) in enumerate(data.items()):
        
        # Sort data points by its time iteration keys
        sorted_data_points = sorted(data_points.items(), key=lambda x: x[0])
        
        # Find maximum of sorted data
        max_iteration = max(sorted_data_points, key=lambda x: x[0])[0]
        
        # Gather x and y data point percentages
        x_values = [iteration / max_iteration * 100 \
                    for iteration, _ in sorted_data_points]
        y_values = [value for _, value in sorted_data_points]
        
        # Define custom linewidth for particular line styles
        if linestyle == ':':
            linewidth = 2.0
        else:
            linewidth = 1.5
        
        # Plot the data
        plt.plot(x_values, y_values, label=f'{label_prefix} {test_case}',
                 color=colors[color_idx % len(colors)], linestyle=linestyle,
                 linewidth=linewidth, marker=marker[i], markersize=12)
        
        # Increase the color index by 1
        color_idx += 1
    
    # Return the updated color index
    return color_idx


"""
FUNCTIONS
"""
def plotDisciplines(all_disciplines_data, feas1_disciplines_data, 
                    feas2_disciplines_data):
    """
    Description
    -----------
    Visualizes the progression of design spaces across different disciplines by
    plotting data for space remaining, feasible space remaining, and
    feasible-to-remaining space.

    Parameters
    ----------
    all_disciplines_data : Dictionary
        Contains total space remaining data for each discipline over elapsed
        time
    feas1_disciplines_data : Dictionary
        Contains feasible-to-remaining space data for each discipline over
        elapsed time
    feas2_disciplines_data : Dictionary
        Contains feasible space remaining data for each discipline over elapsed
        time
    """
    
    # Initialize colors, line styles, markers, and legend names
    colors = ['firebrick', 'darkorange', 'darkgreen']
    line_styles = ['-', '--', ':']
    markers = ['o', 'd', '*']
    data_groups = ['Total Space', 'Feasible', 'Feasible-to-Remaining']
    custom_names = ["No fragility (TC1)", "PFM (TC2)", "EFM (TC3)"] 
    
    
    # Loop through each discipline's data
    for discipline, all_test_cases_data in all_disciplines_data.items():
        
        # Initialize figure
        plt.figure(figsize=(10, 4))
        
        # Create custom legend labels
        color_handles = [Line2D([0], [0], color=color, linewidth=0, 
                                marker=markers[i], markersize=12, 
                                label=custom_names[i]) \
                         for i, color in enumerate(colors)]
        line_style_handles = [Line2D([0], [0], color='black', linewidth=2,
                              linestyle=ls, label=data_groups[i]) \
                              for i, ls in enumerate(line_styles)]
        
        # Retrieve disciplines' feasible space data
        feas1_test_cases_data = feas1_disciplines_data.get(discipline, {})
        feas2_test_cases_data = feas2_disciplines_data.get(discipline, {})
        
        # Plot data for space remaining
        color_idx = 0
        color_idx = plotData(all_test_cases_data, 'All', line_styles[0], 
                             colors, 0, markers)
        
        # Plot data for feasible-to-remaining space
        color_idx = 0
        color_idx = plotData(feas2_test_cases_data, 'Feas2', line_styles[1], 
                              colors, 0, markers)
        
        # Plot data for feasible space remaining
        color_idx = 0
        color_idx = plotData(feas1_test_cases_data, 'Feas1', line_styles[2], 
                             colors, 0, markers)
        
        # Plot legend
        plt.legend(handles=color_handles+line_style_handles, loc='upper left',
                   fontsize=12)
        
        # Set x- and y-axis labels
        plt.xlabel('Elapsed Project Time (%)', fontsize=14)
        plt.ylabel('Design Space Size (%)', fontsize=14)
        
        # Set x- and y-axis limits
        plt.xlim([0, 100])
        plt.ylim([0, 100])
        
        # Increase font size of the tick labels
        plt.tick_params(axis='both', which='major', labelsize=14)
        
        # Plot gridlines
        plt.grid(True)
        
        # Adjust layout to fit all elements within the figure
        plt.tight_layout()
        
        # Show graph
        plt.show()


def plotDiversity(discipline_data, data_type, linestyle, colors, marker):
    """
    Description
    -----------
    Plots data points for a single dataset within a given discipline.
    
    Parameters
    ----------
    discipline_data : Dictionary
        Contains data for a single discipline over elapsed time
    data_type : String
        Type of data being plotted (e.g., 'Diversity')
    linestyle : String
        Style of line for plotting. Use 'None' for no line
    colors : List
        List of colors for plotting lines
    marker : List
        List of marker styles for plotting lines
    """
    
    # Initialize custom legend names
    custom_names = ["No fragility (TC1)", "PFM (TC2)", "EFM (TC3)"] 
    
    # Loop through each discipline's data
    for discipline, all_test_cases_data in discipline_data.items():
    
        # Initialize figure
        plt.figure(figsize=(10, 3))
        
        # Initiatlize color index
        color_idx = 0
        
        # Loop through each test case's data
        for j,(test_case,data_points) in enumerate(all_test_cases_data.items()):
            
            # Sort data points by its time iteration keys
            sorted_data_points = sorted(data_points.items(), key=lambda x: x[0])
            
            # Find maximum of sorted data
            max_iteration = max(sorted_data_points, key=lambda x: x[0])[0]
            
            # Gather x and y data point percentages
            x_values = [iteration / max_iteration * 100 \
                        for iteration, _ in sorted_data_points]
            y_values = [value for _, value in sorted_data_points]
            
            # Define custom linewidth for particular line styles
            if linestyle == ':':
                linewidth = 2.0
            else:
                linewidth = 1.5
            
            # Plot the data
            plt.plot(x_values, y_values, label=f'{data_type} {test_case}',
                     color=colors[color_idx % len(colors)], 
                     linestyle=linestyle, linewidth=linewidth, 
                     marker=marker[j], markersize=12)
            
            # Increase the color index by 1
            color_idx += 1
        
        # Create custom legend labels
        custom_legend = [Line2D([0], [0], color=colors[i % len(colors)], 
                                linestyle=linestyle, linewidth=0, 
                                marker=marker[i], markersize=12, 
                                label=custom_names[i]) \
                         for i in range(len(all_test_cases_data))]
        
        # Plot legend
        plt.legend(handles=custom_legend, loc='upper left', fontsize=12)
        
        # Set x- and y-axis labels with increased font size
        plt.xlabel('Elapsed Project Time (%)', fontsize=14)
        plt.ylabel('Design Space Discrepancy', fontsize=14)
        
        # Set x- and y-axis limits
        plt.xlim([0, 100])
        plt.ylim([0, 0.35])
        
        # Increase font size of the tick labels
        plt.tick_params(axis='both', which='major', labelsize=14)
        
        # Plot gridlines
        plt.grid(True)
        
        # Adjust layout to fit all elements within the figure
        plt.tight_layout()
        
        # Additional adjustment for less tight layout
        plt.subplots_adjust(left=0.08, right=0.97, top=0.9, bottom=0.2)
        
        # Show graph
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
with open('diversity_disciplines.pkl', 'rb') as f:
    diversity_data = pickle.load(f)
# with open('Test_Case_3.pkl', 'rb') as f:
#     Test_Case_3 = pickle.load(f)
# with open('Discips.pkl', 'rb') as f:
#     Discips = pickle.load(f)

# Create line plots for Disciplines 1, 2, and 3
plotDisciplines(all_disciplines_data, feas1_disciplines_data,
                feas2_disciplines_data)

# Create diversity plots for each discipline
plotDiversity(diversity_data, 'Discrepancy', '-', 
              ['firebrick', 'darkorange', 'darkgreen'],
              marker = ['o', 'd', '*'])

# Create Heat Map Plot of Test Case 3 for each discipline
# plotHeatmaps(Test_Case_3, 0, Discips[0]['ins'])
# plotHeatmaps(Test_Case_3, 1, Discips[1]['ins'])
# plotHeatmaps(Test_Case_3, 2, Discips[2]['ins'])
