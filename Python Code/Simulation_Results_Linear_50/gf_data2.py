"""
SUMMARY:
Create box plots of each test case's gradient factor findings across all of
the runs

CREATOR:
Joseph B. Van Houten
"""

"""
LIBRARIES
"""
import pickle
import numpy as np
import matplotlib.pyplot as plt


"""
SCRIPT
"""
# Ensure this script is only run when it is being executed directly
if __name__ == "__main__":

    # Upload saved data
    with open('Gradient_Factor_4.pkl', 'rb') as f:
        Gradient_Factor_4 = pickle.load(f)
    with open('Gradient_Factor_5.pkl', 'rb') as f:
        Gradient_Factor_5 = pickle.load(f)
    
    # Identify the test cases
    test_case_names = ['Gradient_Factor_4', 'Gradient_Factor_5']
    custom_names = ["Extended PFM (TC4)", "Extended EFM (TC5)"]
    colors = ['darkturquoise', 'blueviolet']
    
    # Define bin edges for project time (0% to 100% in 10% intervals)
    bin_edges = np.linspace(0, 100, 11)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Initialize figure
    plt.figure(figsize=(10, 6))
    
    # Loop through each test case
    for idx, (test_case_name, custom_name) in enumerate(zip(test_case_names, custom_names)):
        
        # Retrieve data
        test_case = globals()[test_case_name]
        
        # Store gradient factors per bin
        binned_data = [[] for _ in range(len(bin_edges) - 1)]
        
        for run in test_case:
            for instance in test_case[run]:
                elapsed_time = instance['iter'] / 200 * 100
                gf = instance['gradient_factor']
                # Find which bin it belongs to
                bin_index = np.digitize(elapsed_time, bin_edges) - 1
                if 0 <= bin_index < len(binned_data):
                    binned_data[bin_index].append(gf)
        
        # Create box plots
        bp = plt.boxplot(
            binned_data,
            positions=bin_centers + idx * 3,  # offset for visibility
            widths=4,
            patch_artist=True,
            boxprops=dict(facecolor=colors[idx], color=colors[idx]),
            capprops=dict(color=colors[idx]),
            whiskerprops=dict(color=colors[idx]),
            flierprops=dict(marker='o', color=colors[idx], alpha=0.5),
            medianprops=dict(color='black'),
            labels=None
        )
    
    # Configure plot
    plt.xlabel('Elapsed Project Time (%)', fontsize=14)
    plt.ylabel('Gradient Factor', fontsize=14)
    plt.xlim([0, 100])
    plt.ylim([0, 3])
    plt.xticks(bin_centers, [f"{int(b)}%" for b in bin_centers], rotation=45)
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.grid(True)

    # Custom legend
    handles = [plt.Line2D([0], [0], color=colors[i], lw=4) for i in range(len(custom_names))]
    plt.legend(handles, custom_names, loc='upper left', fontsize=12)

    plt.tight_layout()
    plt.show()
