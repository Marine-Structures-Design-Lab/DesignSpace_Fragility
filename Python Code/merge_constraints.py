"""
SUMMARY:
Takes all of the input rules proposed from each discipline in a particular
space reduction cycle and proposes a universal set of space reductions for each
discipline to abide by based on their respective opinions of each reduction.  

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from point_sorter import sortPoints
from sklearn.gaussian_process.kernels import RBF
from sklearn.preprocessing import StandardScaler
from sklearn.gaussian_process import GaussianProcessRegressor
from scipy.stats import norm
from scipy.optimize import fsolve
# import matplotlib.pyplot as plt
import numpy as np
import copy
import itertools


"""
TERTIARY FUNCTIONS
"""
def sharedIndices(A, B):
    """
    Description
    -----------
    Analyzes a discipline without a proposed space reduction (A) and a
    discipline with a proposed space reduction (B) and organizes the indices of
    the points in the space remaining into lists for the non-reduced, reduced,
    and leftover (eliminated) areas of the design space.

    Parameters
    ----------
    A : Numpy array
        Coordinates of remaining areas in the design space not including the
        newly considered space reduction
    B : Numpy array
        Coordinates of remaining areas in the design space including the newly
        considered space reduction

    Returns
    -------
    all_indices : List
        Indices of points in A (non-reduced design space)
    indices_in_both : List
        Indices of points in A that are also found in B (reduced design space)
    indices_not_in_B : List
        Indices of points in A that are not found in B (leftover design space /
        area of the design space up for elimination)
    """
    
    # Convert rows to tuples for set operations
    A_rows = set(map(tuple, A))
    B_rows = set(map(tuple, B))
    
    # Find rows in A that are not in B
    diff_rows = A_rows - B_rows
    
    # Get indices of A for rows that are not in B
    indices_not_in_B = \
        [i for i, row in enumerate(A) if tuple(row) in diff_rows]
    
    # Get indices of A for rows that are in both A and B
    indices_in_both = \
        [i for i, row in enumerate(A) if tuple(row) not in diff_rows]
    
    # Get all indices of A
    all_indices = list(range(len(A)))
    
    # Return each list of indices
    return all_indices, indices_in_both, indices_not_in_B


def trainData(discip):
    """
    Description
    -----------
    Organize previously tested points into x and y training data for a Gaussian
    Process Regressor (GPR).

    Parameters
    ----------
    discip : Dictionary
        Contains all of the information relevant to the discipline

    Returns
    -------
    x_train : Numpy array
        Input coordinates of previously tested design points
    y_train : Numpy array
        Pass or Fail amounts of previously tested design points
    """
    
    # Combine tested input data from remaining and eliminated arrays
    x_train = discip['tested_ins']
    if 'eliminated' in discip:
        x_train = np.concatenate((x_train, \
            discip['eliminated']['tested_ins']), axis=0)
    
    # Combine pass & fail amounts from remaining & eliminated arrays
    y_train = discip['Pass_Amount'] - discip['Fail_Amount']
    if 'eliminated' in discip:
        y_train = np.concatenate((y_train, \
            discip['eliminated']['Pass_Amount'] - \
            discip['eliminated']['Fail_Amount']))
    
    # Return training data
    return x_train, y_train


def initializeFit(discip, x_train, y_train, **kwargs):
    """
    Description
    -----------
    Fits a GPR from the training data.

    Parameters
    ----------
    discip : Dictionary
        Contains all of the information relevant to the discipline
    x_train : Numpy array
        Input coordinates of previously tested design points
    y_train : Numpy array
        Pass or Fail amounts of previously tested design points
    kwargs : Dictionary, optional
        Additional keyword arguments for GPR model configuration. Common 
        parameters include 'length_scale_bounds' for the RBF kernel
        (default: (1e-2, 1e3)) and 'alpha' for GaussianProcessRegressor
        (default: 0.4 / np.sqrt(len(x_train))) ** 2). These parameters are used 
        to control various aspects of the GPR model, such as kernel properties 
        and regularization
    
    Returns
    -------
    gpr_model : GaussianProcessRegressor
        A trained GPR model
    """
    
    # Extract parameters from kwargs or set default values
    length_scale_bounds = kwargs.get('length_scale_bounds', (1e-3, 1e2))
    alpha = kwargs.get('alpha', (0.4 / np.sqrt(len(x_train))) ** 2)
    
    # Initialize Gaussian kernel
    kernel = 1.0 * RBF(length_scale=np.ones(len(discip['ins'])), 
                       length_scale_bounds=length_scale_bounds)
    gpr_model = GaussianProcessRegressor(kernel=kernel, alpha=alpha)
    
    # Initialize Gaussian process regressor (GPR)
    gpr_model = GaussianProcessRegressor(kernel=kernel, alpha=alpha)
    
    # Fit GPR with training data
    gpr_model.fit(x_train, y_train)
    
    # Return trained GPR
    return gpr_model


def analyzeInfeasibility(predictions, std_devs):
    """
    Description
    -----------
    Calculate the range of each predicted point within 3 standard deviations
    (99.7%) and then determine the average fraction of that range that has a
    predicted pass or fail amount falling below 0.

    Parameters
    ----------
    predictions : Numpy array
        Predicted pass or fail amounts of the area of the design space up for
        elimination.
    std_devs : Numpy array
        Standard deviations of predicted pass or fail amounts of the area of
        the design space up for elimination.

    Returns
    -------
    average_infeasibility : Float
        Average fraction of the design space with pass or fail amounts below 0
    """
    
    # Initialize a variable that sums contributions of each predicted point
    total_above_zero = 0
    
    # Loop through each predicted value
    for pred, std_dev in zip(predictions, std_devs):
        
        # Calculate bounds of prediction within 3 standard deviations
        lower_bound = pred - 3 * std_dev
        upper_bound = pred + 3 * std_dev
        
        # If entire interval is below 0, assign 0 to decimal
        if upper_bound <= 0: decimal_above_zero = 0
        
        # Else if entire interval is above 0, assign 1 to decimal
        elif lower_bound >= 0: decimal_above_zero = 1
        
        # Else calculate the fraction of the interval above 0
        else: decimal_above_zero = (upper_bound-0) / (upper_bound-lower_bound)
        
        # Add the decimal to the sum of contributions
        total_above_zero += decimal_above_zero

    # Return 0 if sum is zero, else calculate the average decimal below zero
    return 0 if total_above_zero == 0 \
        else (1 - (total_above_zero / len(predictions)))


def analyzeFeasibility(means1, std_devs1, means2, std_devs2):
    """
    Description
    -----------
    Calculate the fraction of each point's normal distribution for predicted
    pass or fail value that is above 0 for the reduced and non-reduced design
    spaces.  Then sum those fractions and find the ratio of the reduced sum to
    the non-reduced sum.

    Parameters
    ----------
    means1 : Numpy array
        Predicted pass or fail amounts of the reduced design space
    std_devs1 : Numpy array
        Standard deviations of the predicted pass or fail amounts of the
        reduced design space
    means2 : Numpy array
        Predicted pass or fail amounts of the non-reduced design space
    std_devs2 : Numpy array
        Standard deviations of the predicted pass or fail amounts of the
        non-reduced design space

    Returns
    -------
    average_feasibility : Float
        Fraction of remaining feasible space of the reduced design space
        relative to the non-reduced design space
    """
    
    # Initialize variables that sum contributions of each predicted point
    total_above_zero_1 = 0
    total_above_zero_2 = 0

    # Calculate fraction of distribution above 0 for first set of predictions
    for mean, std_dev in zip(means1, std_devs1):
        cdf_at_zero = norm.cdf(0, loc=mean, scale=std_dev)
        decimal_above_zero = 1 - cdf_at_zero
        total_above_zero_1 += decimal_above_zero

    # Calculate fraction of distribution above 0 for second set of predictions
    for mean, std_dev in zip(means2, std_devs2):
        cdf_at_zero = norm.cdf(0, loc=mean, scale=std_dev)
        decimal_above_zero = 1 - cdf_at_zero
        total_above_zero_2 += decimal_above_zero

    # Calculate and return percentage of first set relative to second set
    return total_above_zero_1 / total_above_zero_2 if total_above_zero_2 != 0 \
        else 0


def bezierPoint(m1, **kwargs):
    """
    Description
    -----------
    Calculate the weighted contribution of the second metric (feasibility)
    based on the value of the first metric with a Quadratic Bezier curve.
    
    Parameters
    ----------
    m1 : Float
        Average fraction of the design space up for elimination with pass or
        fail amounts below 0
    kwargs : Dictionary, optional
        x and y coordinates of control points of quadratic Bezier curve
    
    Returns
    -------
    y : Float
        Weight of second metric (feasibility)
    """
    
    # Extract control points for Quadratic Bezier curve or set default ones
    P0 = kwargs.get('P0', (0.0, 1.0))
    P1 = kwargs.get('P1', (0.5, 0.8))
    P2 = kwargs.get('P2', (1.0, 0.0))

    # Define the x-coordinate of the Bezier curve
    def bezier_x(t):
        return (1 - t)**2 * P0[0] + 2 * (1 - t) * t * P1[0] + t**2 * P2[0] - m1

    # Solve for t where x(t) = m1
    t_solution = fsolve(bezier_x, 0.5)[0]  # Initial guess is 0.5

    # Ensure t is in the range [0, 1]
    if not 0 <= t_solution <= 1:
        return None

    # Calculate the y-coordinate at the solved t
    y = (1 - t_solution)**2 * P0[1] + \
        2 * (1 - t_solution) * t_solution * P1[1] + \
        t_solution**2 * P2[1]
    
    # Return the y-coordinate which is the weight of the feasibility metric
    return y


"""
SECONDARY FUNCTIONS
"""
def getPerceptions(discip, gpr_params):
    """
    Description
    -----------
    Predict the passing or failure amounts for each point in the non-reduced
    design space of each discipline.

    Parameters
    ----------
    discip : Dictionary
        Contains all of the information relevant to the discipline
    gpr_params : Dictionary
        Additional keyword arguments for GPR model configuration. Common 
        parameters include 'length_scale_bounds' for the RBF kernel
        (default: (1e-2, 1e3)) and 'alpha' for GaussianProcessRegressor
        (default: 0.00001). These parameters are used to control various
        aspects of the GPR model, such as kernel properties and regularization
    
    Returns
    -------
    normalized_predictions : Numpy array
        Normalized predicted passing or failing amounts for non-reduced design
        space of particular discipline
    adjusted_std_devs : Numpy array
        Adjusted standard deviations associated with predicted passing or
        failing amounts
    """
    
    # Initialize data for training a GPR
    x_train, y_train = trainData(discip)
    
    # Standardize the training data
    scaler_x = StandardScaler()
    x_train_scaled = scaler_x.fit_transform(x_train)
    scaler_y = StandardScaler()
    y_train_scaled = scaler_y.fit_transform(y_train.reshape(-1, 1)).ravel()

    # # Plot histograms of y_train before and after scaling
    # plt.figure(figsize=(12, 5))
    
    # plt.subplot(1, 2, 1)
    # plt.hist(y_train, bins=30, alpha=0.7, color='blue')
    # plt.title('Histogram of y_train')
    
    # plt.subplot(1, 2, 2)
    # plt.hist(y_train_scaled, bins=30, alpha=0.7, color='green')
    # plt.title('Histogram of y_train_scaled')
    
    # plt.show()

    # Train GPR
    gpr = initializeFit(discip, x_train_scaled, y_train, **gpr_params)
    
    # Standardize the x-data for which pass-fail amounts will be predicted
    x_space_scaled = scaler_x.transform(discip['space_remaining']) \
        if discip['space_remaining'].size > 0 \
        else np.empty((0, len(discip['ins'])))

    # Predict pass-fail data at every point in non-reduced design space
    if len(x_space_scaled) > 0:
        pf_mean, pf_std = gpr.predict(x_space_scaled, return_std=True)
        # pf_mean = \
        #     scaler_y.inverse_transform(pf_mean_scaled.reshape(-1, 1)).ravel()
    else:
        pf_mean = np.empty(0)
        pf_std = np.empty(0)
    
    # Separate negative and positive predictions
    neg_predictions = pf_mean[pf_mean < 0.0]
    pos_predictions = pf_mean[pf_mean >= 0.0]
    
    # Normalize negative predictions to be between -1 and 0
    if len(neg_predictions) >= 1:
        min_neg = np.min(neg_predictions)
        max_neg = np.max(neg_predictions)
        if max_neg != min_neg:
            normalized_neg_predictions = -1 + ((neg_predictions - min_neg) / \
                                               (max_neg - min_neg))
            scale_factor_neg = 1 / (max_neg - min_neg)
        else:
            normalized_neg_predictions = neg_predictions
            scale_factor_neg = 1.0
    else:
        normalized_neg_predictions = np.empty(0)
    
    # Normalize positive predictions to be between 0 and 1
    if len(pos_predictions) >= 1:
        min_pos = np.min(pos_predictions)
        max_pos = np.max(pos_predictions)
        if max_pos != min_pos:
            normalized_pos_predictions = (pos_predictions - min_pos) / \
                (max_pos - min_pos)
            scale_factor_pos = 1 / (max_pos - min_pos)
        else:
            normalized_pos_predictions = pos_predictions
            scale_factor_pos = 1.0
    else:
        normalized_pos_predictions = np.empty(0)
    
    # Combine normalized predictions
    normalized_predictions = np.zeros_like(pf_mean)
    if len(neg_predictions) > 0:
        normalized_predictions[pf_mean < 0.0] = normalized_neg_predictions
    if len(pos_predictions) > 0:
        normalized_predictions[pf_mean >= 0.0] = normalized_pos_predictions
    
    # Adjust standard deviations proportionally
    adjusted_std_devs = np.zeros_like(pf_std)
    if len(neg_predictions) > 0:
        adjusted_std_devs[pf_mean < 0.0] = pf_std[pf_mean < 0.0] * \
            scale_factor_neg
    if len(pos_predictions) > 0:
        adjusted_std_devs[pf_mean >= 0.0] = pf_std[pf_mean >= 0.0] * \
            scale_factor_pos
    
    # Return the normalized predicted data
    return normalized_predictions, adjusted_std_devs


def getPredictions(discip, rule, pf_mean, pf_std):
    """
    Description
    -----------
    Organize predicted passing or failure amounts into categories for the
    non-reduced, reduced, and leftover design spaces of the discipline for a
    particular rule or rule set being proposed.

    Parameters
    ----------
    discip : Dictionary
        Contains all of the information relevant to the discipline
    rule : Tuple of Sympy relational(s)
        Either a sympy And or Or relational or a sympy inequality describing
        the input rule for which discipline is categorizing design spaces
    pf_mean : Numpy array
        Predicted passing or failing amounts for non-reduced design space of
        particular discipline
    pf_std : Numpy array
        Standard deviations associated with predicted passing or failing
        amounts

    Returns
    -------
    passfail : Dictionary
        Predicted passing or failing amounts for each design space of
        discipline considering the particular rule set
    passfail_std : Dictionary
        Standard deviations associated with categorized passing or failing
        amounts
    """
    
    # Make a copy of the discipline taking the input rule(s) into account
    d_copy = copy.deepcopy(discip)
    
    # Add values to eliminated section of discipline copy for new input rule
    d_copy = sortPoints([d_copy], list(rule))
    
    # Create different index lists based on new input rule(s)
    all_indices, indices_in_both, indices_not_in_B = \
        sharedIndices(discip['space_remaining'], d_copy[0]['space_remaining'])
    
    # Add each list to a different dictionary key
    diction = {"non_reduced": all_indices, 
               "reduced": indices_in_both, 
               "leftover": indices_not_in_B}
    
    # Initialize passfail dictionaries
    passfail = {}
    passfail_std = {}
    
    # Loop through each list of indices in dictionary
    for key in diction:
        
        # Assign predicted data to proper dictionary key
        passfail[key] = pf_mean[diction[key]]
        passfail_std[key] = pf_std[diction[key]]
    
    # Return passfail data for the rule
    return passfail, passfail_std


def getOpinion(rule, discip, passfail, passfail_std, bez_point):
    """
    Description
    -----------
    Calculate the discipline's opinion of the rule with passing and failure
    amount data and corresponding perceived infeasibility and feasibility to 
    produce two metrics.

    Parameters
    ----------
    rule : Sympy relational
        Either a sympy And or Or relational or a sympy inequality describing
        the input rule for which discipline is forming an opinion
    discip : Dictionary
        Contains all of the information relevant to the discipline
    passfail : Dictionary
        Predicted passing or failing amounts for each design space of
        discipline considering a particular rule set
    passfail_std : Dictionary
        Standard deviations associated with categorized passing or failing
        amounts
    bez_point : Dictionary
        x and y coordinates of control points of quadratic Bezier curve

    Returns
    -------
    opinion : Float
        A number between 0.0 and 1.0 where a small number matches up with an
        unfavorable opinion of the rule while a large number matches up with a
        favorable opinion of the rule
    """
    
    # Metric 1: Am I get ridding of clearly infeasible space?
    infeas_space = analyzeInfeasibility(passfail['leftover'], 
                                        passfail_std['leftover'])
    
    # Metric 2: Am I maintaining feasible space for this space reduction?
    feas_space = analyzeFeasibility(passfail['reduced'], 
                                    passfail_std['reduced'],
                                    passfail['non_reduced'], 
                                    passfail_std['non_reduced'])
    
    # Use quadratic Bezier curve to determine weight of second metric
    weight2 = bezierPoint(infeas_space, **bez_point)
    
    # Use weight of second metric to determine weight of first metric
    weight1 = 1 - weight2
    
    # Calculate weighted opinion
    opinion = weight1*infeas_space + weight2*feas_space
    
    # Return properly weighted opinion
    return opinion


"""
CLASS
"""
class mergeConstraints:
    
    def __init__(self, rules_new, Discips, gpr_params, bez_point):
        """
        Parameters
        ----------
        rules_new : List
            Contains sympy relationals and/or inequalities for rules that only
            consist of one argument
        Discips : List of dictionaries
            Contains dictionaries with all of the information relevant to each
            discipline
        gpr_params : Dictionary
            Additional keyword arguments for GPR model configuration. Common 
            parameters include 'length_scale_bounds' for the RBF kernel
            (default: (1e-2, 1e3)) and 'alpha' for GaussianProcessRegressor
            (default: 0.00001). These parameters are used to control various
            aspects of the GPR model, such as kernel properties and
            regularization
        bez_point : Dictionary
            x and y coordinates of control points of quadratic Bezier curve
        """
        self.rn = rules_new
        self.D = Discips
        self.gpr_params = gpr_params
        self.bez_point = bez_point
        return
    
    
    def formOpinion(self):
        """
        Description
        -----------
        Has each discipline form an opinion for a proposed rule.  A value of
        0.0 means the discipline is not in favor of the rule at all.  A value
        of 1.0 means the discipline is totally in favor of the rule.  A value
        of nan means the discipline is not directly impacted by the rule.
        
        Parameters
        ----------
        None.

        Returns
        -------
        opinions : Dictionary
            Each key in the dictionary corresponds with a rule set being
            proposed, and each value is a numpy array keeping track of the
            opinion that each discipline has of the particular rule
        passfail : Dictionary
            Predicted passing or failure amounts for the non-reduced, reduced,
            and leftover design spaces of each discipline for each rule set
        passfail_std : Dictionary
            Standard deviations associated with the predicted passing or
            failure amounts
        """
        
        # Gather all of the possible rule combinations
        rule_combos = []
        for r in range(1, len(self.rn) + 1):
            for combo in itertools.combinations(self.rn, r):
                rule_combos.append(combo)
        
        # Initialize dictionaries with a list of numpy arrays for each rule
        opinions = {rule: np.ones(len(self.D)) for rule in self.rn}
        passfail = {rule: [None for _ in self.D] for rule in rule_combos}
        passfail_std = {rule: [None for _ in self.D] for rule in rule_combos}
        
        # Loop through each discipline
        for i, discip in enumerate(self.D):
            
            # Get perceptions of feasibility in the non-reduced design space
            pf_mean, pf_std = getPerceptions(discip, self.gpr_params)
            
            # MOVE ABOVE STATEMENT IN ITS OWN FOR LOOP AND BELOW IN ITS OWN FOR
            # LOOP SO THAT IN THE MIDDLE, I LEAVE MYSELF THE OPTION TO DO AN MOGP
            # BEFORE ACTUALLY MAKING THE PREDICTIONS
            
            # Loop through each new rule combination - rule is a tuple here!
            for j, rule in enumerate(rule_combos):
                
                # Get predictions for different design spaces of the rule
                passfail[rule][i], passfail_std[rule][i] = \
                    getPredictions(discip, rule, pf_mean, pf_std)
                
                # Do not form opinion for rule combos, only individiual rules
                if len(rule) > 1: continue
                
                # Get free variables of the rule
                rule_vars = rule[0].free_symbols
                
                # Assign nan if discipline is not directly affected by rule
                if rule_vars <= set(discip['ins']): pass
                else: 
                    opinions[rule[0]][i] = np.nan
                    continue
                
                # Get opinion of discipline directly affected by rule
                opinions[rule[0]][i] = getOpinion(rule[0], discip, 
                                                  passfail[rule][i], 
                                                  passfail_std[rule][i], 
                                                  self.bez_point)
                
        # Display formed opinions
        print("Opinions: " + str(opinions))
                
        # Return the opinions of each rule and passfail data
        return opinions, passfail, passfail_std
    
    
    def domDecision(self, opinions, irules_discip, passfail, passfail_std):
        """
        Description
        -----------
        Determines if any discipline has the grounds to throw out a rule being
        proposed.  Dominance is naturally included in every rule proposal as
        each discipline is given veto power.  Vetoing is much easier early on
        but becomes more difficult later.
        
        Parameters
        ----------
        opinions : Dictionary
            Each key in the dictionary corresponds with a rule being proposed,
            and each value is a numpy array keeping track of the opinion that
            each discipline has of the particular rule set
        irules_discip : List of integers
            Index of the discipline proposing a particular rule that coincides
            with the input rule list.
        passfail : Dictionary
            Predicted passing or failure amounts for the non-reduced, reduced,
            and leftover design spaces of each discipline for each rule set
        passfail_std : Dictionary
            Standard deviations associated with the predicted passing or
            failure amounts
        
        Returns
        -------
        rules_new : List
            Contains updated sympy Or relationals and/or inequalities for rules
            after enduring merging process.
        passfail : Dictionary
            Predicted passing or failure amounts for the non-reduced, reduced,
            and leftover design spaces of each discipline of the new rule list
        passfail_std : Dictionary
            Standard deviations associated with the predicted passing or
            failure amounts of the new rule list
        """
        
        # Make a set containing indices of rules to throw out
        rules_delete = set()
        
        # Loop through each new rule being proposed
        for i, rule in enumerate(self.rn):
            
            # Initialize an empty set for gathering failure criteria
            fail_crit = set()
            
            # Loop through each discipline
            for j, discip in enumerate(self.D):
                
                # Continue to next discipline if it has no opinion on rule
                if np.isnan(opinions[rule][j]): continue
                
                # Add discipline's failure criterion to failure critieria set
                fail_crit.add(discip['part_params']['fail_crit'][0])
            
            # Loop through each discipline's opinion
            for j, discip in enumerate(opinions[rule]):
                
                # Determine threshold for throwing out the rule
                ### Opinion of the discipline proposing the rule minus the max
                ### fail criterion value for all of the disciplines involved
                threshold = opinions[rule][irules_discip[i]] - max(fail_crit)
                
                # If discipline is proposing rule, continue to next discipline
                if j == irules_discip[i]: continue
                
                # If discipline has no opinion, continue to next discipline
                if np.isnan(opinions[rule][j]): continue
                
                # Check if discipline's opinion warrants throwing the rule out
                if opinions[rule][j] < threshold:
                    
                    # Add index of rule to the rule deletion list
                    rules_delete.add(i)
                    
                    # Break the discipline loop and proceed to next rule
                    break
                    
        # Remove passfail data including vetoed rule(s)
        keys_to_remove = []
        for key in passfail.keys():
            if any(self.rn[i] in key for i in rules_delete):
                keys_to_remove.append(key)
        for key in keys_to_remove:
            del passfail[key]
            del passfail_std[key]
        
        # Remove vetoed rules from the input rule list
        self.rn = [item for idx, item in enumerate(self.rn) \
                   if idx not in rules_delete]
        
        # Return updated rule list and passfail data
        return self.rn, passfail, passfail_std
    
    