"""
SUMMARY:
Create scatter plots of each test case's gradient factor findings across all of
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
    
    # Identify the test cases whose data will be assessed
    test_case_names = ['Gradient_Factor_4', 'Gradient_Factor_5']
    custom_names = ["Extended PFM (TC4)", "Extended EFM (TC5)"]

    # Colors for each test case
    colors = ['darkturquoise', 'blueviolet']
        
    # Initialize figure
    plt.figure(figsize=(10, 6))
    
    # Initialize empty lists for data
    x_values = [None for _ in test_case_names]
    y_values = [None for _ in test_case_names]

    # Loop through each test case
    for idx, (test_case_name, custom_name) in enumerate(zip(test_case_names, 
                                                            custom_names)):
        
        # Retrieve the actual test case data from globals
        test_case = globals()[test_case_name]
        
        # Create arrays to store data
        x_values[idx] = np.empty(0)
        y_values[idx] = np.empty(0)
        
        # Loop through each run
        for run in test_case.keys():
            
            # Loop through each instance data was collected
            for index, instance in enumerate(test_case[run]):
                
                # Extract necessary data
                x_values[idx] = np.append(x_values[idx], instance['iter']/400*100)
                y_values[idx] = np.append(y_values[idx], instance['gradient_factor'])
                
    # Plot the data
    plt.scatter(x_values[0], y_values[0], color=colors[0], marker='x', label=custom_names[0], s=80)
    plt.scatter(x_values[1], y_values[1], color=colors[1], marker='o', facecolors='none', edgecolors=colors[1], label=custom_names[1], s=80)
    
    # Configure plot
    plt.xlabel('Elapsed Project Time (%)', fontsize=14)
    plt.ylabel('Gradient Factor', fontsize=14)
    plt.xlim([0, 100])
    plt.ylim([0, 3])
    plt.tick_params(axis='both', which='major', labelsize=12)
    plt.grid(True)
    plt.legend(loc='upper left', fontsize=12)
    plt.tight_layout()
    plt.show()
