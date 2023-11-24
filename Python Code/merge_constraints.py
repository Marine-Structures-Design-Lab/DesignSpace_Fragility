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




"""
SECONDARY FUNCTIONS
"""
# Develop a strategy for forming an opinion!!!
### Forming an opinion should only focus on the infeasibility of the space to be reduced
### Making a decision based on dominance needs to account for the space that would remain
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
    passfail, passfail_std = predictData(d_copy, gpr, diction)
    
    
    
    return 0.0






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
                
        # Return the opinions of each rule from each discipline
        return opinions
    
    
    # Do minimum merge if not ready for conflicts yet
    
    
    # Do dominance if ready for conflicts
    
    
    
    
    
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    # No dominance until at least 50% of spaces have been eliminated
    ### One option is to have the requests pop up with stats and I decide
    ### Or program decides with stats
    ### Stats: How many disciplines are requesting what vs. the other
    ### How each side would be affected by the other discipline's proposal
    
    
    ### Could call a getInput method here...but not have it be a uniform method
    ### Could also do this for the fragility or other methods that may need to
    ### search points further
    
    
    