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
    for i, test_case in enumerate(sorted(data.keys(), 
                                         key=lambda x: int(x.split('_')[-1]))):
        
        # Assign data points
        data_points = data[test_case]
        
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
    colors = ['firebrick', 'darkorange', 'darkgreen', 'darkturquoise', 
              'blueviolet']
    # line_styles = ['-', '--', ':', '-.', 'None', 'None']
    line_styles = ['--', ':']
    # markers = ['', '', '', '', '*', '+']
    markers = ['o', 'd', '*', 'X', 'P']
    # data_groups = ['Total Space', 'Feasible Space', 'Feasible-to-Remaining']
    data_groups = ['Feasible', 'Feasible-to-Remaining']
    custom_names = ["No fragility (TC1)", "Initial PFM (TC2)", 
                    "Initial EFM (TC3)", "Extended PFM (TC4)",
                    "Extended EFM (TC5)"]
    
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
        # color_idx = 0
        # color_idx = plotData(all_test_cases_data, 'All', line_styles[0], 
        #                       colors, 0, markers)
        
        # Plot data for feasible-to-remaining space
        color_idx = 0
        color_idx = plotData(feas2_test_cases_data, 'Feas2', line_styles[0], 
                              colors, 0, markers)
        
        # Plot data for feasible space remaining
        color_idx = 0
        color_idx = plotData(feas1_test_cases_data, 'Feas1', line_styles[1], 
                              colors, 0, markers)
        
        # Plot legend
        plt.legend(handles=color_handles+line_style_handles, loc='upper left',
                   fontsize=12)
        
        # Set x- and y-axis labels
        plt.xlabel('Elapsed Project Time (%)', fontsize=14)
        plt.ylabel('Design Space Size (%)', fontsize=14)
        
        # Set x- and y-axis limits
        plt.xlim([0, 100])
        plt.ylim([0, 60])
        
        # Increase font size of the tick labels
        plt.tick_params(axis='both', which='major', labelsize=12)
        
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
    custom_names = ["No fragility (TC1)", "Initial PFM (TC2)", 
                    "Initial EFM (TC3)", "Extended PFM (TC4)", 
                    "Extended EFM (TC5)"] 
    
    # Loop through each discipline's data
    for discipline, all_test_cases_data in discipline_data.items():
    
        # Initialize figure
        plt.figure(figsize=(10, 3))
        
        # Initiatlize color index
        color_idx = 0
        
        # Loop through each test case's data
        for j, test_case in enumerate(sorted(all_test_cases_data.keys(), 
            key=lambda x: int(x.split('_')[-1]))):
            
            # Label data points
            data_points = all_test_cases_data[test_case]
            
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
        plt.ylim([0, 0.8])
        
        # Increase font size of the tick labels
        plt.tick_params(axis='both', which='major', labelsize=12)
        
        # Plot gridlines
        plt.grid(True)
        
        # Adjust layout to fit all elements within the figure
        plt.tight_layout()
        
        # Show graph
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
with open('allext_disciplines.pkl', 'rb') as f:
    allext_disciplines_data = pickle.load(f)
with open('feas1ext_disciplines.pkl', 'rb') as f:
    feas1ext_disciplines_data = pickle.load(f)
with open('feas2ext_disciplines.pkl', 'rb') as f:
    feas2ext_disciplines_data = pickle.load(f)
with open('diversityext_disciplines.pkl', 'rb') as f:
    diversityext_data = pickle.load(f)
# with open('Test_Case_1.pkl', 'rb') as f:
#     Test_Case_1 = pickle.load(f)
# with open('Discips.pkl', 'rb') as f:
#     Discips = pickle.load(f)

# Add extension data to total space remaining and diversity data
for discip_key, discip_dict in all_disciplines_data.items():
    for test_key, test_dict in allext_disciplines_data[discip_key].items():
        discip_dict[test_key] = test_dict
        feas1_disciplines_data[discip_key][test_key] = \
            feas1ext_disciplines_data[discip_key][test_key]
        feas2_disciplines_data[discip_key][test_key] = \
            feas2ext_disciplines_data[discip_key][test_key]
        diversity_data[discip_key][test_key] = \
            diversityext_data[discip_key][test_key]

# Create line plots for Disciplines 1, 2, and 3
plotDisciplines(all_disciplines_data, feas1_disciplines_data,
                feas2_disciplines_data)

# Create diversity plots for each discipline
plotDiversity(diversity_data, 'Discrepancy', '-', 
              ['firebrick', 'darkorange', 'darkgreen', 'darkturquoise', 
               'blueviolet'],
              marker = ['o', 'd', '*', 'X', 'P'])

