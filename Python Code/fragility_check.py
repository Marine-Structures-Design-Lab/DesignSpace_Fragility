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
import itertools
import matplotlib.pyplot as plt
import statsmodels.api as sm

"""
FUNCTIONS
"""
def kl_divergence(p, q, epsilon=1e-10):
    """
    Compute KL divergence of two distributions.
    
    Parameters:
    - p, q: The two distributions. They should be on the same grid.
    - epsilon: A small value to ensure we don't get log(0).
    
    Returns:
    - KL divergence between p and q.
    """

    # Ensure the distributions are normalized
    p /= p.sum()
    q /= q.sum()

    # Add epsilon to avoid log(0)
    p = p + epsilon
    q = q + epsilon

    return np.sum(p * np.log(p / q))






"""
CLASS
"""
class checkFragility:
    
    def __init__(self, Discips, irules_new):
        self.D = Discips
        self.ir = irules_new
        return
    
    
    def createDataSets(self):
        
        # Initialize list of empty dictionaries for data
        all_data = [{} for _ in self.D]
        
        # Loop through each discipline
        for i in range(0, len(self.D)):
            
            # Loop over all possible input variable combination lengths
            for j in range(1, len(self.D[i]['ins'])+1):
                
                # Generate combinations
                for combo in itertools.combinations(self.D[i]['ins'], j):
                    
                    # Gather the indices of the variables in the combo
                    indices = [self.D[i]['ins'].index(var) for var in combo]
                    indices = tuple(indices)
                    
                    # Collect eliminated data
                    elim_data = self.D[i].get('eliminated', {})
                    etested_ins = elim_data.get('tested_ins', np.empty((0, j)))
                    etested_ins = etested_ins[:, indices]
                    ef_amount = elim_data.get('Fail_Amount', np.array([]))
                    ef_amount = np.reshape(ef_amount, (-1, 1))
                    elim_data = np.hstack((etested_ins, ef_amount))
                    
                    # Collect non-eliminated data
                    tested_ins = self.D[i].get('tested_ins', np.empty((0, j)))
                    tested_ins = tested_ins[:, indices]
                    f_amount = self.D[i].get('Fail_Amount', np.array([]))
                    f_amount = np.reshape(f_amount, (-1, 1))
                    nonelim_data = np.hstack((tested_ins, f_amount))
                    
                    # Add eliminated and non-eliminated data together
                    all_data[i][combo] = np.vstack((elim_data, nonelim_data))
        
        # Return the eliminated and non-eliminated combined data sets
        return all_data
    
    
    # (SHOULD BE ABLE TO COMEBACK TO THIS AND MAKE CODE LESS REPETITIVE)
    def calcKDEs(self, all_data, KLgap):
        
        # Initialize empty lists
        KDEs = [{} for _ in range(len(self.D))]
        joint_KDEs = [[] for _ in range(len(self.D))]
        
        # Loop through each discipline
        for i in range(0, len(self.D)):
            
            # Determine the number of dimensions for joint KDE
            num_dimensions = len(max(all_data[i], key=lambda k: len(k))) + 1
            
            # Loop through each variable combination
            for combo in all_data[i]:
                
                # Skip combo if the tuple is not a single input variable
                if len(combo) > 1:
                    continue
                
                # Add combo to KDE dictionaries if it does not already exist
                KDEs[i].setdefault(combo, [])
                
                # Establish minimum number of data points for KDE development
                # (MIGHT GET A WARNING HERE IF I HAVE TOO LITTLE EXPLORED DATA)
                if len(KDEs[i][combo]) == 0: min_data = num_dimensions + 1
                else: min_data = len(KDEs[i][combo])*KLgap + num_dimensions + 1
                
                # Loop through data for KDE development
                for j in range(min_data, all_data[i][combo].shape[0], KLgap):
                    
                    # Gather data for particular combination
                    combo_data = all_data[i][combo][0:j, 0:-1]
                    
                    # Perform univariate KDE (free to adjust these!)
                    bandwidth_univariate = 'scott'
                    kernel_univariate = 'gau'
                    kde = sm.nonparametric.KDEUnivariate(combo_data)
                    kde.fit(bw=bandwidth_univariate, kernel=kernel_univariate)
                    
                    # Append KDE to the combo's list
                    KDEs[i][combo].append(kde)
            
            # Establish minimum number of data points for KDE development
            if len(joint_KDEs[i]) == 0: min_data = min_data = num_dimensions + 1
            else: min_data = len(joint_KDEs[i])*KLgap + num_dimensions + 1
            
            # Loop through data for KDE development
            for j in range(min_data, all_data[i][combo].shape[0], KLgap):
                
                # Gather data for joint combination
                joint_data = all_data[i][max(all_data[i], key=lambda k: len(k))][0:j, :]
                
                # Perform multivariate KDE (free to adjust these!)
                var_type_string = 'c' * num_dimensions
                bandwidth_multivariate = 'normal_reference'
                kde = sm.nonparametric.KDEMultivariate(data=joint_data, var_type=var_type_string, bw=bandwidth_multivariate)
                
                # Append KDE to the joint KDE's list
                joint_KDEs[i].append(kde)
            
        # Return the univariate and multivariate KDEs
        return KDEs, joint_KDEs
    
    
    
    # NEED TO ADJUST THESE TWO METHODS TO ONLY GO THROUGH THEIR LOOPS IF DATA HASN'T
    # LED TO AN EVALUATION ALREADY SIMILARLY TO HOW i DO IN THE ABOVE METHOD
    
    ### ALSO DO I WANT ANY VISUALIZATION METHODS????
    
    
    def evalBayes(self, KDEs, joint_KDEs):
        
        # Initialize empty lists
        posterior_KDEs = [[] for _ in range(len(self.D))]
        
        # Specify number of points in each dimension of evaluation grids
        # (Free to adjust this!)
        grid_res = 10
        
        # Loop through each discipline
        for i in range(0, len(self.D)):
            
            # Determine the number of dimensions of the joint KDEs
            num_dimensions = np.array(joint_KDEs[i][0].data).shape[1]
            
            # Create the range lists
            # (MAY WANT TO ADJUST THE RANGE OF FAILURE AMOUNT TO BE 0 TO MAX+0.5!)
            ranges = [np.linspace(0, 1, grid_res) for _ in range(num_dimensions)]
            
            # Loop through each KDE
            for j, joint_kde in enumerate(joint_KDEs[i]):
                
                # Create an evaluation grid
                grid = np.meshgrid(*ranges)
                
                # Convert grid points
                grid_points = np.vstack([g.ravel() for g in grid]).T
                
                # Evaluate the joint KDE P(A, B)
                joint_values = joint_kde.pdf(grid_points)
                
                # Evaluate the marginal KDEs P(B)
                marginal_values = np.prod([kde_list[j].evaluate(grid_points[:, ind]) for ind, kde_list in enumerate(KDEs[i].values())], axis=0)
                
                # Calculate the posterior P(A|B)
                posterior_values = joint_values / marginal_values
                
                # Store the posterior values
                posterior_KDEs[i].append(posterior_values.reshape(*[grid_res]*num_dimensions))
                
        # Return the posterior KDEs
        return posterior_KDEs
    
    
    def computeKL(self, posterior_KDEs):
        """
        Compute KL divergence for each successive posterior distribution.
        
        Parameters:
        - posterior_KDEs: List of posterior KDEs.
        
        Returns:
        - List of KL divergences.
        """
        kl_divs = []
        
        # Loop through each discipline
        for post_kdes in posterior_KDEs:
            discipline_kl_divs = []
            for i in range(len(post_kdes) - 1):
                div = kl_divergence(post_kdes[i], post_kdes[i + 1])
                discipline_kl_divs.append(div)
            kl_divs.append(discipline_kl_divs)
        
        return kl_divs
    





    
    
    
    
    
    
    # Return a true or false boolean value if fragile or not
    def basicCheck(self):
        
        fragile = False
        
        return fragile
