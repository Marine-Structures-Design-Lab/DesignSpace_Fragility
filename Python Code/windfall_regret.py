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
from point_sorter import sortPoints
from merge_constraints import sharedIndices


"""
CLASS
"""
class windfallRegret:
    
    def __init__(self, Discips, irules_new, passfail, passfail_std):
        self.D = Discips
        self.ir = irules_new
        self.pf = passfail
        self.pf_std = passfail_std
        return
    
    
    # Figure out how to do this for each input variable combination rather than only space as a whole
    def calcWindRegret(self):
        
        # Initialize empty dictionaries
        windreg = {}
        run_wind = {}
        run_reg = {}
        
        # Loop through each new rule (set) being proposed
        for rule, lis in self.pf.items():
            
            # Add empty list to dictionaries
            windreg[rule] = []
            run_wind[rule] = []
            run_reg[rule] = []
            
            # Loop through each discipline's passfail data
            for ind_dic, dic in enumerate(lis):
                
                # Create empty dictionaries for discipline
                windreg[rule].append({})
                run_wind[rule].append({})
                run_reg[rule].append({})
                
                # Loop through each design space of discipline
                for ds, arr in dic.items():
                    
                    # Initialize empty arrays and values
                    windreg[rule][-1][ds] = np.empty_like(arr)
                    run_wind[rule][-1][ds] = 0.0
                    run_reg[rule][-1][ds] = 0.0
                
                # Make a copy of discipline taking the input rule into account
                d_copy = copy.deepcopy(self.D[ind_dic])
                
                # Move values to eliminated section of discipline copy
                d_copy = sortPoints([d_copy], [rule])
                
                # Create different index lists for input rule
                all_indices, indices_in_both, indices_not_in_B = \
                    sharedIndices(self.D[ind_dic]['space_remaining'],
                                  d_copy[0]['space_remaining'])
                
                # Loop through each passfail value of the non-reduced matrix
                for ind_pf, pf in enumerate(dic['non_reduced']):
                    
                    # Convert passfail prediction to complementary probability
                    prob_feas = 1.0 - stats.norm.cdf(abs(pf)/\
                        self.pf_std[rule][ind_dic]['non_reduced'][ind_pf])
                    
                    # Check if point is in both non-reduced and reduced matrices
                    if ind_pf in indices_in_both:
                        
                        # Check if point is predicted infeasible (windfall chance)
                        if pf < 0:
                            
                            # Add pos. probability to the proper dictionary arrays
                            windreg[rule][ind_dic]['non_reduced'][ind_pf] = prob_feas
                            windreg[rule][ind_dic]['reduced'][indices_in_both.index(ind_pf)] = prob_feas
                                        
                            # Add to proper running windfall count
                            run_wind[rule][ind_dic]['non_reduced'] += prob_feas
                            run_wind[rule][ind_dic]['reduced'] += prob_feas
                                        
                        # Do below if point is predicted feasible (regret chance)
                        else:
                                        
                            # Add neg. probability to the proper dictionary arrays
                            windreg[rule][ind_dic]['non_reduced'][ind_pf] = -prob_feas
                            windreg[rule][ind_dic]['reduced'][indices_in_both.index(ind_pf)] = -prob_feas
                                        
                            # Add to proper running regret count
                            run_reg[rule][ind_dic]['non_reduced'] += prob_feas
                            run_reg[rule][ind_dic]['reduced'] += prob_feas
                            
                    # Do below if point is not in both non-reduced and reduced matrices
                    else:
                        
                        # Check if point is predicted infeasible (non-reduced: windfall chance, reduced: regret chance)
                        if pf < 0:
                            
                            # Add pos. probability to the proper dictionary arrays (Should I do leftover or put these values in reduced for graphing?)
                            windreg[rule][ind_dic]['non_reduced'][ind_pf] = prob_feas
                            windreg[rule][ind_dic]['leftover'][indices_not_in_B.index(ind_pf)] = -prob_feas
                                            
                            # Add to proper running windfall count (Do I want to use leftover key at all?)
                            run_wind[rule][ind_dic]['non_reduced'] += prob_feas
                            run_reg[rule][ind_dic]['reduced'] += prob_feas
                        
                        # Do below if point is predicted feasible (non-reduced: regret chance, reduced: windfall chance)
                        else:
                                        
                            # Add neg. probability to the proper dictionary arrays
                            windreg[rule][ind_dic]['non_reduced'][ind_pf] = -prob_feas
                            windreg[rule][ind_dic]['leftover'][indices_not_in_B.index(ind_pf)] = prob_feas
                                        
                            # Add to proper running windfall count
                            run_reg[rule][ind_dic]['non_reduced'] += prob_feas
                            run_wind[rule][ind_dic]['reduced'] += prob_feas
                            
                # Loop through each design space of discipline
                for ds, arr in dic.items():
                
                    # Divide probabilistic sums by number of remaining points - CHECK THAT I AM DIVIDING BY CORRECT THING AND SHOULDN'T BE TP_ACTUAL
                    run_wind[rule][ind_dic][ds] = run_wind[rule][ind_dic][ds] / self.D[ind_dic]['space_remaining'].shape[0]
                    run_reg[rule][ind_dic][ds] = run_reg[rule][ind_dic][ds] / self.D[ind_dic]['space_remaining'].shape[0]
                
                # Consider plotting windfall or regret over time for each variable combination!
                        
        # Returning windfall and regret information for new rule(s)
        return windreg, run_wind, run_reg
    
    
    def quantRisk(self, run_wind, run_reg):
        
        # Initialize empty dictionary
        risk = {}
        
        # Loop through each new rule being proposed
        for rule in self.ir:
            
            # Add empty list to dictionary
            risk[rule] = []
            
            # Loop through each discipline's regret and windfall data
            for ind_dic, (reg_dic, wind_dic) in enumerate(zip(run_reg[rule], run_wind[rule])):
                
                # Create an empty dictionary for regret and windfall tracking
                risk[rule].append({
                    "regret" : None, 
                    "windfall" : None
                    })
                
                ########## Regret ##########
                
                # Calculate the potential for regret for the space reduction
                ### + value indicates added potential for regret
                ### - value indicates reduced potential for regret
                if reg_dic['non_reduced'] == 0: reg_dic['non_reduced'] +=1e-10
                reg_value = reg_dic['reduced'] / reg_dic['non_reduced'] - 1
                
                # Print the potential for regret results of space reduction
                print(f"Discipline {ind_dic+1} has {round(reg_value, 2)} added potential for regret.")
                
                # Replace regret value in risk dictionary
                risk[rule][ind_dic]['regret'] = reg_value
                
                ########## Windfall ##########
                
                # Calculate the potential for windfall for the space reduction
                ### + value indicates added potential for windfall
                ### - value indicates reduced potential for windfall
                if wind_dic['non_reduced'] == 0: wind_dic['non_reduced'] += 1e-10
                wind_value = wind_dic['reduced'] / wind_dic['non_reduced'] - 1
                
                # Print the potential for windfal results of space reduction
                print(f"Discipline {ind_dic+1} has {round(wind_value, 2)} added potential for windfall.")
                
                # Replace windfall value in risk dictionary
                risk[rule][ind_dic]['windfall'] = wind_value
                
        # Return the dictionary for risk tracking
        return risk
    
    
    # Surfaces are temporary and may need adjustment to fit other SBD problems
    def plotWindRegret(self, windreg):
        
        # Loop through each discipline's windfall-regret values
        for ind1, d in enumerate(windreg):
            
            # Print percent of space that would remain in discipline
            print(f"Discipline {ind1+1} would go from "
                  f"{round((d['non_reduced'][-1].shape[0]/self.D[ind1]['tp_actual'])*100, 2)}% to "
                  f"{round((d['reduced'][-1].shape[0]/self.D[ind1]['tp_actual'])*100, 2)}%"
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
    
