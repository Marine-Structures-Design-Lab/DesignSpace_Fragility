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
    
    # Return the calculated KL divergence
    return np.sum(p * np.log(p / q))






"""
CLASS
"""
class checkFragility:
    
    def __init__(self, Discips, irules_new, KDE_data, joint_KDEs, KDEs):
        
        # Initialize disciplines and new rules
        self.D = Discips
        self.ir = irules_new
        
        # Loop through each discipline
        for i in range(0, len(self.D)):
            
            # Loop over all possible input variable combination lengths
            for j in range(1, len(self.D[i]['ins']) + 1):
                
                # Generate combinations
                for combo in itertools.combinations(self.D[i]['ins'], j):
                    
                    # Add combo to dictionary if it does not already exist
                    KDE_data[i].setdefault(combo, np.empty((0, j+1)))
                    joint_KDEs[i].setdefault(combo, [])
                    
                    # Check if currently only considering individual variable
                    if j == 1:
                        
                        # Add combo to dictionary if it does not already exist
                        KDEs[i].setdefault(combo, [])
                    
        
        # Initialize object variables for other inputs
        self.kde_d = KDE_data
        self.j_kde = joint_KDEs
        self.kde = KDEs
        
        return
    
    
    # Initialize KDE_data and other variables being returned in script file
    # to make sure I know the order that data was added and to avoid repetitive
    # KDE & KL divergence calculations!!!
    
    # ADJUST GRID SIZE AFTER I'VE DONE THIS!!!
    
    def createDataSets(self):
        
        # Loop through each discipline
        for i in range(0, len(self.kde_d)):
            
            # Loop over each variable combination
            for combo in self.kde_d[i]:
                
                # Check the size of the eliminated data
                if 'eliminated' in self.D[i]:
                    elim_size = self.D[i]['eliminated']['tested_ins'].shape[0]
                else:
                    elim_size = 0
                
                # Check the size of the non-eliminated data
                nonelim_size = self.D[i]['tested_ins'].shape[0]
                
                # Determine number of new points that have been explored
                num_points = nonelim_size - \
                    (self.kde_d[i][combo].shape[0] - elim_size)
                
                # Check if new points have been explored
                if num_points > 0:
                    
                    # Gather the indices of the variables in the combo
                    indices = [self.D[i]['ins'].index(var) for var in combo]
                    indices = tuple(indices)
                    
                    # Collect new non-eliminated data
                    tested_ins = self.D[i]['tested_ins'][-num_points:, indices]
                    f_amount = self.D[i]['Fail_Amount'][-num_points:]
                    f_amount = np.reshape(f_amount, (-1, 1))
                    nonelim_data = np.hstack((tested_ins, f_amount))
                    
                    # Add eliminated and non-eliminated data together
                    self.kde_d[i][combo] = \
                        np.vstack((self.kde_d[i][combo], nonelim_data))
        
        # Return the potentially updated KDE data set
        return self.kde_d
    
    
    def calcKDEs(self, KLgap):
        
        # Loop through each discipline
        for i in range(0, len(self.j_kde)):
            
            # Determine the maximum number of dimensions for joint KDE
            num_dimensions = len(max(self.kde_d[i], key=lambda k: len(k))) + 1
            
            # Loop through each variable combination in joint KDE
            for combo in self.j_kde[i]:
                
                # Establish minimum number of data points for KDE development
                # (MIGHT GET AN ERROR HERE IF I HAVE TOO LITTLE EXPLORED DATA)
                if len(self.j_kde[i][combo]) == 0: 
                    min_data = num_dimensions + 1
                else: 
                    min_data = \
                        len(self.j_kde[i][combo])*KLgap + num_dimensions + 1
                
                # Loop through data for KDE development
                for j in range(min_data, self.kde_d[i][combo].shape[0], KLgap):
                    
                    # Gather data for joint combination
                    joint_data = self.kde_d[i][combo][0:j, :]
                    
                    # Perform multivariate KDE (free to adjust these!)
                    var_type_string = 'c' * (len(combo) + 1)
                    bandwidth_multivariate = 'normal_reference'
                    kde = sm.nonparametric.KDEMultivariate(data=joint_data, \
                        var_type=var_type_string, bw=bandwidth_multivariate)
                    
                    # Append KDE to the joint KDE's list
                    self.j_kde[i][combo].append(kde)
                    
                    # Check if tuple only consists of a single input variable
                    if len(combo) == 1:
                        
                        # Gather data for particular combination
                        combo_data = self.kde_d[i][combo][0:j, 0:-1]
                        
                        # Perform univariate KDE (free to adjust these!)
                        bandwidth_univariate = 'scott'
                        kernel_univariate = 'gau'
                        kde = sm.nonparametric.KDEUnivariate(combo_data)
                        kde.fit(bw=bandwidth_univariate, \
                                kernel=kernel_univariate)
                        
                        # Append KDE to the KDE's list
                        self.kde[i][combo].append(kde)
                    
        # Return the univariate and multivariate KDEs
        return self.kde, self.j_kde
    
    
    def evalBayes(self):
        
        # Initialize empty lists
        posterior_KDEs = [{} for _ in range(len(self.D))]
        
        # Specify number of points in each dimension of evaluation grids
        # (Free to adjust this!)
        grid_res = 10
        
        # Loop through each discipline
        for i in range(0, len(self.D)):
            
            # Loop through each variable combination
            for combo in self.j_kde[i]:
                
                # Add combo to posterior KDE dictionaries
                posterior_KDEs[i].setdefault(combo, [])
                
                # Determine the number of dimensions of the joint KDE
                num_dimensions = np.array(self.j_kde[i][combo][0].data).shape[1]
                
                # Initialize an empty dictionary of marginal KDEs
                marg_kdes = {}
                
                # Gather the relevant individual KDEs
                for key in self.kde[i]:
                    if key[0] in combo:
                        marg_kdes[key] = self.kde[i][key]

                # Create the range lists
                # (MAY WANT TO ADJUST THE RANGE OF FAILURE AMOUNT TO BE 0 TO MAX+0.5!)
                ranges = [np.linspace(0, 1, grid_res) for _ in range(num_dimensions)]
                
                # Loop through each joint KDE
                for j, joint_kde in enumerate(self.j_kde[i][combo]):
                    
                    # Create an evaluation grid
                    grid = np.meshgrid(*ranges)
                    
                    # Convert grid points
                    grid_points = np.vstack([g.ravel() for g in grid]).T
                    
                    # Evaluate the joint KDE P(A, B)
                    joint_values = joint_kde.pdf(grid_points)
                    
                    # Evaluate the product of the relevant marginal KDEs
                    marginal_values = [kde_list[j].evaluate(grid_points[:, ind]) for ind, kde_list in enumerate(marg_kdes.values())]
                    marginal_values = np.prod(marginal_values, axis=0)
                    
                    # Calculate the posterior P(A|B)
                    posterior_values = joint_values / marginal_values
                    
                    # Store the posterior values
                    posterior_KDEs[i][combo].append(posterior_values.reshape(*[grid_res]*num_dimensions))
                
        # Return the posterior KDEs
        return posterior_KDEs
    
    
    def computeKL(self, posterior_KDEs):
        
        # Initialize empty lists
        KL_divs = [{} for _ in range(len(self.D))]
        
        # Loop through each discipline
        for i in range(0, len(self.D)):
            
            # Loop through each variable combination
            for combo in posterior_KDEs[i]:
                
                # Add combo to KL divergence dictionaries
                KL_divs[i].setdefault(combo, [])
                
                # Loop through each coinciding pair of posterior probabilities
                for j in range(0, len(posterior_KDEs[i][combo]) - 1):
                    
                    # Calculate KL divergence between consecutive probabilities
                    div = kl_divergence(posterior_KDEs[i][combo][j+1], posterior_KDEs[i][combo][j])
                    
                    # Append the KL divergence to the proper dictionary key
                    KL_divs[i][combo].append(div)
        
        # Return the KL divergences
        return KL_divs
    
    
    # Method to visualize KL divergences
    
    # Method to visualize KDEs
    
    # Return a true or false boolean value if fragile or not
    def basicCheck(self):
        
        fragile = False
        
        return fragile
