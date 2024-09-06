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
from merge_constraints import trainData, normalizePredictions


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
 
    # Return combined matrices of training data and full design variable list
    return x_full, y_full, x_vars


def prepareData(Discips, x_vars):
    
    # Initialize list for each discipline's array of testing data
    test_data = [None for _ in Discips]
    
    # Loop through each discipline
    for i, discip in enumerate(Discips):
        
        # Determine indices of discipline's design variables in full list
        indices_x = [x_vars.index(var) for var in discip['ins']]
        
        # Initialize a numpy array of nan values for testing data
        test_data[i] = np.full((discip['space_remaining'].shape[0], len(x_vars)), np.nan)
        
        # Populate the array with the discipline's remaining design space data
        test_data[i][:, indices_x] = discip['space_remaining']
    
    # Return the organized testing data
    return test_data


"""
MAIN FUNCTION
"""
def connectPerceptions(Discips):
    
    # Isolate each discipline's training data
    x_train, y_train, x_vars = organizeData(Discips)
    
    # Standardize the training data
    scaler_x = StandardScaler()
    x_train_scaled = scaler_x.fit_transform(x_train)
    scaler_y = StandardScaler()
    y_train_scaled = scaler_y.fit_transform(y_train.reshape(-1,1))
    
    # Define an RBF kernel
    kernel = GPy.kern.RBF(input_dim=x_train_scaled.shape[1], ARD=True)
    
    # Create the GP model
    model = GPy.models.GPRegression(x_train_scaled, y_train_scaled, kernel)
    
    # Optimize the model
    model.optimize()
    
    # Initialize lists for each discipline's array of pass-fail predictions
    pf_fragility = [None for _ in Discips]
    pf_std_fragility = [None for _ in Discips]
    
    # Prepare all data for testing
    test_data = prepareData(Discips, x_vars)
    
    # Loop through each discipline's test matrix
    for i, discip in enumerate(test_data):
        
        # Standardize the testing data
        x_test_scaled = scaler_x.fit_transform(discip)
        
        # Use the model to make predictions
        mu_scaled, sigma_scaled = model.predict(x_test_scaled)
        
        # Convert variances into standard deviations
        std_dev_scaled = np.sqrt(sigma_scaled)
        
        # Unstandardize the predictions
        mu_unscaled = scaler_y.inverse_transform(mu_scaled)
        std_dev_unscaled = std_dev_scaled * scaler_y.scale_
        
        # Normalize predictions and adjust standard deviations accordingly
        normalized_predictions, adjusted_std_devs = normalizePredictions(mu_unscaled, std_dev_unscaled)

        # Add the predictions and standard deviations to the fragility lists
        pf_fragility[i] = normalized_predictions.reshape(-1)
        pf_std_fragility[i] = adjusted_std_devs.reshape(-1)
       
    # Return the pass-fail predictions and standard deviations
    return pf_fragility, pf_std_fragility