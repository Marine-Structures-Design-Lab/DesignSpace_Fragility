"""
SUMMARY:
First merges the rule(s) being proposed by each discipline such that there are
no contradictions by removing any rules apart of a contradiction.  Dominance
will be saved for consideration in the fragility framework.  There is also
potential for adding a method that removes any redundancies in the new rules
being proposed or possibly in all of the rules up to this point if the Input
Rules list is passed as another argument.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from point_sorter import sortPoints
from windfall_regret import sharedIndices
from sklearn.gaussian_process.kernels import RBF
from sklearn.gaussian_process import GaussianProcessRegressor
from scipy.stats import norm
from scipy.optimize import fsolve
import numpy as np
import sympy as sp
import copy

"""
TERTIARY FUNCTIONS
"""
def trainData(discip):
    
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


def initializeFit(discip, x_train, y_train):
    
    # Initialize Gaussian kernel
    kernel = 1.0 * RBF(length_scale=np.ones(len(discip['ins'])), \
                       length_scale_bounds=(1e-2, 1e3))
    
    # Initialize Gaussian process regressor (GPR)
    gpr_model = GaussianProcessRegressor(kernel=kernel, alpha=0.00001)
    
    # Fit GPR with training data
    gpr_model.fit(x_train, y_train)
    
    # Return trained GPR
    return gpr_model


def predictData(discip, gpr, diction):
    
    # Test GPR at each point remaining of non-reduced matrix
    means, stddevs = gpr.predict(discip['space_remaining'], return_std=True)
    
    # Initialize dictionaries
    passfail = {}
    passfail_std = {}
    
    # Loop through each list of indices in dictionary
    for key in diction:
        
        # Assign predicted data to proper dictionary key
        passfail[key] = means[diction[key]]
        passfail_std[key] = stddevs[diction[key]]
        
    # Return predicted passing and failing dictionaries with newest tests
    return passfail, passfail_std


def analyzeInfeasibility(predictions, std_devs):
    total_above_zero = 0

    for pred, std_dev in zip(predictions, std_devs):
        lower_bound = pred - 3 * std_dev
        upper_bound = pred + 3 * std_dev

        if upper_bound <= 0:
            # Entire interval is below zero, so decimal above zero is 0
            decimal_above_zero = 0
        elif lower_bound >= 0:
            # Entire interval is above zero, so decimal above zero is 1
            decimal_above_zero = 1
        else:
            # Interval crosses zero, calculate the decimal part above zero
            decimal_above_zero = (upper_bound - 0) / (upper_bound - lower_bound)

        total_above_zero += decimal_above_zero

    # Return 0 if total_above_zero is zero, else calculate the average
    return 0 if total_above_zero == 0 else (1 - (total_above_zero / len(predictions)))


def analyzeFeasibility(means1, std_devs1, means2, std_devs2):

    total_above_zero_1 = 0
    total_above_zero_2 = 0

    # Calculating for the first set
    for mean, std_dev in zip(means1, std_devs1):
        cdf_at_zero = norm.cdf(0, loc=mean, scale=std_dev)
        decimal_above_zero = 1 - cdf_at_zero
        total_above_zero_1 += decimal_above_zero

    # Calculating for the second set
    for mean, std_dev in zip(means2, std_devs2):
        cdf_at_zero = norm.cdf(0, loc=mean, scale=std_dev)
        decimal_above_zero = 1 - cdf_at_zero
        total_above_zero_2 += decimal_above_zero

    # Calculating the percentage of the first set relative to the second set
    return total_above_zero_1 / total_above_zero_2 if total_above_zero_2 != 0 else 0


def bezier_point(m1):
    
    # Control points
    P0 = (0.0, 1.0)
    P1 = (0.5, 0.8)
    P2 = (1.0, 0.0)

    # Define the x-coordinate of the Bezier curve
    def bezier_x(t):
        return (1 - t)**2 * P0[0] + 2 * (1 - t) * t * P1[0] + t**2 * P2[0] - m1

    # Solve for t where x(t) = m1
    t_solution = fsolve(bezier_x, 0.5)[0]  # Initial guess is 0.5

    # Ensure t is in the range [0, 1]
    if not 0 <= t_solution <= 1:
        return None

    # Calculate the y-coordinate at the solved t
    y = (1 - t_solution)**2 * P0[1] + 2 * (1 - t_solution) * t_solution * P1[1] + t_solution**2 * P2[1]

    return y



"""
SECONDARY FUNCTIONS
"""
# Develop a strategy for forming an opinion!!!
def getOpinion(rule, discip):
    
    # Make a copy of the discipline that takes input rule into account
    d_copy = copy.deepcopy(discip)
    d_copy = sortPoints([d_copy], [rule])
    
    # Find different index lists based on rule
    all_indices, indices_in_both, indices_not_in_B = \
        sharedIndices(discip['space_remaining'], d_copy[0]['space_remaining'])
    
    # Add each list to a different dictionary key
    diction = {"non_reduced": all_indices, 
               "reduced": indices_in_both, 
               "leftover": indices_not_in_B}
    
    # Initialize data for training a GPR
    x_train, y_train = trainData(discip)
    
    # Train GPR - maybe come back and introduce noise later
    gpr = initializeFit(discip, x_train, y_train)
    
    # Predict GPR at points in various space remaining indices
    passfail, passfail_std = predictData(discip, gpr, diction)
    
    # Metric 1: Am I get ridding of clearly infeasible space?
    infeas_space = analyzeInfeasibility(passfail['leftover'], passfail_std['leftover'])
    
    # Metric 2: Am I maintaining feasible space for this space reduction?
    feas_space = analyzeFeasibility(passfail['reduced'], passfail_std['reduced'],
                                    passfail['non_reduced'], passfail_std['non_reduced'])
    
    # Quadratic Bezier curve to determine weight of second metric
    weight2 = bezier_point(infeas_space)
    
    # Determine weight of first metric
    weight1 = 1 - weight2
    
    # Return properly weighted opinion from metrics
    return weight1*infeas_space + weight2*feas_space






"""
CLASS
"""
class mergeConstraints:
    
    def __init__(self, rules_new, Discips):
        """
        Parameters
        ----------
        rules_new : List
            Contains sympy Or relationals and/or inequalities for rules that
            only consist of one argument
        """
        self.rn = rules_new
        self.D = Discips
        return
    
    
    def removeContradiction(self):
        """
        Description
        -----------
        Considers the independent rule (consisting of a single inequality or a
        sympy Or relational containing multiple inequalities) being proposed by
        one or more disciplines and merges them such that from the top-level,
        the rule(s) do not contradict each other
        
        Parameters
        ----------
        None.

        Returns
        -------
        noncon_rules : List
            Contains sympy Or relationals and/or inequalities for rules that
            only consist of one argument without any contradictions
        """
        
        # Initialize a noncontradictory rule list
        noncon_rules = []
        
        # Loop through each new rule
        for i in range(0,len(self.rn)):
            
            # Set a boolean variable tracking contradiction to False
            is_contra = False
            
            # Loop through each new rule again
            for j in range(0,len(self.rn)):
                
                # Check that rules being checked for contradiction are not same
                if i != j:
                    
                    # Place rules inside a sympy And relational
                    contra = sp.And(self.rn[j], self.rn[i])
                    
                    # Check if simplified And relational evaluates to False
                    if sp.simplify(contra) == False:
                        
                        # Change contradiction variable to true and break loop
                        is_contra = True
                        break
            
            # Check if contradiction variable is still false
            if not is_contra:
                
                # Append the rule to the noncontradictory rule list
                noncon_rules.append(self.rn[i])
        
        # Return the noncontradictory rule list
        return noncon_rules
    
    
    # No 'Or' rule redundancies
    # def removeRedundancy(self):
    #     # Do I only want to remove redundancies in the new rules?...or do I
    #     # want to do the entire list of rules established thus far?
        
    #     return
    
    
    
    
    
    
    # Use GPR to determine infeasibility of designs in the space to be removed
    # Have each discipline form an opinion for the proposed space reduction
    def formOpinion(self):
        
        # Initialize a nested numpy array for opinions of each rule
        opinions = [np.ones(len(self.D)) for _ in self.rn]
        
        # Loop through each new rule being proposed
        for i, rule in enumerate(self.rn):
            
            # Loop through each discipline
            for j, discip in enumerate(self.D):
                
                # Get free variables of the rule
                rule_vars = rule.free_symbols
                
                # Assign nan if discipline is not directly affected by rule
                if rule_vars <= set(discip['ins']): pass
                else: 
                    opinions[i][j] = np.nan
                    continue
                
                # Get opinion of discipline directly affected by rule
                opinions[i][j] = getOpinion(rule, discip)
                
        print(opinions)
                
        # Return the opinions of each rule from each discipline
        return opinions
    
    
    # Determine if any discipline has the grounds to throw out the rule being proposed
    ### Dominance is naturally included in every rule proposal
    ### Each discipline is given the opportunity for veto power
    ### Make veto power easy early on but harder later
    def domDecision(self, rule_opinions, irules_discip):
        
        # Make a set containing indices of rules to throw out
        rules_delete = set()
        
        # Loop through each new rule being proposed
        for i, rule in enumerate(self.rn):
            
            # Determine max fail_criteria value of disciplines involved
            # Initialize an empty set for gathering failure criteria
            fail_crit = set()
            
            # Loop through each discipline
            for j, discip in enumerate(self.D):
                
                # Continue to next discipline if it has no opinion on rule
                if np.isnan(rule_opinions[i][j]): continue
                
                # Add discipline's failure criterion to failure critieria set
                fail_crit.add(discip['part_params']['fail_crit'])
            
            # Loop through each discipline's opinion
            for j, discip in enumerate(rule_opinions[i]):
                
                # Determine threshold for throwing out the rule
                ### Opinion of the discipline proposing the rule minus the max
                ### fail criterion value for all of the disciplines involved
                threshold = rule_opinions[i][irules_discip[i]] - max(fail_crit)
                
                # If discipline is the one proposing the rule, continue to next discipline
                if j == irules_discip[i]: continue
                
                # If discipline has no opinion, continue to next discipline
                if np.isnan(rule_opinions[i][j]): continue
                
                # Check if discipline's opinion warrants throwing the rule out
                if rule_opinions[i][j] < threshold:
                    
                    # Add index of rule to the rule deletion list
                    rules_delete.add(i)
                    
                    # Break the discipline loop and proceed to next rule
                    break
                    
        # Remove vetoed rules from the input rule list
        self.rn = [item for idx, item in enumerate(self.rn) if idx not in rules_delete]
        
        # Return updated rule list which is potentially condensed
        return self.rn
    
    
    
    
    
    

    



















    
# def remove_redundancies(rules):
#     non_redundant_rules = []
#     for i in range(len(rules)):
#         is_redundant = False
#         for j in range(len(rules)):
#             if i != j:
#                 implication = sp.Implies(rules[j], rules[i])
#                 if sp.simplify(implication) == True:
#                     is_redundant = True
#                     break
#         if not is_redundant:
#             non_redundant_rules.append(rules[i])
#     return non_redundant_rules   
    
    
    
    
    