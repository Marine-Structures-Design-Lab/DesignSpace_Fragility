"""
SUMMARY:
Creates a Gaussian Process Regressor (GPR) that considers interdependencies of
shared design variables between disciplines to make more informed pass-fail
predictions in each discipline's remaining design space.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import numpy as np
import gpflow
from sklearn.preprocessing import StandardScaler
from merge_constraints import trainData, normalizePredictions


"""
TERTIARY FUNCTION
"""
def padData(x, target_dim):
    """
    Description
    -----------
    Pads an x-training array with columns of 0's to ensure each discipline's
    training array has the same number of columns.

    Parameters
    ----------
    x : Numpy array
        A particular discipline's x-training data before being padded
    target_dim : Integer
        Number of design variables in the discipline containing the most

    Returns
    -------
    x_padded : Numpy array
        A particular discipline's x-training data after being padded, if
        necessary
    """
    
    # Determine the number of design variables of the training data
    current_dim = x.shape[1]
    
    # Check if data's dimensions are less than maximum number of dimensions
    if current_dim < target_dim:
        
        # Pad the array with columns of 0.0's to match max number of dimensions
        x_padded = np.pad(x, ((0, 0), (0, target_dim - current_dim)), 
                          constant_values=0.0)
        
    # Do not pad the array if number of dimensions already maxed out
    else:
        x_padded = x
    
    # Return training data that may have been padded
    return x_padded


"""
SECONDARY FUNCTIONS
"""
def prepareTrain(Discips, target_dim):
    """
    Description
    -----------
    Organizes the training data of each discipline to be trained by a multi
    kernel Gaussian Process Regressor.
    
    Parameters
    ----------
    Discips : List of dictionaries
        All of the information pertaining to each discipline of the design
        problem.
    target_dim : Integer
        Number of design variables in the discipline containing the most

    Returns
    -------
    X : List of numpy arrays
        s-training data of each discipline for training the GP model
    Y : List of numpy arrays
        y-training data of each discipline for training the GP model
    scalers_x : List of objects
        Objects for each discipline to scale the x-training data
    """
    
    # Initialize lists for x and y training data
    X = [None for _ in Discips]
    Y = [None for _ in Discips]
    
    # Initialize a list of scalers for each discipline's x-training data
    scalers_x = [None for _ in Discips]
    
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
        
        # Create an array for the task index
        output_index = i * np.ones((x_train_scaled.shape[0], 1))
        
        # Add the task index to the training array
        x_train_scaled = np.hstack([output_index, x_train_scaled])
        
        # Pad the array if necessary
        x_padded = padData(x_train_scaled, target_dim)
        
        # Store the x and y training data in the combined list
        X[i] = x_padded
        Y[i] = y_train
    
    # Return lists of training and scaler data
    return X, Y, scalers_x


def executeTest(Discips, target_dim, scalers_x, model):
    """
    Description
    -----------
    Makes pass-fail predictions for the space remaining in each discipline
    using the multi kernel.
    
    Parameters
    ----------
    Discips : List of dictionaries
        All of the information pertaining to each discipline of the design
        problem.
    target_dim : Integer
        Number of design variables in the discipline containing the most
    scalers_x : List of objects
        Objects for each discipline to scale the x-training data
    model : GPFlow object
        Optimized GP model built from the multi kernel and training data of
        each discipline

    Returns
    -------
    pf_fragility : List of numpy arrays
        Predicted pass-fail amounts for the non-reduced design space in each
        discipline
    pf_std_fragility : List of numpy arrays
        Standard deviations of predicted pass-fail amounts for the non-reduced
        design space in each discipline
    """
    
    # Initialize lists for each discipline's array of pass-fail predictions
    pf_fragility = [None for _ in Discips]
    pf_std_fragility = [None for _ in Discips]
    
    # Loop through each discipline's test matrix
    for i, discip in enumerate(Discips):
        
        x_test = scalers_x[i].transform(discip['space_remaining']) \
            if discip['space_remaining'].size > 0 \
            else np.empty((0, len(discip['ins'])))
        
        # Standardize the testing data
        x_test_scaled = scalers_x[i].transform(x_test)
        
        # Create an array for the task index
        test_index = i * np.ones((x_test_scaled.shape[0], 1))
        
        # Add a column for the test index to the testing array
        x_test_scaled = np.hstack([test_index, x_test_scaled])
        
        # Pad the array if necessary
        x_test_padded = padData(x_test_scaled, target_dim)
        
        # Use the model to make predictions
        mu, sigma = model.predict_f(x_test_padded)
        
        # Convert variances into standard deviations
        std_dev = np.sqrt(sigma)
        
        # Normalize predictions and adjust standard deviations accordingly
        normalized_predictions, adjusted_std_devs = \
            normalizePredictions(mu, std_dev)

        # Add the predictions and standard deviations to the fragility lists
        pf_fragility[i] = normalized_predictions.reshape(-1)
        pf_std_fragility[i] = adjusted_std_devs.reshape(-1)
    
    # Return each discipline's interdependent pass-fail predictions
    return pf_fragility, pf_std_fragility


"""
MAIN FUNCTION
"""
def connectPerceptions(Discips):
    """
    Description
    -----------
    Forms a Gaussian Process regressor that is built with a kernel that
    combines the kernels of each individual discipline and then predicts the
    pass-fail amounts in each discipline with the trained model.

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
    
    # Determine number of design variables in discipline with the most
    target_dim = max([len(discip['ins'])+1 for discip in Discips])
    
    # Organize training data from each discipline
    X, Y, scalers_x = prepareTrain(Discips, target_dim)
        
    # Combine the input and output data from all of the disciplines
    X_full = np.vstack(X)
    Y_combined = np.vstack(Y)
    
    # Initialize a list of kernels
    kernels = [None for _ in Discips]
    
    # Loop through each discipline
    for i, discip in enumerate(Discips):
        
        # Define a list of active dimensions
        active_dim = list(range(1, len(discip['ins'])+1))
        
        # Define the kernel for the discipline
        kernels[i] = gpflow.kernels.RBF(len(discip['ins']),
                                        active_dims = active_dim)
    
    # Define the coregion kernel
    coregion_kernel = gpflow.kernels.Coregion(output_dim=len(Discips), rank=1,
                                              active_dims = [0])
    
    # Combine the kernels for each discipline using the coregion kernel
    multi_kernel = kernels[0]*coregion_kernel
    for i in range(1, len(kernels)):
        multi_kernel += kernels[i]*coregion_kernel
    
    # Build the multi-output Gaussian Process Regression (GPR) model
    model = gpflow.models.GPR(data=(X_full, Y_combined), kernel=multi_kernel)
    
    # Optimize the model using GPflow's SciPy optimizer
    optimizer = gpflow.optimizers.Scipy()
    optimizer.minimize(
        model.training_loss,
        model.trainable_variables,
        options=dict(maxiter=1000)
    )
    
    # Make pass-fail predictions in each discipline with the MOGP
    pf_fragility, pf_std_fragility = executeTest(Discips, target_dim, 
                                                 scalers_x, model)
       
    # Return the pass-fail predictions and standard deviations
    return pf_fragility, pf_std_fragility

