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
import scipy.stats as stats
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF


"""
CLASS
"""
class windfallRegret:
    
    def __init__(self, Discips):
        self.D = Discips
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
    
    
    def predictData(self, gpr):
        
        # Initialize empty lists for predicted arrays of each discipline
        passfail = []
        passfail_std = []
        
        # Loop through each discipline
        for i in range(0, len(self.D)):
            
            # Test GPR at each point remaining for discipline before new rule
            means, stddevs = gpr[i].predict(self.D[i]['space_remaining'], return_std=True)
            
            # Append arrays to empty lists
            passfail.append(means)
            passfail_std.append(stddevs)
        
        return passfail, passfail_std
    
    
    def calcWindRegret(self, passfail, passfail_std):
        
        # Initialize empty lists for windfalls and regrets of each discipline
        windfall = []
        regret = []
        running_windfall = []
        running_regret = []
        
        # Loop through each discipline
        for i in range(0, len(self.D)):
            
            # Establish running totals of windfall and regret
            running_wind = 0
            running_reg = 0
            
            # Initalize matrices for windfall and regret tracking
            wind = np.empty_like(passfail[i])
            reg = np.empty_like(passfail[i])
            
            # Loop through each predicted point
            for j in range(0, passfail[i].shape[0]):
                
                # Check if point is predicted as infeasible (windfall chance)
                if passfail[i][j] < 0:
                    
                    # Convert prediction to probability
                    prob_feas = 1.0 - stats.norm.cdf(-passfail[i][j]/passfail_std[i][j])
                    
                    # Store probability as local windfall and make regret small
                    wind[j] = prob_feas
                    reg[j] = -10000000000
                    
                    # Add to running windfall total
                    running_wind += prob_feas
                
                # Do following if point is predicted feasible (regret chance)
                else:
                    
                    # Convert prediction to probability
                    prob_feas = 1.0 - stats.norm.cdf(passfail[i][j]/passfail_std[i][j])
                    
                    # Store probability as local regret and make windfall small
                    reg[j] = prob_feas
                    wind[j] = -10000000000
                    
                    # Add to running regret total
                    running_reg += prob_feas
            
            # Print statistics for discipline
            print('Stats for Discipline ' + str(i+1))
            print('Total windfall: ' + str(running_wind))
            print('Total regret: ' + str(running_reg))
            
            # Append matrices and values to proper list
            windfall.append(wind)
            regret.append(reg)
            running_windfall.append(running_wind)
            running_regret.append(running_reg)
                    
        # Return windfall and regret information
        return windfall, regret, running_windfall, running_regret
    
    # Surfaces are temporary and may need adjustment to fit other SBD problems
    # Need to add regret plot (combine into a single scale so I don't need two plots)
    # Need to add plots for space remaining with points that are eliminated
    def plotWindRegret(self, windfall, regret, tp_actual):
        
        # Loop through each discipline
        for i in range(0, len(self.D)):
            
            # Print percent of space that remains in discipline
            print(f"Discipline {i+1} has "
              f"{round((np.shape(self.D[i]['space_remaining'])[0]/tp_actual)*100, 2)}"
              f"% of its original design space remaining")

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
                    ax.plot_surface(j, k, l[m], color=colors[m], alpha=0.5, rstride=100, cstride=100)
                else:
                    ax.plot_surface(l[m], j, k, color=colors[m], alpha=0.5, rstride=100, cstride=100)
            
            # Define the levels and discretize the windfall data
            levels = np.linspace(0, 1, 11)
            windfall_discrete = np.digitize(windfall[i], bins=levels) / 10
            
            # When plotting space remaining data, use the discretized windfall values
            scatter = ax.scatter(self.D[i]['space_remaining'][:,0], \
                                self.D[i]['space_remaining'][:,1], \
                                self.D[i]['space_remaining'][:,2], c=windfall_discrete, s=10, cmap='viridis', alpha=0.4, vmin=0, vmax=1)
            
            # Adjust the colorbar to reflect the levels
            cbar = plt.colorbar(scatter, ax=ax, ticks=levels, boundaries=levels)
            cbar.set_label('Windfall Scale')

            
            # Gather and plot passing and failing remaining tested input indices
            pass_ind = np.where(self.D[i]['pass?'])[0].tolist()
            fail_ind = np.where(np.array(self.D[i]['pass?']) == False)[0].tolist()
            ax.scatter(self.D[i]['tested_ins'][pass_ind,0], \
                       self.D[i]['tested_ins'][pass_ind,1], \
                       self.D[i]['tested_ins'][pass_ind,2], c='green', alpha=1)
            ax.scatter(self.D[i]['tested_ins'][fail_ind,0], \
                       self.D[i]['tested_ins'][fail_ind,1], \
                       self.D[i]['tested_ins'][fail_ind,2], c='red', alpha=1)
            
            # Gather and plot passing and failing eliminated tested input indices
            if 'eliminated' in self.D[i]:
                pass_ind = np.where(self.D[i]['eliminated']['pass?'])[0].tolist()
                fail_ind = np.where(np.array(self.D[i]['eliminated']['pass?']) == False)[0].tolist()
                ax.scatter(self.D[i]['eliminated']['tested_ins'][pass_ind,0], \
                           self.D[i]['eliminated']['tested_ins'][pass_ind,1], \
                           self.D[i]['eliminated']['tested_ins'][pass_ind,2], c='green', alpha=1)
                ax.scatter(self.D[i]['eliminated']['tested_ins'][fail_ind,0], \
                           self.D[i]['eliminated']['tested_ins'][fail_ind,1], \
                           self.D[i]['eliminated']['tested_ins'][fail_ind,2], c='red', alpha=1)
            
            # Set axis limits
            ax.set_xlim([0, 1])
            ax.set_ylim([0, 1])
            ax.set_zlim([0, 1])
            
            # Set labels and title
            ax.set_xlabel(self.D[i]['ins'][0])
            ax.set_ylabel(self.D[i]['ins'][1])
            ax.set_zlabel(self.D[i]['ins'][2])
            ax.set_title('Discipline '+ str(i+1) + ' Remaining Input Space')
            
            # Show plot
            plt.show()
        
        # Nothing to return as I am plotting information
        return
    
