"""
SUMMARY:
This file ontains a class with methods that methodically propose an area of a
discipline's design space for a space reduction by labeling explored points as
"good" or "bad" depending on their failure amount values, training a decision
tree classifier to make single-variable partitions in the design space, and
then extracting those partitions as Sympy inequalities to work with them and
review them further.  This file also contains secondary and tertiary functions
located outside of the class to help each of the methods perform their tasks
more concisely.  Some code is left commented out to allow the programmer to
divide data into training and testing sets and plot the decision trees if they
so desire.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import numpy as np
import sympy as sp
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import _tree
from scipy.stats import qmc
from scipy.spatial import cKDTree
# from sklearn.model_selection import train_test_split
# import matplotlib.pyplot as plt
# from sklearn import tree

"""
TERTIARY FUNCTION
"""
def recurse(tree_, node, cur_p, feature_names, paths, bad_tot, bad_frac, X, y):
    """
    Description
    -----------
    Cycles through the child nodes of the decision tree until the leaf nodes
    are reached and creates a list of inequalities defining each branch from
    the root node to the leaf node while also determing the amount of "bad"
    points within each branch
    
    Parameters
    ----------
    tree_ : Tree
        A decision tree that has been trained
    node : Integer
        Current node ID of the decision tree
    cur_p : List of sympy inequalities
        Represents the current path from the root node to the current node of
        the decision tree
    feature_names : List of sympy symbols
        All of the input variables within the discipline's control
    paths : List of lists
        Contains all of the sympy inequalities defining each path
    bad_tot : List of integers
        A count of the total number of "bad" points in each leaf node
    bad_frac : List of floats
        The fraction of "bad" points to total points in each leaf node
    X : Numpy array
        Feature input data for which decision tree rules are being extracted
    y : Numpy vector
        Feature output data for which decision tree rules are being extracted
    
    Returns
    -------
    None - Updates the mutable lists of paths, bad_tot, and bad_frac without
    needing to return any of them
    """
    
    # Check if the current node is not a leaf node (i.e. no child nodes)
    if tree_.feature[node] != _tree.TREE_UNDEFINED:
        
        # Gather x-variable and decision threshold for current decision node
        feature = feature_names[tree_.feature[node]]
        threshold = tree_.threshold[node]
        
        # Create inequalities using the feature and threshold
        less_than_or_equal = sp.Le(feature, threshold)
        greater_than = sp.Gt(feature, threshold)
        
        # Call the recurse function on itself for the child nodes
        recurse(tree_, tree_.children_left[node], \
                cur_p + [less_than_or_equal], feature_names, paths, \
                bad_tot, bad_frac, X, y)
        recurse(tree_, tree_.children_right[node], \
                cur_p + [greater_than], feature_names, paths, \
                bad_tot, bad_frac, X, y)
    
    # Perform the following commands if the current node is a leaf node
    else:
        
        # Add the current decision path to the list of paths
        paths.append(cur_p)
        
        # Create a boolean array where "True" values indicate samples in X that
        ### fall within the current leaf node's partition
        partition_indices = tree_.apply(X) == node
        
        # Count the total number of points within the current partition
        total_count = np.sum(partition_indices)
        
        # Count the number of "bad" points in the partition
        bad_total = np.sum(y[partition_indices] == 'bad')
        
        # Append the number of "bad" points in the partition to bad_tot list
        bad_tot.append(bad_total)
        
        # Calculate the fraction of "bad" points in the partition
        bad_fraction = bad_total / total_count if total_count != 0 else 0
        
        # Add the calculated fraction to the bad_counts list
        bad_frac.append(bad_fraction)


"""
SECONDARY FUNCTIONS
"""
# Convert decision tree to a list of sympy inequalities
def getInequalities(tree, feature_names, X, y):
    """
    Description
    -----------
    Gathers all of the inequalities for each path of the decision tree along
    with statistics on the total number and fraction of bad points within the
    space defined by each path
    
    Parameters
    ----------
    tree : Tree
        A decision tree that has been trained
    feature_names : List of sympy symbols
        All of the input variables within the discipline's control
    X : Numpy array
        Feature input data for which decision tree rules are being extracted
    y : Numpy vector
        Feature output data for which decision tree rules are being extracted

    Returns
    -------
    paths : Nested list of sympy inequalities
        Each nested list contains all of the inequalities that define a branch
        of the decision tree
    bad_tot : List of integers
        The total number of "bad" points located in each branch of the decision
        tree
    bad_frac : List of floats
        The fraction of "bad" points to total points in each branch of the
        decision tree
    """
    
    # Initialize empty lists (mutable objects) for inequalities and bad points
    paths = []
    bad_tot = []
    bad_frac = []
    
    # Call the recurse function from the decision tree's initial root node
    recurse(tree.tree_, 0, [], feature_names, paths, bad_tot, bad_frac, X, y)
    
    # Return mutable lists for decision tree paths and "bad" variable counts
    return paths, bad_tot, bad_frac


def redundantIneqs(inequalities):
    """
    Description
    -----------
    Checks if any inequalities of the decision tree's extracted rule describe
    any overlapping regions, and if so, simplifies those inequalities into a
    single inequality describing the redundant space

    Parameters
    ----------
    inequalities : List of sympy inequalities
        The inequalities describing the area of the design space the decision
        tree is suggesting be removed

    Returns
    -------
    unique_ineqs : List of sympy inequalities
        The same inequalities but with potential redundancies removed
    """
    
    # Create a dictionary for storing max and min thresholds of each variable
    thresholds = {}
    
    # Loop through each inequality in the list of inequalities
    for inequality in inequalities:
        
        # Get the variable and the threshold
        variable = inequality.lhs
        threshold = inequality.rhs
        
        # Check if variable not already been defined in thresholds dictionary
        if variable not in thresholds:
            
            # Check if inequality has a greater than sign
            if inequality.rel_op == '>':
                
                # Assign the threshold to the maximum value for the variable
                thresholds[variable] = {'min': None, 'max': threshold}
                
            # Perform the following command for the less than or equal to sign
            else:
                
                # Assign the threshold to the minimum value for the variable
                thresholds[variable] = {'min': threshold, 'max': None}
        
        # Perform following commands if variable has been defined in dictionary
        else:
            
            # Check if inequality has a greater than sign and if the max
            ### threshold is none or the new threshold is greater than the
            ### current max threshold
            if inequality.rel_op == '>' and \
                (thresholds[variable]['max'] is None or \
                 threshold > thresholds[variable]['max']):
                    
                # Assign new threshold to maximum threshold for variable
                thresholds[variable]['max'] = threshold
                
            # Check if inequality has a less than or equal to sign and if the
            ### min threshold is none or the new threshold is less than the
            ### current min threshold
            elif inequality.rel_op == '<=' and \
                (thresholds[variable]['min'] is None or \
                 threshold < thresholds[variable]['min']):
                
                # Assign new threshold to minimum threshold for variable
                thresholds[variable]['min'] = threshold

    # Create an empty unique inequalities list
    unique_ineqs = []
    
    # Loop through each variable in the thresholds dictionary
    for variable, bounds in thresholds.items():
        
        # Check if the variable's min bound is not none
        if bounds['min'] is not None:
            
            # Append the new inequality rule to the unique inequalities list
            unique_ineqs.append(sp.Le(variable, bounds['min']))
            
        # Check if the variable's max bound is not none
        if bounds['max'] is not None:
            
            # Append the new inequality rule to the unique inequalities list
            unique_ineqs.append(sp.Gt(variable, bounds['max']))
    
    # Return the nonredundant inequalities list
    return unique_ineqs


def filterPoints(X, fail_amount, inequalities, feature_names):
    """
    Description
    -----------
    Gather the input locations and failure amounts for all of the tested input
    points meeting all of the inequalities of the potential rule
    
    Parameters
    ----------
    X : Numpy array
        Feature input data for which decision tree inequalities are being
        evaluated
    fail_amount : Numpy vector
        Failure amounts of output data to output rules corresponding to
        featured input data
    inequalities : List of sympy inequalities
        The inequalities describing the area of the design space the decision
        tree is suggesting be removed
    feature_names : List of sympy symbols
        All of the input variables within the discipline's control
    
    Returns
    -------
    X_within_bounds : Numpy array
        Filtered X-data satisfying all the inequalities
    FA_within_bounds : Numpy vector
        Filtered failure amount data satisfying all the inequalities
    """
    
    # Initialize an empty boolean array of True values for points within bounds
    is_within_bounds = np.ones(X.shape[0], dtype=bool)

    # Loop through each inequality of potential rule
    for inequality in inequalities:
        
        # Determine input variable index and threshold of inequality
        var_index = feature_names.index(inequality.lhs)
        threshold = float(inequality.rhs)
        
        # Check if inequality has a greater than sign
        if inequality.rel_op == '>':
            
            # Check each remaining True value to see if input point meets the
            ### bound of the newest greater than inequality
            is_within_bounds = np.logical_and(is_within_bounds, \
                                              X[:, var_index] > threshold)
        
        # Perform the following command for less than or equal to inequality
        else:
            
            # Check each remaining True value to see if input point meets the
            ### bound of the newest less than or equal to inequality
            is_within_bounds = np.logical_and(is_within_bounds, \
                                              X[:, var_index] <= threshold)
    
    
    # Filter the input points satisfying all inequalities
    X_within_bounds = X[is_within_bounds]
    
    # Filter the failure amount values of points satisfying all inequalities
    FA_within_bounds = fail_amount[is_within_bounds]
    
    # Return the filtered input and output arrays
    return X_within_bounds, FA_within_bounds


"""
CLASS
"""
class checkSpace:
    
    def __init__(self, variables, **kwargs):
        """
        Parameters
        ----------
        variables : List of sympy symbols
            All of the input variables within the discipline's control
        **kwargs : Dictionary
            All of the keyword arguments of the decision tree classifier
        """
        self.feature_names = variables
        self.classifier = DecisionTreeClassifier(**kwargs)
        self.inequalities = None
        return
    
    
    def goodBad(self, values, threshold):
        """
        Description
        -----------
        Create an array of "good" and "bad" labels based on the user-
        initialized cdf threshold amount for training the decision tree
        
        Parameters
        ----------
        values : Numpy array
            The failure amount values being used to make the "good" and "bad"
            labels for each data point
        threshold : Float
            The discipline specific decimal value that determines what fraction
            of points are to be labeled "bad" vs. "good" at the particular
            moment in time

        Returns
        -------
        labels : Numpy array
            A one-dimensional vector containing a "good" or "bad" label that
            corresponds to the same indices of the discipline's tested points
            thus far
        """
        
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
    
    
    def buildTree(self, X, y, test_size=0.3, random_state=1):
        """
        Description
        -----------
        Builds the decision tree with the data provided while also providing
        options to separate data into train and testing sets in case the
        decision tree needs to be tested as well as visualizing the decision
        tree with a tree diagram

        Parameters
        ----------
        X : Numpy array
            The coordinates of the input points being used as input data to
            train the decision tree
        y : Numpy vector
            The vector of "good" and "bad" values being used as output data to
            train the decision tree
        test_size : Float, optional
            The fraction of the data set to use for testing instead of training
        random_state : Integer, optional
            The seed to use for randomization of training vs. testing data to
            help replicate results

        Returns
        -------
        None - The self.classifier variable is reestablished but not returned
        """
        
        # Assign points to the training and testing lists
        #X_train, X_test, y_train, y_test = train_test_split\
        #    (X, y, test_size=test_size, random_state=random_state, )
        
        # Train the decision tree classifier
        self.classifier = self.classifier.fit(X, y)
        # self.classifier = self.classifier.fit(X_train, y_train)
        
        # Print the decision tree
        # plt.figure(figsize=(15,10))
        # tree.plot_tree(self.classifier, filled=True)
        # plt.show()
        
        # Nothing to return
        return
    
    
    def extractRules(self, X, y):
        """
        Description
        -----------
        Create inequalities from the partitions of the decision tree
        encompassing the highest fraction of "bad" points without any
        redundancies that will be used to (potentially) propose a new rule

        Parameters
        ----------
        X : Numpy array
            Feature input data for which decision tree rules are being
            extracted
        y : Numpy vector
            Feature output data for which decision tree rules are being
            extracted

        Returns
        -------
        bad_rule : List of sympy inequalities
            Inequalities that define the unique branch of the decision tree
            that the discipline will consider eliminating
        """
        
        # Gather inequalities of the decision tree's nodes
        self.inequalities, bad_tot, bad_frac = \
            getInequalities(self.classifier, self.feature_names, X, y)
        
        # Identify the partition(s) with the highest fraction of "bad" points
        max_index = np.where(bad_frac == np.max(bad_frac))[0].tolist()
        
        # Check if multiple indices having the highest fraction of "bad" points
        if len(max_index) > 1:
            
            # Identify the partition with the highest total of "bad" points
            bad_index = np.argmax(np.array(bad_tot)[max_index])
            max_index = max_index[bad_index]
        
        # Perform the following commands if one index with highest fraction
        else:
            
            # Remove the one argument from the list
            max_index = max_index[0]
        
        # Isolate the inequalities of the leaf node with the "worst" points
        bad_rule = self.inequalities[max_index]
        
        # Remove redundant inequalities apart of the rule
        bad_rule = redundantIneqs(bad_rule)
        
        # Return the list of non-redundant inequalities describing the rule
        return bad_rule

    
    def reviewPartitions(self, X, rule, fail_amount, \
                         fail_crit, dist_crit, disc_crit):
        """
        Description
        -----------
        Evaluate various criteria within the area of the discipline's design 
        space to be reduced to ensure that area has been reasonably explored
        before committing to proposing the reduction
        
        Parameters
        ----------
        X : Numpy array
            Feature input data for which decision tree partitions are being
            reviewed
        rule : List of sympy inequalities
            Describing the particular area of the design space that is being
            reviewed for potential reduction
        fail_amount : Numpy vector
            Failure amounts of output data to established output rules
        fail_crit : Float
            The discipline-specific maximum fraction of feasible input points
            allowed in the area of the design space being reviewed for removal
        dist_crit : Float
            The discipline-specific maximum distance of normalized points
            within the area of the design space being reviewed for removal to
            any nearest neighbor in the input space
        disc_crit : Float
            The discipline-specific maximum uniformity metric of points within
            the area of the design space being reviewed for removal (where 0.0
            indicates high uniformity and 1.0 indicates low uniformity)
        
        Returns
        -------
        True or False
            False returned at any point a criterion is not met, True returned
            otherwise (meaning all criteria are met)
        """
        
        # Return false if no rule being proposed by the discipline
        if not rule:
            return False
        
        # Filter points and failure amounts that meet the proposed inequalities
        X_bounds, FA_bounds = \
            filterPoints(X, fail_amount, rule, self.feature_names)
        
        # Check that fraction of filtered points with a 0.0 failure amount
        ### value does not exceed criterion
        zero_count = np.count_nonzero(FA_bounds == 0.0)
        fraction = (zero_count / len(FA_bounds))
        if fraction > fail_crit:
            return False
        
        # Create a KDTree that is trained with ALL points in the design space
        tree = cKDTree(X)
        
        # Find distances of points within bounds to nearest one in ENTIRE space
        distances, _ = tree.query(X_bounds, k=2)
        
        # Get maximum nearest neighbor distance in the entire design space
        max_distance = np.max(distances[:, 1])
        
        # Check that max distance does not exceed criterion
        if max_distance > dist_crit:
            return False
        
        # Check that max and min values of each input variable in X_bounds is
        ### far enough apart such that a normalized box can form around points
        if np.any(np.isclose(np.max(X_bounds,axis=0),np.min(X_bounds,axis=0))):
            return False
        else:
            # Normalize the input points within the bounded inequality space
            X_scaled = (X_bounds - np.min(X_bounds, axis=0)) /\
                (np.max(X_bounds, axis=0) - np.min(X_bounds, axis=0))
        
        # Determine the uniformity of points meeting the proposed inequalities
        discrepancy = qmc.discrepancy(X_scaled)
        
        # Check that discrepancy does not exceed criterion
        if discrepancy > disc_crit:
            return False
        
        # Return True as all criteria are met
        return True
    
    
    def prepareRule(self, pot_rule):
        """
        Description
        -----------
        Flip signs of inequalities making up the potential rule and store the
        inequalities as arguments in an Or relational so that the rule
        describes the space still open to the discipline rather than the space
        being eliminated

        Parameters
        ----------
        pot_rule : List of sympy inequalities
            Describes the particular area of the design space that is being
            manipulated for potential reduction

        Returns
        -------
        or_relational : Sympy relational or inequality
            Describes the area of the design space that will remain open to the
            discipline after elimination of the pot_rule space
        """
        
        # Define mapping for inverse inequality signs
        inv_ops = {sp.Gt: sp.Le, sp.Lt: sp.Ge, sp.Ge: sp.Lt, sp.Le: sp.Gt}
        
        # Define an empty list for the new rules
        new_rules = []
        
        # Loop through each inequality of the potential rule list
        for ineq in pot_rule:
            
            # Gather the inverse inequality sign of the original inequality
            inverse_op = inv_ops[type(ineq)]
            
            # Rewrite the inequality with the inverse inequality sign
            flipped_ineq = inverse_op(ineq.lhs, ineq.rhs)
            
            # Append the new inequality to the new potential rule list
            new_rules.append(flipped_ineq)
        
        # Assign each inequality of the sub rules list as an Or argument
        ### This will simplify to the argument itself if there is only one
        ### argument being passed to sp.Or in new_rules
        or_relational = sp.Or(*new_rules)
        
        # Return the new rule with the flipped inequality signs
        return or_relational
