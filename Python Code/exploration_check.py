"""
SUMMARY:
Contains methods with different strategies for checking the design spaces of
each discipline, proposing space reductions, and potentially adjusting the
threshold of criteria that dictate whether a space reduction is ready to be
proposed.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import numpy as np
import sympy as sp
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from sklearn import tree
from sklearn.tree import _tree
import matplotlib.pyplot as plt

"""
CLASS
"""
class checkSpace:
    
    # Initialize the class
    def __init__(self, variables, **kwargs):
        self.feature_names = variables
        self.regressor = DecisionTreeRegressor(**kwargs)
        self.inequalities = None
        return
    
    
    # Train and test the tree
    def buildTree(self, X, y, test_size=0.3, random_state=1, feature_names=None):
        
        # Assign points to the training and testing lists
        X_train, X_test, y_train, y_test =\
            train_test_split(X, y, test_size=test_size, random_state=random_state,)
            
        # Train Decision Tree Regressor
        self.regressor = self.regressor.fit(X_train, y_train)
        
        # Predict the response for test dataset
        y_pred = self.regressor.predict(X_test)
        
        # Compute the Mean Squared Error (MSE)
        mse = mean_squared_error(y_test, y_pred)

        # Or compute Root Mean Squared Error (RMSE)
        rmse = np.sqrt(mse)
        
        # Print error values and plot decision tree
        print("MSE:", mse)
        print("RMSE:", rmse)
        
        # Print the decision tree
        plt.figure(figsize=(15,10))
        tree.plot_tree(self.regressor, filled=True)
        plt.show()
        
        # Nothing to return
        return
    
    
    # Predicts target variable with the model
    def predict(self, X):
        
        # Return predicted data
        return self.regressor.predict(X)
    
    
    def extract_decision_rules(self):
        self.inequalities = self.tree_to_inequalities(self.regressor, self.feature_names)
        # for inequality in self.inequalities:
        #     print(inequality)
        return(self.inequalities)
    
    
    def tree_to_inequalities(self, tree, feature_names):
        """ Convert a decision tree to a list of sympy inequalities """
        tree_ = tree.tree_
        feature_symbols = self.feature_names
        
        paths = []
    
        def recurse(node, current_path):
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                feature = feature_symbols[tree_.feature[node]]
                threshold = tree_.threshold[node]
                
                # Create inequalities
                less_than_or_equal = sp.Le(feature, threshold)
                greater_than = sp.Gt(feature, threshold)
                
                # Recurse on child nodes
                recurse(tree_.children_left[node], current_path + [less_than_or_equal])
                recurse(tree_.children_right[node], current_path + [greater_than])
            else:
                paths.append(current_path)
    
        recurse(0, [])
        
        return paths








    

    



# Old variance code: 
# # Isolate tested input points that fail
# data = self.d[i]['tested_ins'][~np.array(self.d[i]['pass?'])]

# # Calculate variance of data for each dimension
# input_variance = np.var(data, axis=0)

# # Determine index of dimension for partitioning
# part_ind = np.argmin(input_variance)

# # Determine the input variable corresponding to this index
# part_var = self.d[i]['ins'][part_ind]