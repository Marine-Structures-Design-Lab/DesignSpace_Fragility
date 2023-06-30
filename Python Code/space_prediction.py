"""
SUMMARY:

(May want to consider adding a StandardScalar from sklearn for x-input values)

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C
from scipy.stats import norm
import numpy as np
import sympy as sp
import warnings
from sklearn.exceptions import ConvergenceWarning

"""
SECONDARY FUNCTIONS
"""
def getLHS(rule):
    
    if isinstance(rule, sp.Rel):
        return rule.lhs
    elif isinstance(rule, (sp.And, sp.Or)):
        return getLHS(rule.args[0])


"""
CLASS
"""
# Turn off warning messages (free to adjust this)
warnings.filterwarnings('ignore', category=ConvergenceWarning)
warnings.filterwarnings('ignore', category=UserWarning)

class predictSpace:

    def __init__(self, x_train, y_train):
        """
        Description
        -----------
        

        Parameters
        ----------
        x_train : TYPE
            DESCRIPTION.
        y_train : TYPE
            DESCRIPTION.

        Returns
        -------
        None.
        """
        
        # Initalize an empty list of trained Gaussian process models
        self.models = []
        
        # Set intial kernel values for training model (free to adjust these)
        kernel = C(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e4))
        
        # Loop through each output variable
        for i in range(y_train.shape[1]):
            
            # Establish Gaussian process model to train (free to adjust these)
            model = GaussianProcessRegressor\
                (kernel=kernel, alpha=1e-10, n_restarts_optimizer=20)
            
            # Check if there is data to train the model
            if x_train.shape[0] > 0:
                
                # Train the model with provided input and output points
                model.fit(x_train, y_train[:, i])
            
            # Append the trained model to the list of trained models
            self.models.append(model)
        
        # Nothing to return
        return
    
    
    def predictOutput(self, x_test):
        
        # Initalize lists for predicted value and standard deviation arrays
        pred_list = []
        stddev_list = []
        
        # Loop through each trained Gaussian process model
        for model in self.models:
            
            # Check if there is data for testing the model
            if x_test.shape[0] > 0:
                
                # Evaluate predicted and standard deviation data of test values
                predictions, std_devs = \
                    model.predict(np.array(x_test), return_std=True)
            
            # Return empty arrays if no data for testing the model
            else:
                predictions = np.array([])
                std_devs = np.array([])
            
            # Append 2D numpy arrays of evaluated data to the proper list
            pred_list.append(predictions.reshape(-1, 1))
            stddev_list.append(std_devs.reshape(-1, 1))
        
        # Return the lists of numpy arrays
        return pred_list, stddev_list
        
    
    def getError(self, predictions, std_devs, confidence=0.95):
        
        # Determine the z-score given the desired confidence level
        z = norm.ppf((1 + confidence) / 2)
        
        # Initialize list for predict value bound arrays
        pred_bounds = []
        
        # Loop through each array of predictions
        for i in range(0, len(predictions)):
            
            # Calculate the lower and upper bounds of the predicted values
            lower_bounds = predictions[i] - z * std_devs[i]
            upper_bounds = predictions[i] + z * std_devs[i]
            
            # Stack the lower and upper bounds into an array
            bounds = np.column_stack((lower_bounds, upper_bounds))
            
            # Append the bounds to the predicted bounds list
            pred_bounds.append(bounds)
        
        # Return a list of the predicted value confidence bounds
        return pred_bounds
    
    
    def checkBounds(self, pred_bounds, output_rules, out_vars):
        
        # Initialize a numpy array for each predicted point and output rule
        success_range = np.zeros((pred_bounds[0].shape[0], len(output_rules)))
        
        # Loop through each output rule
        for rule in output_rules:
            
            # Gather the lhs of the output rule
            lhs = getLHS(rule)
            
            # 
            
            
            
            
        
        
        
        return success_range
