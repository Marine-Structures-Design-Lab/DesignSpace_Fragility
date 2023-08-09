"""
SUMMARY:


CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV
from scipy.stats import entropy
from scipy.integrate import nquad
import numpy as np
import itertools
import matplotlib.pyplot as plt


def compute_kl(p_kde, q_kde, num_dimensions):
    """Compute KL divergence between two KDEs with specified number of dimensions."""
    
    # Create bounds for each dimension
    bounds = [(0, 1) for _ in range(num_dimensions)]
    
    def integrand(*args):
        x = np.array(args).reshape(1, -1)  # reshape to 2D array for score_samples
        p_x = np.exp(p_kde.score_samples(x))
        q_x = np.exp(q_kde.score_samples(x))
        return p_x * np.log(p_x / q_x)
    
    return nquad(integrand, bounds)[0]


def plot_2D_KDE(kde):
    # Create a grid to evaluate the KDE
    xx, yy = np.mgrid[0:1.01:0.01, 0:1.01:0.01]
    grid_points = np.c_[xx.ravel(), yy.ravel()]

    # Evaluate the KDE on the grid
    pdf = np.exp(kde.score_samples(grid_points[:, 0].reshape(-1, 1)))  # Use only the x values (input location values)
    pdf = pdf.reshape(xx.shape)

    # Plot
    plt.contourf(xx, yy, pdf, cmap='Blues')
    plt.colorbar()
    plt.xlabel("Input Location Value (x1)")
    plt.ylabel("Failure Amount")
    plt.title("Probability Distribution of Failure Amounts")
    plt.show()







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
    
    
    def klDivergence(self, all_data, KLgap):
        
        # Initialize empty lists for prior and posterior KDEs
        prior_KDEs = [{} for _ in range(len(self.D))]
        posterior_KDEs = [{} for _ in range(len(self.D))]
        
        # Initialize empty list for KL divergence values
        KL_values = [{} for _ in range(len(self.D))]
        
        # Loop through each discipline
        for i in range(0, len(all_data)):
            
            # Loop through each variable combination of discipline
            for combo in all_data[i]:
                
                # Break loop if not enough data for KDEs
                if all_data[i][combo].shape[0] - KLgap < 2:
                    break
                
                # Add combo to KDE dictionaries if it does not already exist
                prior_KDEs[i].setdefault(combo, [])
                posterior_KDEs[i].setdefault(combo, [])
                
                # Add combo to KL dictionaries if it does not already exist
                KL_values[i].setdefault(combo, [])
                
                # Establish starting index
                start_index = len(prior_KDEs[i][combo])
                
                # Initialize a counting variable
                count = 0
                
                # Loop through data for KDE development according to increment
                for j in range(2, all_data[i][combo].shape[0] - KLgap, KLgap):
                    
                    # Continue if KDE already calculated for data set
                    if count < start_index:
                        count += 1
                        continue
                    
                    # Gather prior and posterior data from all of the data
                    prior_data = all_data[i][combo][0:j, :]
                    posterior_data = all_data[i][combo][0:j+KLgap, :]
                    
                    # Determine cv's for KDE's (free to adjust conditionals)
                    prior_cv = 5 if prior_data.shape[0] >= 5 else prior_data.shape[0]
                    posterior_cv = 5 if posterior_data.shape[0] >= 5 else posterior_data.shape[0]
                    
                    # Set possible bandwidths for KDE (free to adjust)
                    params = {'bandwidth': np.linspace(0.01, 1, 50)}
                    
                    # Prior grid search and KDE development
                    grid = GridSearchCV(KernelDensity(kernel='gaussian'), params, cv=prior_cv)
                    grid.fit(prior_data[:,:-1], prior_data[:,-1])
                    prior_KDEs[i][combo].append(grid.best_estimator_)
                    
                    # Posterior grid search and KDE development
                    grid = GridSearchCV(KernelDensity(kernel='gaussian'), params, cv=posterior_cv)
                    grid.fit(posterior_data[:,:-1], posterior_data[:,-1])
                    posterior_KDEs[i][combo].append(grid.best_estimator_)
                    
                    # Determine the number of dimensions (excluding the target column)
                    num_dimensions = prior_data.shape[1] - 1
                    
                    # Compute KL Divergence from prior and posterior KDEs
                    #KL_values[i][combo].append(compute_kl(prior_KDEs[i][combo][-1], posterior_KDEs[i][combo][-1], num_dimensions))
                    #print("Computed KL-Divergence for " + str(combo) + " " + str(count+1) + " times!")
                    
                    
                    
                    
                    # Increase count by 1
                    count += 1
        
        # Return KL divergence values and KDEs
        return KL_values, prior_KDEs, posterior_KDEs


    def visualize_KDEs(self, prior_KDEs, posterior_KDEs):
        for discipline, variable_combos in enumerate(prior_KDEs):
            for combo, kdes in variable_combos.items():
                num_dimensions = len(combo)  # Simply find the length of the tuple to get dimensions
                
                if num_dimensions == 1:  # 1D data implies 2D KDE plot of x1 vs Failure Amount
                    for idx, kde in enumerate(kdes):
                        print(f"Visualizing Prior KDE for {combo} - {idx+1}")
                        plot_2D_KDE(kde)
                        # Similarly for the posterior KDE, if required.
                        print(f"Visualizing Posterior KDE for {combo} - {idx+1}")
                        plot_2D_KDE(posterior_KDEs[discipline][combo][idx])
    




    
    

    
    
    
    
    
    # Return a true or false boolean value if fragile or not
    def basicCheck(self):
        
        fragile = False
        
        return fragile
