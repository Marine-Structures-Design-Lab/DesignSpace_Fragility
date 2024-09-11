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
import GPy
from GPy.util.multioutput import LCM
from sklearn.preprocessing import StandardScaler
from merge_constraints import trainData, normalizePredictions


"""
SECONDARY FUNCTION
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
    
    # Initialize a list of kernels
    kernels = [None for _ in Discips]
    
    # Initialize lists for x and y training data
    X_combined = [None for _ in Discips]
    Y_combined = [None for _ in Discips]
    
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
        
        # Store the x and y training data in the combined list
        X_combined[i] = x_train_scaled
        Y_combined[i] = y_train
        
        # Train and optimize the individual GPR
        kernels[i] = GPy.kern.RBF(input_dim=x_train_scaled.shape[1], ARD=True)
        gpr = GPy.models.GPRegression(x_train_scaled, y_train, kernels[i])
        gpr.optimize()
    
    # Create a Linear Coregionalization Model (LCM) to combine the kernels
    lcm = LCM(input_dim=[x_train_scaled.shape[1] for x_train_scaled in X_combined], 
              num_outputs=len(Discips),
              kernels_list=kernels)
    
    # Build and optimize the Multi-Output GPR model
    mogp = GPy.models.GPCoregionalizedRegression(X_combined, Y_combined, 
                                                 kernel=lcm)
    mogp.optimize()
    
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
        print(x_test_scaled)
        
        # Use the model to make predictions
        mu, sigma = mogp.predict(x_test_scaled, Y_metadata={'output_index': i})
        
        # Convert variances into standard deviations
        std_dev = np.sqrt(sigma)
        
        # Normalize predictions and adjust standard deviations accordingly
        normalized_predictions, adjusted_std_devs = \
            normalizePredictions(mu, std_dev)

        # Add the predictions and standard deviations to the fragility lists
        pf_fragility[i] = normalized_predictions.reshape(-1)
        pf_std_fragility[i] = adjusted_std_devs.reshape(-1)
       
    # Return the pass-fail predictions and standard deviations
    return pf_fragility, pf_std_fragility

