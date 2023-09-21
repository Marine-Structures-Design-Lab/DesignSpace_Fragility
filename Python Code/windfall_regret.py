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
CLASS
"""
class windfallRegret:
    
    def __init__(self, Discips, irules_new, passfail, passfail_std, windfall, \
                 regret, running_windfall, running_regret, net_windreg):
        
        # Initialize instance variables for disciplines and new rules
        self.D = Discips
        self.ir = irules_new
        
        # Initialize instance variables for windfall-regret data tracking
        self.pf = passfail
        self.pf_std = passfail_std
        self.wind = windfall
        self.reg = regret
        self.run_wind = running_windfall
        self.run_reg = running_regret
        self.net_wr = net_windreg
        
        # Initialize a copy of the discipline mirroring new input rule(s)
        self.D_red = copy.deepcopy(Discips)
        self.D_red = sortPoints(self.D_red, irules_new)
        
        # Place non-reduced and reduced dictionaries into a list
        self.D_list = [self.D, self.D_red]
        
        # Initialize a list of strings for looping (order matters!)
        self.strings = ['non_reduced', 'reduced']
        
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
        
        # Loop through non-reduced and reduced data
        for index, red_type in enumerate(self.strings):
            
            # Loop through each discipline
            for i, discip in enumerate(self.D_list[index]):
                
                # Test GPR at each point remaining for discipline BEFORE new rule
                means, stddevs = gpr[i].predict(discip['space_remaining'], return_std=True)
                
                # Append arrays to empty lists
                self.pf[i][red_type].append(means)
                self.pf_std[i][red_type].append(stddevs)
        
        # Return predicted passing and failing dictionaries with newest tests
        return self.pf, self.pf_std
    
    
    # Need to adjust tp_actual in each discipline because there may be different numbers of dimensions
    # Figure out how to do this for each input variable combination rather than only space as a whole
    def calcWindRegret(self, tp_actual):
        
        # Loop through non-reduced and reduced data
        for index, red_type in enumerate(self.strings):
            
            # Loop through each discipline
            for i, discip in enumerate(self.D_list[index]):
                
                # Determine length that a point covers in each direction
                dl = 1/(tp_actual**(1/len(discip['ins'])))
                
                # Establish running totals of windfall and regret
                running_wind = 0
                running_reg = 0
                net_wr = 0
                
                # Initalize matrices for windfall and regret tracking
                wind = np.empty_like(self.pf[i][red_type][-1])
                reg = np.empty_like(self.pf[i][red_type][-1])
                
                # Loop through each predicted point
                for j in range(0, self.pf[i][red_type][-1].shape[0]):
                    
                    # Check if point is predicted as infeasible (windfall chance)
                    if self.pf[i][red_type][-1][j] < 0:
                        
                        # Convert prediction to probability
                        prob_feas = 1.0 - stats.norm.cdf(-self.pf[i][red_type][-1][j]/self.pf_std[i][red_type][-1][j])
                        
                        # Store probability as local windfall and make regret small
                        wind[j] = prob_feas
                        reg[j] = 0
                        
                        # Add to running windfall total
                        running_wind += prob_feas*dl**(len(discip['ins']))
                    
                    # Do following if point is predicted feasible (regret chance)
                    else:
                        
                        # Convert prediction to probability
                        prob_feas = 1.0 - stats.norm.cdf(self.pf[i][red_type][-1][j]/self.pf_std[i][red_type][-1][j])
                        
                        # Store probability as local regret and make windfall small
                        reg[j] = prob_feas
                        wind[j] = 0
                        
                        # Add to running regret total
                        running_reg += prob_feas*dl**(len(discip['ins']))
                    
                    # Calculate the difference between the net windfall and regret
                    net_wr = running_wind - running_reg
                
                # Append matrices and values to proper list
                self.wind[i][red_type].append(wind)
                self.reg[i][red_type].append(reg)
                self.run_wind[i][red_type].append(running_wind)
                self.run_reg[i][red_type].append(running_reg)
                self.net_wr[i][red_type].append(net_wr)
                
                # Consider plotting net windfall-regret over time for each variable combination!
                
                
        # Return windfall and regret information
        return self.wind, self.reg, self.run_wind, self.run_reg, self.net_wr
    
    
    def quantRisk(self):
        
        # Initialize list for tracking space reduction risk of each discipline
        reduction_risk = []
        reduction_potential = []
        
        # Loop through each discipline
        for i in range(0, len(self.D)):
            
            # Calculate the "risk" or "potential value for the space reduction
            risk_or_pot = (self.net_wr[i]['reduced'][-1]/self.net_wr[i]['non_reduced'][-1] - 1) * 100
            
            # Check if reduced design space is risk affiliated
            if self.net_wr[i]['non_reduced'][-1] <= 0:
                
                # Append risk_or_pot value to the risk list
                reduction_risk.append(risk_or_pot)
                
                # Append 0.0 to the potential list
                reduction_potential.append(0.0)
                
                # Print results
                if risk_or_pot >= 0:
                    print(f"Discipline {i+1} experiences {round(risk_or_pot, 2)}% added risk for this space reduction.")
                else:
                    print(f"Discipline {i+1} experiences {-round(risk_or_pot, 2)}% reduced risk for this space reduction.")
                
            # Perform following commands as reduced design space is potential affiliated
            else:
                
                # Append risk_or_pot value to the potential list
                reduction_potential.append(risk_or_pot)
                
                # Append 0.0 to the risk list
                reduction_risk.append(0.0)
                
                # Print results
                if risk_or_pot >= 0:
                    print(f"Discipline {i+1} experiences {round(risk_or_pot, 2)}% added potential for this space reduction.")
                else:
                    print(f"Discipline {i+1} experiences {-round(risk_or_pot, 2)}% reduced potential for this space reduction.")
                
        # Return risk and potential of space reduction for each discipline
        return reduction_risk, reduction_potential
    
    
    # Surfaces are temporary and may need adjustment to fit other SBD problems
    # Need to add regret plot (combine into a single scale so I don't need two plots)
    # Need to add plots for space remaining with points that are eliminated
    def plotWindRegret(self, tp_actual):
        
        # Loop through non-reduced and reduced data
        for index, red_type in enumerate(self.strings):
            
            # Loop through each discipline
            for i, discip in enumerate(self.D_list[index]):
                
                # Print percent of space that would remain in discipline
                if index == 0:
                    print(f"Discipline {i+1} would go from "
                      f"{round((self.D_list[0][i]['space_remaining'].shape[0]/tp_actual)*100, 2)}% to "
                      f"{round((self.D_list[1][i]['space_remaining'].shape[0]/tp_actual)*100, 2)}%"
                      f" of its original design space remaining!")
    
                # Initialize an empty list for storing numpy arrays
                l = []
                
                # Surface plot
                j = np.linspace(0, 1, 4000)
                k = np.linspace(0, 1, 4000)
                j, k = np.meshgrid(j, k)
                
                if i == 0:
                    l.append(0.8*j**2 + 2*k**2 - 0.0)
                    l.append(0.8*j**2 + 2*k**2 - 0.4)
                    l.append(0.8*j**2 + 2*k**2 - 1.2)
                    l.append(0.8*j**2 + 2*k**2 - 1.6)
                elif i == 1:
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
                    if i < 2:
                        ax.plot_surface(j, k, l[m], color=colors[m], alpha=0.1, rstride=100, cstride=100)
                    else:
                        ax.plot_surface(l[m], j, k, color=colors[m], alpha=0.1, rstride=100, cstride=100)
                
                # Define the levels and discretize the windfall-regret data
                levels = np.linspace(-1, 1, 21)
                windfall_discrete = np.digitize(self.wind[i][red_type][-1], bins=levels) / 10
                regret_discrete = np.digitize(self.reg[i][red_type][-1], bins=levels) / 10
                wr_discrete = windfall_discrete - regret_discrete
                
                # When plotting space remaining data, use the discretized windfall values
                scatter = ax.scatter(discip['space_remaining'][:,0], \
                                     discip['space_remaining'][:,1], \
                                     discip['space_remaining'][:,2], c=wr_discrete, s=10, cmap='RdBu', alpha=1.0, vmin=-1, vmax=1)
                
                # Adjust the colorbar to reflect the levels
                cbar = plt.colorbar(scatter, ax=ax, ticks=levels, boundaries=levels)
                cbar.set_label('Windfall-Regret Scale')
                
                # Edit the color bar
                tick_labels = [f"{round(level, 1)}" for level in levels]
                tick_labels[0] = f"{tick_labels[0]} (Regret)"
                tick_labels[-1] = f"{tick_labels[-1]} (Windfall)"
                cbar.ax.set_yticklabels(tick_labels)
                
                # Gather and plot passing and failing remaining tested input indices
                pass_ind = np.where(discip['pass?'])[0].tolist()
                fail_ind = np.where(np.array(discip['pass?']) == False)[0].tolist()
                ax.scatter(discip['tested_ins'][pass_ind,0], \
                           discip['tested_ins'][pass_ind,1], \
                           discip['tested_ins'][pass_ind,2], c='lightgreen', alpha=1)
                ax.scatter(discip['tested_ins'][fail_ind,0], \
                           discip['tested_ins'][fail_ind,1], \
                           discip['tested_ins'][fail_ind,2], c='red', alpha=1)
                
                # Gather and plot passing and failing eliminated tested input indices
                if 'eliminated' in discip:
                    pass_ind = np.where(discip['eliminated']['pass?'])[0].tolist()
                    fail_ind = np.where(np.array(discip['eliminated']['pass?']) == False)[0].tolist()
                    ax.scatter(discip['eliminated']['tested_ins'][pass_ind,0], \
                               discip['eliminated']['tested_ins'][pass_ind,1], \
                               discip['eliminated']['tested_ins'][pass_ind,2], c='lightgreen', alpha=1)
                    ax.scatter(discip['eliminated']['tested_ins'][fail_ind,0], \
                               discip['eliminated']['tested_ins'][fail_ind,1], \
                               discip['eliminated']['tested_ins'][fail_ind,2], c='red', alpha=1)
                
                # Set axis limits
                ax.set_xlim([0, 1])
                ax.set_ylim([0, 1])
                ax.set_zlim([0, 1])
                
                # Set labels and title
                ax.set_xlabel(discip['ins'][0])
                ax.set_ylabel(discip['ins'][1])
                ax.set_zlabel(discip['ins'][2])
                ax.set_title(f"Discipline {i+1} {red_type} input space")
                
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
    
