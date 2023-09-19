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
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF


"""
CLASS
"""
class windfallRegret:
    
    def __init__(self, Discips):
        self.D = Discips
        return
    
    def trainData(self):
        
        # Initialize empty lists for training data arrays
        x_train = []
        y_train = []
        
        # Loop through each discipline
        for i in range(0, len(self.D)):
            
            # Combine tested input data from remaining and eliminated arrays
            x_train.append(self.D[i]['tested_ins'])
            if 'eliminated' in self.D[i]:
                x_train[i] = np.concatenate((x_train[i], \
                    self.D[i]['eliminated']['tested_ins']), axis=0)
            
            # Combine pass & fail amounts from remaining & eliminated arrays
            y_train.append(self.D[i]['Pass_Amount'] - self.D[i]['Fail_Amount'])
            if 'eliminated' in self.D[i]:
                y_train[i] = np.concatenate((y_train[i], \
                    self.D[i]['eliminated']['Pass_Amount'] - \
                    self.D[i]['eliminated']['Fail_Amount']))
            
        # Return training data
        return x_train, y_train
    
    def initializeFit(self, x_train, y_train):
        
        # Initialize empty list of GPR models
        gpr = []
        
        # Loop through each discipline
        for i in range(0, len(self.D)):
            
            # Initialize Gaussian kernel
            kernel = 1.0 * RBF(length_scale=np.ones(len(self.D[i]['ins'])), \
                               length_scale_bounds=(1e-2, 1e3))
            
            # Initialize Gaussian process regressor (GPR)
            gpr_model = GaussianProcessRegressor(kernel=kernel, alpha=0.00001)
            
            # Fit GPR with training data
            gpr_model.fit(x_train[i], y_train[i])

            # Append fitted model to list of GPR models
            gpr.append(gpr_model)
        
        # Return trained GPR
        return gpr
    
    def predictData(self, gpr):
        
        # Initialize empty lists for predicted arrays of each discipline
        passfail = []
        passfail_std = []
        
        # Loop through each discipline
        for i in range(0, len(self.D)):
            
            # Test GPR at each point remaining for discipline before new rule
            means, stddevs = gpr[i].predict(self.D[i]['space_remaining'], return_std=True)
            
            # Append arrays to empty lists
            passfail.append(means)
            passfail_std.append(stddevs)
        
        return passfail, passfail_std
    
    
