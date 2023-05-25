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
#from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import _tree
from scipy.stats import qmc
from scipy.spatial import cKDTree
#import matplotlib.pyplot as plt

"""
CLASS
"""
class checkSpace:
    
    # Initialize the class
    def __init__(self, variables, **kwargs):
        self.feature_names = variables
        self.classifier = DecisionTreeClassifier(**kwargs)
        self.inequalities = None
        return
    
    
    # Create an array of "good" and "bad" labels for failure amounts
    def goodBad(self, values, threshold):
        
        # Sort the failure amount values
        cdf_values = np.sort(values)
        
        # Determine the failure amount value defining the "good" and "bad" line
        separator = cdf_values[int((1-threshold)*len(cdf_values))]
        
        # Assign "bad" or "good" to the point
        ### Using > instead of >= here ensures failure amounts of 0.0 are never
        ### labeled as "bad"
        labels = ['bad' if v > separator else 'good' for v in values]
        
        # Convert list to a numpy array
        labels = np.array(labels)
        
        # Return the array of "good" and "bad" labels
        return labels
    
    
    # Train and show the decision tree
    def buildTree(self, X, y, test_size=0.3, random_state=1):
        
        # Assign points to the training and testing lists
        # X_train, X_test, y_train, y_test =\
        #     train_test_split(X, y, test_size=test_size, random_state=random_state,)
            
        # Train the decision tree classifier
        self.classifier = self.classifier.fit(X, y)
        # self.classifier = self.classifier.fit(X_train, y_train)
        
        # Print the decision tree
        # plt.figure(figsize=(15,10))
        # tree.plot_tree(self.classifier, filled=True)
        # plt.show()
        
        # Nothing to return
        return
    
    
    # Extract inequalities from the decision tree for the new rule proposal
    def extractRules(self, X, y):
        
        def tree_to_inequalities(tree, feature_names, X, y):
            
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
                    
                    # Count 'bad' points in the partition
                    partition_indices = tree.apply(X) == node
                    bad_count = np.sum(y[partition_indices] == 'bad')
                    bad_counts.append(bad_count)
            
            """ Convert a decision tree to a list of sympy inequalities """
            tree_ = tree.tree_
            feature_symbols = self.feature_names
            
            paths = []
            bad_counts = []
            
            recurse(0, [])
            
            return paths, bad_counts
        
        def remove_redundant_inequalities(inequalities):
            
            # Create a dictionary to store the maximum and minimum thresholds for each variable
            thresholds = {}
        
            for inequality in inequalities:
                
                # Get the variable and the threshold
                variable = str(inequality.lhs)
                threshold = inequality.rhs
        
                if variable not in thresholds:
                    if inequality.rel_op == '>':
                        thresholds[variable] = {'min': None, 'max': threshold}
                    else:  # inequality.rel_op == '<='
                        thresholds[variable] = {'min': threshold, 'max': None}
                else:
                    if inequality.rel_op == '>' and (thresholds[variable]['max'] is None or threshold > thresholds[variable]['max']):
                        thresholds[variable]['max'] = threshold
                    elif inequality.rel_op == '<=' and (thresholds[variable]['min'] is None or threshold < thresholds[variable]['min']):
                        thresholds[variable]['min'] = threshold
        
            # Build the unique inequalities list
            unique_inequalities = []
            for variable, bounds in thresholds.items():
                if bounds['min'] is not None:
                    unique_inequalities.append(sp.Le(sp.Symbol(variable), bounds['min']))
                if bounds['max'] is not None:
                    unique_inequalities.append(sp.Gt(sp.Symbol(variable), bounds['max']))
        
            return unique_inequalities
        
        # Gather inequalities of the decision tree's nodes
        self.inequalities, bad_counts =\
            tree_to_inequalities(self.classifier, self.feature_names, X, y)
        
        # Identify the partition with the most 'bad' points
        max_bad_index = np.argmax(bad_counts)
        rules_for_max_bad = self.inequalities[max_bad_index]
        
        # Remove redundant inequalities apart of the rule
        rules_for_max_bad_unique =\
            remove_redundant_inequalities(rules_for_max_bad)
            
        # Group rules into a
        
        #
        return rules_for_max_bad_unique
    
    
    # Check the maximum distance of a point to the nearest neighbor (point in the space I am looking at or not)
    # Check the uniformity of points in the space I am looking at spacifically
    def reviewPartitions(self, X, rules, fail_amount, fail_crit, dist_crit, disc_crit):
        
        def filter_points_within_bounds(X, fail_amount, inequalities):
            # Initialize a boolean array indicating whether each point is within the bounds
            is_within_bounds = np.ones(X.shape[0], dtype=bool)
        
            # Evaluate each inequality
            for inequality in inequalities:
                variable_index = self.feature_names.index(inequality.lhs)
                threshold = float(inequality.rhs)
        
                if inequality.rel_op == '>':
                    is_within_bounds = np.logical_and(is_within_bounds, X[:, variable_index] > threshold)
                else:  # inequality.rel_op == '<='
                    is_within_bounds = np.logical_and(is_within_bounds, X[:, variable_index] <= threshold)
        
            # Filter the points within the bounds
            X_within_bounds = X[is_within_bounds]
            
            # Gather the "good" or "bad" values of points within bounds
            FA_within_bounds = fail_amount[is_within_bounds]
            
            #
            return X_within_bounds, FA_within_bounds
        
        # Gather the points that meet the proposed inequalities
        X_bounds, FA_within_bounds = filter_points_within_bounds(X, fail_amount, rules)
        
        # Check that fraction of points with a 0.0 failure amount value in bounds does not exceed criterion
        zero_count = np.count_nonzero(FA_within_bounds == 0)
        fraction = (zero_count / len(FA_within_bounds))
        if fraction > fail_crit:
            return False
        
        # Create a KDTree with all points in the design space
        ### Train this with all passing and failing points, not just passing points at this point in time
        tree = cKDTree(X)
        
        # Find distances of each point within bounds to nearest point in ENTIRE design space
        ### This is where I would also want to know points that are in the fail group now
        distances, _ = tree.query(X_bounds, k=2)
        
        # The maximum distance to the nearest neighbor in the entire design space
        max_distance = np.max(distances[:, 1])
        
        # Check that max distance does not exceed criterion
        if max_distance > dist_crit:
            return False
        
        # Normalize the input points within the bounded inequality space
        if np.any(np.isclose(np.max(X_bounds,axis=0),np.min(X_bounds,axis=0))):
            return False
        else:
            X_scaled = (X_bounds - np.min(X_bounds, axis=0)) /\
                (np.max(X_bounds, axis=0) - np.min(X_bounds, axis=0))
        
        # Determine the uniformity of points meeting the proposed inequalities
        discrepancy = qmc.discrepancy(X_scaled)
        # MAYBE JUST LOOK AT 
        
        # Check that discrepancy does not exceed criterion
        if discrepancy > disc_crit:
            return False
        
        # Return True if distance and discrepancy criteria are met
        return True
    
    
    def prepareRule(self, pot_rules):
        
        # Define mapping for inverse inequality signs
        inv_ops = {sp.Gt: sp.Le, sp.Lt: sp.Ge, sp.Ge: sp.Lt, sp.Le: sp.Gt}
        
        # Define an empty list for the new rules
        new_rules = []
        
        # Loop through each inequality of the potential rules list
        for ineq in pot_rules:
            
            # Gather the inverse inequality sign of the original inequality
            inverse_op = inv_ops[type(ineq)]
            
            # Rewrite the inequality with the inverse inequality sign
            flipped_ineq = inverse_op(ineq.lhs, ineq.rhs)
            
            # Append the new inequality to the potential rules list
            new_rules.append(flipped_ineq)
        
        # Assign each inequality of the sub rules list as an Or argument
        # CONSIDER ONLY DOING THIS IF THERE IS MORE THAN ONE ARGUMENT TO ADD TO OR!!!
        or_relational = sp.Or(*new_rules)
        
        # Return the new rule as they sympy Or relational
        return or_relational

    

