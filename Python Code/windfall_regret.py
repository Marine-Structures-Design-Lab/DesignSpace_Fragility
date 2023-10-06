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
import copy
import scipy.stats as stats
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from point_sorter import sortPoints


"""
FUNCTIONS
"""
def sharedIndices(A, B):
    
    # Convert rows to tuples for set operations
    A_rows = set(map(tuple, A))
    B_rows = set(map(tuple, B))
    
    # Find rows in A that are not in B
    diff_rows = A_rows - B_rows
    
    # Get indices of A for rows that are not in B
    indices_not_in_B = [i for i, row in enumerate(A) if tuple(row) in diff_rows]
    
    # Get indices of A for rows that are in both A and B
    indices_in_both = [i for i, row in enumerate(A) if tuple(row) not in diff_rows]
    
    # Get all indices of A
    all_indices = list(range(len(A)))
    
    return all_indices, indices_in_both, indices_not_in_B


"""
CLASS
"""
class windfallRegret:
    
    def __init__(self, Discips, irules_new, passfail, passfail_std, windreg, \
                 running_windfall, running_regret, net_windreg, risk_or_potential):
        
        # Initialize instance variables for disciplines and new rules
        self.D = Discips
        self.ir = irules_new
        
        # Initialize instance variables for windfall-regret data tracking
        self.pf = passfail
        self.pf_std = passfail_std
        self.windreg = windreg
        self.run_wind = running_windfall
        self.run_reg = running_regret
        self.net_wr = net_windreg
        self.risk_or_pot = risk_or_potential
        
        # Initialize a copy of the discipline mirroring new input rule(s)
        D_red = copy.deepcopy(Discips)
        D_red = sortPoints(D_red, irules_new)
        
        # Initialize list for tracking indices
        self.i_lists = []
        
        # Loop through each discipline
        for i in range(0, len(self.D)):
            
            # Find different index lists based on current space reduction
            all_indices, indices_in_both, indices_not_in_B = \
                sharedIndices(Discips[i]['space_remaining'], D_red[i]['space_remaining'])
            
            # Add each list to a different dictionary key
            diction = {"non_reduced": all_indices, "reduced": indices_in_both, "leftover": indices_not_in_B}
            
            # Append dictionary to the index tracking list
            self.i_lists.append(diction)
            
        # Nothing to return
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
    
    
    # Can I figure out a way to plot this or the above method?
    def predictData(self, gpr):
        
        # Loop through each discipline's index lists
        for i, lists in enumerate(self.i_lists):
            
            # Test GPR at each point remaining of non-reduced matrix
            means, stddevs = gpr[i].predict(self.D[i]['space_remaining'], return_std=True)
            
            # Loop through each list of indices of discipline
            for key in lists:
                
                # Append arrays to empty lists
                self.pf[i][key].append(means[lists[key]])
                self.pf_std[i][key].append(stddevs[lists[key]])
                
        # Return predicted passing and failing dictionaries with newest tests
        return self.pf, self.pf_std
    
    
    # Need to adjust tp_actual in each discipline because there may be different numbers of dimensions
    # Figure out how to do this for each input variable combination rather than only space as a whole
    def calcWindRegret(self, tp_actual):
            
        # Loop through each discipline's pass/fail dictionary
        for ind1, d in enumerate(self.pf):
            
            # Initialize empty dictionaries
            windreg = {}
            run_wind = {}
            run_reg = {}
            net_wr = {}
            
            # Loop through each item of dictionary
            for key, value in d.items():
                
                # Initalize values for windfall and regret tracking
                windreg[key] = np.empty_like(value[-1])
                run_wind[key] = 0.0
                run_reg[key] = 0.0
                
            # Loop through each predicted value of the non-reduced matrix
            for ind2, value in enumerate(d['non_reduced'][-1]):
                
                # Convert prediction to a probability of the opposite event
                prob_feas = 1.0 - stats.norm.cdf(abs(value)/self.pf_std[ind1]['non_reduced'][-1][ind2])
                
                # Check if point is in both non-reduced and reduced matrices
                if ind2 in self.i_lists[ind1]["reduced"]:
                    
                    # Check if point is predicted infeasible (windfall chance)
                    if value < 0:
                        
                        # Add pos. probability to the proper dictionary arrays
                        windreg['non_reduced'][ind2] = prob_feas
                        windreg['reduced'][self.i_lists[ind1]["reduced"].index(ind2)] = prob_feas
                        
                        # Add to proper running windfall count
                        run_wind['non_reduced'] += prob_feas
                        run_wind['reduced'] += prob_feas
                        
                    # Do below if point is predicted feasible (regret chance)
                    else:
                        
                        # Add neg. probability to the proper dictionary arrays
                        windreg['non_reduced'][ind2] = -prob_feas
                        windreg['reduced'][self.i_lists[ind1]["reduced"].index(ind2)] = -prob_feas
                        
                        # Add to proper running regret count
                        run_reg['non_reduced'] += prob_feas
                        run_reg['reduced'] += prob_feas
                
                # Do below if point is not in both non-reduced and reduced matrices
                else:
                    
                    # Check if point is predicted infeasible (non-reduced: windfall chance, reduced: regret chance)
                    if value < 0:
                        
                        # Add pos. probability to the proper dictionary arrays (Should I do leftover or put these values in reduced?)
                        windreg['non_reduced'][ind2] = prob_feas
                        windreg['leftover'][self.i_lists[ind1]["leftover"].index(ind2)] = -prob_feas
                        
                        # Add to proper running windfall count (Do I want to use leftover key at all?)
                        run_wind['non_reduced'] += prob_feas
                        run_reg['reduced'] += prob_feas
                    
                    # Do below if point is predicted feasible (non-reduced: regret chance, reduced: windfall chance)
                    else:
                        
                        # Add neg. probability to the proper dictionary arrays
                        windreg['non_reduced'][ind2] = -prob_feas
                        windreg['leftover'][self.i_lists[ind1]["leftover"].index(ind2)] = prob_feas
                        
                        # Add to proper running windfall count
                        run_reg['non_reduced'] += prob_feas
                        run_wind['reduced'] += prob_feas
            
            # Loop through each item of dictionary
            for key, value in d.items():
                
                # Divide probabilistic sums by original number of points
                run_wind[key] = run_wind[key] / tp_actual
                run_reg[key] = run_reg[key] / tp_actual
                
                # Calculate difference between net windfall and regret
                net_wr[key] = run_wind[key] - run_reg[key]
                
                # Append matrices and values to proper list
                self.windreg[ind1][key].append(windreg[key])
                self.run_wind[ind1][key].append(run_wind[key])
                self.run_reg[ind1][key].append(run_reg[key])
                self.net_wr[ind1][key].append(net_wr[key])
                
                # Consider plotting net windfall-regret over time for each variable combination!
            
        # Return windfall and regret information
        return self.windreg, self.run_wind, self.run_reg, self.net_wr
    
    
    def quantRisk(self):
        
        # Loop through each discipline's risk or potential dictionary
        for i, d in enumerate(self.risk_or_pot):
            
            ########## Regret ##########
            # Calculate the "risk" value for the space reduction
            ### + value indicates added regret
            ### - value indicates reduced regret
            if self.run_reg[i]['non_reduced'][-1] == 0: self.run_reg[i]['non_reduced'][-1] += 1e-10
            risk = self.run_reg[i]['reduced'][-1]/self.run_reg[i]['non_reduced'][-1] - 1
            
            # Print the added risk results of the space reduction
            print(f"Discipline {i+1} would experience {round(risk, 2)} added regret.")
            
            # Append risk value to proper risk_or_potential key
            d["regret"].append(risk)
            
            ########## Windfall ##########
            # Calculate the "potential" value for the space reduction
            ### + value indicates added windfall
            ### - value indicates reduced windfall
            if self.run_wind[i]['non_reduced'][-1] == 0: self.run_wind[i]['non_reduced'][-1] += 1e-10
            windfall = self.run_wind[i]['reduced'][-1]/self.run_wind[i]['non_reduced'][-1] - 1
            
            # Print the reduced potential results of the space reduction
            print(f"Discipline {i+1} would experience {-round(windfall, 2)} reduced windfall.")
            
            # Append windfall value to proper risk_or_potential key
            d["windfall"].append(windfall)
            
            ########## Net Windfall-Regret ##########
            # Calculate the percent shift in net windfall-regret for the space reduction
            ### + means a shift towards more windfall influence
            ### - means a shift towards more regret influence
            ### Values less than 1 mean it remains primarily regret or windfall influenced
            ### Values greater than 1 can mean influence has flipped or have become way more ingrained in regret or windfall depending on "before" value
            if self.net_wr[i]['non_reduced'][-1] == 0: self.net_wr[i]['non_reduced'][-1] += 1e-10
            net = (self.net_wr[i]['reduced'][-1] - self.net_wr[i]['non_reduced'][-1])/abs(self.net_wr[i]['non_reduced'][-1])
            
            # Print the percent shift results of the space reduction
            print(f"Discipline {i+1} would experience {round(net, 2)} shift in net windfall-regret.")
            
            # Append net value to proper risk_or_potential key
            d["net"].append(net)
        
        # Return updated risk_or_potential dictionary
        return self.risk_or_pot
    
    
    # Surfaces are temporary and may need adjustment to fit other SBD problems
    def plotWindRegret(self, tp_actual):
        
        # Loop through each discipline's windfall-regret values
        for ind1, d in enumerate(self.windreg):
            
            # Print percent of space that would remain in discipline
            print(f"Discipline {ind1+1} would go from "
                  f"{round((d['non_reduced'][-1].shape[0]/tp_actual)*100, 2)}% to "
                  f"{round((d['reduced'][-1].shape[0]/tp_actual)*100, 2)}%"
                  f" of its original design space remaining!")
            
            # Loop through each item of dictionary
            for key, value in d.items():
                
                # Continue if array is empty
                if value[-1].shape[0] == 0:
                    continue
                
                # Initialize an empty list for storing numpy arrays
                l = []
                
                # Surface plot
                j = np.linspace(0, 1, 4000)
                k = np.linspace(0, 1, 4000)
                j, k = np.meshgrid(j, k)
                
                if ind1 == 0:
                    l.append(0.8*j**2 + 2*k**2 - 0.0)
                    l.append(0.8*j**2 + 2*k**2 - 0.4)
                    l.append(0.8*j**2 + 2*k**2 - 1.2)
                    l.append(0.8*j**2 + 2*k**2 - 1.6)
                elif ind1 == 1:
                    l.append((12.5*j**3-6.25*j**2+0.5)/1.25)
                    l.append((12.5*j**3-6.25*j**2+0.7)/1.25)
                    l.append(-k**3+np.sqrt(0.2))
                    l.append(-k**3+np.sqrt(0.5))
                else:
                    l.append((2*j+0.2*np.sin(25*k)-0.0)**5)
                    l.append((2*j+0.2*np.sin(25*k)-0.5)**5)
                    l.append((np.cos(3*j)+0.8)**3)
                    l.append((np.cos(3*j)+1.6)**3)
                
                # Replace out-of-bounds z_values with np.nan
                l = [np.where((z >= 0) & (z <= 1), z, np.nan) for z in l]
                
                # Initialize plot
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                
                # Initialize colors for plots
                colors = ['teal', 'teal', 'magenta', 'magenta']
                
                # Plot every surface
                for m in range(0,len(l)):
                    if ind1 < 2:
                        ax.plot_surface(j, k, l[m], color=colors[m], alpha=0.1, rstride=100, cstride=100)
                    else:
                        ax.plot_surface(l[m], j, k, color=colors[m], alpha=0.1, rstride=100, cstride=100)
                
                # Define the levels and discretize the windfall-regret data
                levels = np.linspace(-0.5, 0.5, 11)
                wr_discrete = (np.digitize(value[-1], bins=levels) - 6) / 10.0
                
                # When plotting space remaining data, use the discretized windfall values
                scatter = ax.scatter(self.D[ind1]['space_remaining'][self.i_lists[ind1][key], 0], \
                                     self.D[ind1]['space_remaining'][self.i_lists[ind1][key], 1], \
                                     self.D[ind1]['space_remaining'][self.i_lists[ind1][key], 2], \
                                     c=wr_discrete, s=10, cmap='RdBu', alpha=1.0, vmin=-0.5, vmax=0.5)
                
                # Adjust the colorbar to reflect the levels
                cbar = plt.colorbar(scatter, ax=ax, ticks=levels, boundaries=levels)
                cbar.set_label('Windfall-Regret Scale')
                
                # Edit the color bar
                tick_labels = [f"{round(level, 1)}" for level in levels]
                tick_labels[0] = f"{tick_labels[0]} (Regret)"
                tick_labels[-1] = f"{tick_labels[-1]} (Windfall)"
                cbar.ax.set_yticklabels(tick_labels)
                
                # Gather and plot passing and failing remaining tested input indices
                pass_ind = np.where(self.D[ind1]['pass?'])[0].tolist()
                fail_ind = np.where(np.array(self.D[ind1]['pass?']) == False)[0].tolist()
                ax.scatter(self.D[ind1]['tested_ins'][pass_ind,0], \
                           self.D[ind1]['tested_ins'][pass_ind,1], \
                           self.D[ind1]['tested_ins'][pass_ind,2], c='lightgreen', alpha=1)
                ax.scatter(self.D[ind1]['tested_ins'][fail_ind,0], \
                           self.D[ind1]['tested_ins'][fail_ind,1], \
                           self.D[ind1]['tested_ins'][fail_ind,2], c='red', alpha=1)
                
                # Gather and plot passing and failing eliminated tested input indices
                if 'eliminated' in self.D[ind1]:
                    pass_ind = np.where(self.D[ind1]['eliminated']['pass?'])[0].tolist()
                    fail_ind = np.where(np.array(self.D[ind1]['eliminated']['pass?']) == False)[0].tolist()
                    ax.scatter(self.D[ind1]['eliminated']['tested_ins'][pass_ind,0], \
                               self.D[ind1]['eliminated']['tested_ins'][pass_ind,1], \
                               self.D[ind1]['eliminated']['tested_ins'][pass_ind,2], c='lightgreen', alpha=1)
                    ax.scatter(self.D[ind1]['eliminated']['tested_ins'][fail_ind,0], \
                               self.D[ind1]['eliminated']['tested_ins'][fail_ind,1], \
                               self.D[ind1]['eliminated']['tested_ins'][fail_ind,2], c='red', alpha=1)
                
                # Set axis limits
                ax.set_xlim([0, 1])
                ax.set_ylim([0, 1])
                ax.set_zlim([0, 1])
                
                # Set labels and title
                ax.set_xlabel(self.D[ind1]['ins'][0])
                ax.set_ylabel(self.D[ind1]['ins'][1])
                ax.set_zlabel(self.D[ind1]['ins'][2])
                ax.set_title(f"Discipline {ind1+1} {key} input space")
                
                # Create proxy artists for the legend
                legend_elements = [Line2D([0], [0], marker='o', color='w', label='Feasible',
                                          markersize=10, markerfacecolor='lightgreen'),
                                    Line2D([0], [0], marker='o', color='w', label='Infeasible',
                                          markersize=10, markerfacecolor='red')]
    
                # Add the legend to your axis
                ax.legend(handles=legend_elements, loc='upper left')
                
                # Show plot
                plt.show()
            
        # Nothing to return as I am plotting information
        return
    
