"""
SUMMARY:


CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import numpy as np
import GPy
from sklearn.preprocessing import StandardScaler
from merge_constraints import trainData


"""
SECONDARY FUNCTION
"""
def organizeData(Discips):
    
    # Initialize empty lists for x and y training data
    x_train = [None for _ in Discips]
    y_train = [None for _ in Discips]
    
    # Initialize an empty list for tracking training data array sizes
    array_size = [None for _ in Discips]
    
    # Initalize empty list for design variables
    x_vars = []
    
    # Loop through each discipline
    for i, discip in enumerate(Discips):
        
        # Combine tested input data from remaining and eliminated arrays
        x_train[i], y_train[i] = trainData(discip)
        
        # Determine the discipline's amount of training points
        array_size[i] = x_train[i].shape[0]
        
        # Loop through each design variable of the discipline
        for symbol in discip['ins']:
            
            # Check if variable is not already in the design variable list
            if symbol not in x_vars:
                
                # Append the variable to the design variable list
                x_vars.append(symbol)
                
    # Initialize x and y training data arrays with Nan
    x_full = np.full((sum(array_size), len(x_vars)), np.nan)
    y_full = np.full(sum(array_size), np.nan)
    
    # Initialize a row starting count at 0
    start_row = 0
                
    # Loop through each discipline's x and y training data
    for i, (xt, yt) in enumerate(zip(x_train, y_train)):
        
        # Determine indices of discipline's design variables in full list
        indices_x = [x_vars.index(var) for var in Discips[i]['ins']]
        
        # Replace Nan values in large training arrays with training data
        x_full[start_row:start_row + array_size[i], indices_x] = xt
        y_full[start_row:start_row + array_size[i]] = yt
        
        # Increase the row counter
        start_row += array_size[i]
    
    # Return combined matrices of training data
    return x_full, y_full


def testData(discip):
    
    
    return


"""
MAIN FUNCTION
"""
def connectPerceptions(Discips):
    
    # Isolate each discipline's training data with Nan where necessary
    x_train, y_train = organizeData(Discips)
    
    # Standardize the training data
    scaler_x = StandardScaler()
    x_train_scaled = scaler_x.fit_transform(x_train)
    scaler_y = StandardScaler()
    y_train_scaled = scaler_y.fit_transform(y_train)
    
    # Define an RBF kernel
    kernel = GPy.kern.RBF(input_dim=x_train_scaled.shape[1], ARD=True)
    
    # Create and optimize the GP model
    model = GPy.models.GPRegression(x_train_scaled, y_train_scaled, kernel)
    model.optimize()
    
    # Initialize lists for each discipline's array of pass-fail predictions
    pf_fragility = [None for _ in Discips]
    pf_std_fragility = [None for _ in Discips]
    
    # Loop through each discipline
    for discip in Discips:
        
        
    
    # Isolate each disciplines testing data with Nan where necessary
    
    
    # Standardize the testing data
    
    # Use the model to make predictions
    
    # Convert variances into standard deviations
    
    # Unstandardize the predictions
    
    # Normalize the predictions and adjust the standard deviations accordingly
    
    # Break the predictions up into a list of 1D numpy arrays for predictions and standard deviations
    
    # Return the pass-fail predictions and standard deviations
    return pf_fragility, pf_std_fragility