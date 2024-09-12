"""
SUMMARY:
Trains a new Gaussian process regressor with combined data from the explored
points of each discipline rather than just the data unique to each discipline
and then uses the regressor to predict pass-fail amounts in each discipline's
remaining design space.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import numpy as np
import gpflow
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from merge_constraints import trainData, normalizePredictions


"""
SECONDARY FUNCTIONS
"""
def organizeVars(Discips):
    """
    Description
    -----------
    

    Parameters
    ----------
    Discips : List of dictionaries
        All of the information pertaining to each discipline of the design
        problem.

    Returns
    -------
    x_vars : List
        Sympy variables for all of the design variables of the design problem.
    """
    
    # Initalize empty list for design variables
    x_vars = []
    
    # Loop through each discipline
    for i, discip in enumerate(Discips):
        
        # Loop through each design variable of the discipline
        for symbol in discip['ins']:
            
            # Check if variable is not already in the design variable list
            if symbol not in x_vars:
                
                # Append the variable to the design variable list
                x_vars.append(symbol)
 
    # Return full design variable list
    return x_vars


def padData(x, target_dim):
    
    current_dim = x.shape[1]
    
    if current_dim < target_dim:
        x_padded = np.pad(x, ((0, 0), (0, target_dim - current_dim)), 
                          constant_values=np.nan)
    else:
        x_padded = x
    
    return x_padded





"""
MAIN FUNCTION
"""
def connectPerceptions(Discips):
    """
    Description
    -----------
    

    Parameters
    ----------
    Discips : List of dictionaries
        All of the information pertaining to each discipline of the design
        problem.

    Returns
    -------
    pf_fragility : List of numpy arrays
        Predicted pass-fail amounts for the non-reduced design space in each
        discipline
    pf_std_fragility : List of numpy arrays
        Standard deviations of predicted pass-fail amounts for the non-reduced
        design space in each discipline
    """
    
    # Initialize lists for x and y training data
    X = [None for _ in Discips]
    Y = [None for _ in Discips]
    
    # Initalize list for output indices
    output_index = [None for _ in Discips]
    
    # Initialize a list of scalers for each discipline's x-training data
    scalers_x = [None for _ in Discips]
    
    # Determine number of design variables in discipline with the most
    target_dim = max([len(discip['ins']) for discip in Discips])
    
    # Loop through each discipline
    for i, discip in enumerate(Discips):
        
        # Initialize data for training a GPR
        x_train, y_train = trainData(discip)
        
        # Reshape the y training data
        y_train = y_train.reshape(-1, 1)
        
        # Standardize the x-training data
        scaler_x = StandardScaler()
        x_train_scaled = scaler_x.fit_transform(x_train)
        
        # Store the scaler for this discipline
        scalers_x[i] = scaler_x
        
        # Pad the array if necessary
        x_padded = padData(x_train_scaled, target_dim)
        
        # Store the x and y training data in the combined list
        X[i] = x_padded
        Y[i] = y_train
        
        # Create an array for the task index
        output_index[i] = i * np.ones((x_train_scaled.shape[0], 1))
    
    # Combine the input data from all of the disciplines
    X_combined = np.vstack(X)
    
    # Combine the task arrays from all of the disciplines
    output_index = np.vstack(output_index)
    
    # Add the output index to the x-training array
    X_full = np.hstack([X_combined, output_index])
    
    # Concatenate the outputs
    Y_combined = np.vstack(Y)
    
    # Initialize a list of kernels
    kernels = [None for _ in Discips]
    
    # Loop through each discipline
    for i, discip in enumerate(Discips):
        
        # Define a list of active dimensions
        active_dim = list(range(0, len(discip['ins'])))
        
        # Define the kernel for the discipline
        kernels[i] = gpflow.kernels.RBF(len(discip['ins']), active_dims = active_dim)
    
    # Define the coregion kernel
    coregion_kernel = gpflow.kernels.Coregion(output_dim=len(Discips), rank=1,
                                              active_dims = [target_dim])
    
    # Combine the kernels for each discipline using the coregion kernel
    multi_kernel = kernels[0]*coregion_kernel
    for i in range(1, len(kernels)):
        multi_kernel += kernels[i]*coregion_kernel
    
    # Build the multi-output Gaussian Process Regression (GPR) model
    model = gpflow.models.GPR(data=(X_full, Y_combined), kernel=multi_kernel)
    
    # Optimize the model using GPflow's SciPy optimizer
    optimizer = gpflow.optimizers.Scipy()
    result = optimizer.minimize(
        model.training_loss,
        model.trainable_variables,
        options=dict(maxiter=1000)
    )

    
    
    
    # Initialize lists for each discipline's array of pass-fail predictions
    pf_fragility = [None for _ in Discips]
    pf_std_fragility = [None for _ in Discips]
    
    # # Loop through each discipline's test matrix
    # for i, discip in enumerate(Discips):
        
    #     x_test = scalers_x[i].transform(discip['space_remaining']) \
    #         if discip['space_remaining'].size > 0 \
    #         else np.empty((0, len(discip['ins'])))
        
    #     # Standardize the testing data
    #     x_test_scaled = scalers_x[i].transform(x_test)
    #     print(x_test_scaled)
        
    #     # Use the model to make predictions
    #     mu, sigma = mogp.predict(x_test_scaled, Y_metadata={'output_index': i})
        
    #     # Convert variances into standard deviations
    #     std_dev = np.sqrt(sigma)
        
    #     # Normalize predictions and adjust standard deviations accordingly
    #     normalized_predictions, adjusted_std_devs = \
    #         normalizePredictions(mu, std_dev)

    #     # Add the predictions and standard deviations to the fragility lists
    #     pf_fragility[i] = normalized_predictions.reshape(-1)
    #     pf_std_fragility[i] = adjusted_std_devs.reshape(-1)
       
    # Return the pass-fail predictions and standard deviations
    return pf_fragility, pf_std_fragility

