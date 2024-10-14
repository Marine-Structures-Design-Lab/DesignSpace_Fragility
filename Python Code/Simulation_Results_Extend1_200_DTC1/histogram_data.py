"""
SUMMARY:
Create histograms of each design variable's space remaining at different times
of the simulations across all of the runs

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
    with open('Test_Case_1.pkl', 'rb') as f:
        Test_Case_1 = pickle.load(f)
    with open('Test_Case_2.pkl', 'rb') as f:
        Test_Case_2 = pickle.load(f)
    with open('Test_Case_3.pkl', 'rb') as f:
        Test_Case_3 = pickle.load(f)
    with open('Test_Case_4.pkl', 'rb') as f:
        Test_Case_4 = pickle.load(f)
    with open('Test_Case_5.pkl', 'rb') as f:
        Test_Case_5 = pickle.load(f)
    
    # Identify the test cases whose data will be assessed
    test_case_names = ['Test_Case_1', 'Test_Case_2', 'Test_Case_3', 
                       'Test_Case_4', 'Test_Case_5']
    custom_names = ["No fragility (TC1)", "Initial PFM (TC2)", 
                    "Initial EFM (TC3)", "Extended PFM (TC4)",
                    "Extended EFM (TC5)"]
    
    # Create custom bin bounds
    custom_bins = np.array([-0.0625, 0.0625, 0.1875, 0.3125, 0.4375, 0.5625, 
                            0.6875, 0.8125, 0.9375, 1.0625])

    # Colors for each test case
    colors = ['firebrick', 'darkorange', 'darkgreen', 'darkturquoise', 
              'blueviolet']
    
    # Determine number of test cases
    num_cases = len(test_case_names)

    # Set custom bar width
    bar_width = (np.diff(custom_bins)[0] * 0.8) / num_cases
    
    # Calculate bin midpoints for x-ticks
    bin_midpoints = (custom_bins[:-1] + custom_bins[1:]) / 2
    adjusted_xticks = bin_midpoints + (2 * bar_width)

    # Loop through each coordinate (plot each coordinate's histogram once)
    for i in range(0, 6):
        
        # Initialize figure
        plt.figure(figsize=(7, 5))

        # Loop through each test case
        for idx, test_case_name in enumerate(test_case_names):
            
            # Retrieve the actual test case data from globals
            test_case = globals()[test_case_name]
            
            # Initialize numpy arrays for stacking
            first_array = np.empty((0, 6))
            # last_array = np.empty((0, 6))
            time_array = np.empty((0, 6))
            
            # Loop through each run
            for run in test_case.keys():
                
                # Loop through each instance data was collected
                for index, instance in enumerate(test_case[run][0]):
                    
                    # Break if the instance's iteration is greater than cut-off
                    if instance['iter'] > 107: break
                    
                    # Set new instance index
                    instance_index = index
                
                # Stack the initial space remaining arrays
                first_array = np.vstack((first_array, 
                    test_case[run][0][0]['space_remaining']))
                
                # Stack the last space remaining arrays
                # last_array = np.vstack((last_array,
                #     test_case[run][0][-1]['space_remaining']))
                
                # Stack the space remaining arrays at the cut-off
                time_array = np.vstack((time_array,
                    test_case[run][0][instance_index]['space_remaining']))
            
            # Create histograms
            first_hist, bins = np.histogram(first_array[:, i],bins=custom_bins)
            # last_hist, _ = np.histogram(last_array[:, i], bins=bins)
            time_hist, _ = np.histogram(time_array[:, i], bins=bins)
            
            # Avoid division by zero errors
            first_hist = np.where(first_hist == 0, 1, first_hist)
            
            # Calculate bin percentages relative to first bins
            # percentage_hist = (last_hist / first_hist) * 100
            percentage_hist = (time_hist / first_hist) * 100
            
            # Compute the x-offset for each test case
            offset = idx * bar_width
            
            # Adjust bin positions by adding an offset for each test case
            adjusted_bins = bins[:-1] + offset
            
            # Plot this test case's results on the current histogram
            plt.bar(adjusted_bins, percentage_hist, width=bar_width, 
                    edgecolor='black', align='edge', 
                    color=colors[idx], label=f'{custom_names[idx]}')
        
        # Configure plot
        plt.xlabel('Normalized Value', fontsize=14)
        plt.ylabel('Designs Remaining (%)', fontsize=14)
        plt.ylim(0, 100)
        plt.grid(axis='y')
        plt.xticks(adjusted_xticks, np.round(bin_midpoints, 3), fontsize=12)
        plt.yticks(fontsize=12)
        plt.legend(loc='upper left', fontsize=12)
        plt.tight_layout()
        plt.show()
