"""
SUMMARY:
Uses formed perceptions of feasibility within each discipline's design space to
determine potentials for regret and windfall before quantifying the risk of a
space reduction decision by calculating the added potentials relative to
leaving the design spaces untouched.  Also visualizes these potentials for
regret and windfall (for SBD1 problem, specifically).

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
# from matplotlib.lines import Line2D
from point_sorter import sortPoints
from merge_constraints import sharedIndices


"""
FUNCTION
"""
# Function for repeated sharedIndices data
# FRAGILITY NEEDS TO BE CHECKED WITH ALL OF THE INPUT RULES ALREADY PROPOSED FOR A CURRENT TIME STAMP!
# aka non-reduced design space needs to be the one before ANY rules have been proposed for that specific time stamp!
# Consider making some sort of a copy for it...










"""
CLASS
"""
class windfallRegret:
    
    def __init__(self, Discips_fragility, irules_fragility):
        """
        Parameters
        ----------
        Discips_fragility : TYPE
            DESCRIPTION.
        irules_fragility : TYPE
            DESCRIPTION.
        """
        self.Df = Discips_fragility
        self.irf = irules_fragility
        return
    
    
    def calcWindRegret(self, passfail, passfail_std, pf_fragility, pf_std_fragility):
        
        # Initialize empty dictionaries
        windreg = {}
        run_wind = {}
        run_reg = {}
        
        # Loop through each new rule combo being proposed
        for rule, lis in passfail.items():
            
            # Add empty list to dictionaries
            windreg[rule+tuple(self.irf)] = []
            run_wind[rule+tuple(self.irf)] = []
            run_reg[rule+tuple(self.irf)] = []
            
            # Loop through each discipline's passfail data
            for ind_dic, dic in enumerate(lis):
                
                # Create empty dictionaries for discipline
                windreg[rule+tuple(self.irf)].append({})
                run_wind[rule+tuple(self.irf)].append({})
                run_reg[rule+tuple(self.irf)].append({})
                
                # Loop through each design space of discipline
                for ds, arr in dic.items():
                    
                    # Initialize empty arrays and values
                    windreg[rule+tuple(self.irf)][ind_dic][ds] = np.array([], dtype=float)
                    run_wind[rule+tuple(self.irf)][ind_dic][ds] = 0.0
                    run_reg[rule+tuple(self.irf)][ind_dic][ds] = 0.0
                
                # Make a copy of discipline taking the input rules into account
                d_copy = copy.deepcopy(self.Df[ind_dic])
                
                # Move values to eliminated section of discipline copy
                d_copy = sortPoints([d_copy], list(rule)+self.irf)
                
                # Create different index lists for input rule
                all_indices, indices_in_both, indices_not_in_B = \
                    sharedIndices(self.Df[ind_dic]['space_remaining'],
                                  d_copy[0]['space_remaining'])
                
                # Loop through each passfail value of the NON-REDUCED array
                for ind_pf, pf in enumerate(pf_fragility[ind_dic]):
                    
                    # Convert passfail prediction to complementary probability
                    prob_feas = 1.0 - stats.norm.cdf(abs(pf) / pf_std_fragility[ind_dic][ind_pf])
                    
                    # Check if point is in both non-reduced and reduced matrices
                    if ind_pf in indices_in_both:
                        
                        # Check if point predicted infeasible (windfall chance)
                        if pf < 0:
                            
                            # Consider changing rule key to include ALL OF THE RULES??? CREATE A NEW TUPLE?...add the tuple?????
                            # Add pos. probability to the proper dictionary arrays - Add value to bottom instead
                            windreg[rule+tuple(self.irf)][ind_dic]['non_reduced'] = np.append(windreg[rule+tuple(self.irf)][ind_dic]['non_reduced'], prob_feas)
                            windreg[rule+tuple(self.irf)][ind_dic]['reduced'] = np.append(windreg[rule+tuple(self.irf)][ind_dic]['reduced'], prob_feas)
                            # windreg[rule+tuple(self.irf)][ind_dic]['non_reduced'][ind_pf] = prob_feas
                            # windreg[rule+tuple(self.irf)][ind_dic]['reduced'][indices_in_both.index(ind_pf)] = prob_feas
                                        
                            # Add to proper running windfall count
                            run_wind[rule+tuple(self.irf)][ind_dic]['non_reduced'] += prob_feas
                            run_wind[rule+tuple(self.irf)][ind_dic]['reduced'] += prob_feas
                                        
                        # Do below if point predicted feasible (regret chance)
                        else:
                                        
                            # Add neg. probability to the proper dictionary arrays
                            windreg[rule+tuple(self.irf)][ind_dic]['non_reduced'] = np.append(windreg[rule+tuple(self.irf)][ind_dic]['non_reduced'], -prob_feas)
                            windreg[rule+tuple(self.irf)][ind_dic]['reduced'] = np.append(windreg[rule+tuple(self.irf)][ind_dic]['reduced'], -prob_feas)
                            # windreg[rule+tuple(self.irf)][ind_dic]['non_reduced'][ind_pf] = -prob_feas
                            # windreg[rule+tuple(self.irf)][ind_dic]['reduced'][indices_in_both.index(ind_pf)] = -prob_feas
                                        
                            # Add to proper running regret count
                            run_reg[rule+tuple(self.irf)][ind_dic]['non_reduced'] += prob_feas
                            run_reg[rule+tuple(self.irf)][ind_dic]['reduced'] += prob_feas
                            
                    # Do below if point is not in both non-reduced and reduced matrices
                    else:
                        
                        # Check if point is predicted infeasible (non-reduced: windfall chance, reduced: regret chance)
                        if pf < 0:
                            
                            # Add pos. probability to the proper dictionary arrays (Should I do leftover or put these values in reduced for graphing?)
                            windreg[rule+tuple(self.irf)][ind_dic]['non_reduced'] = np.append(windreg[rule+tuple(self.irf)][ind_dic]['non_reduced'], prob_feas)
                            windreg[rule+tuple(self.irf)][ind_dic]['leftover'] = np.append(windreg[rule+tuple(self.irf)][ind_dic]['leftover'], -prob_feas)
                            # windreg[rule+tuple(self.irf)][ind_dic]['non_reduced'][ind_pf] = prob_feas
                            # windreg[rule+tuple(self.irf)][ind_dic]['leftover'][indices_not_in_B.index(ind_pf)] = -prob_feas
                                            
                            # Add to proper running windfall count (Do I want to use leftover key at all?)
                            run_wind[rule+tuple(self.irf)][ind_dic]['non_reduced'] += prob_feas
                            run_reg[rule+tuple(self.irf)][ind_dic]['reduced'] += prob_feas
                        
                        # Do below if point is predicted feasible (non-reduced: regret chance, reduced: windfall chance)
                        else:
                                        
                            # Add neg. probability to the proper dictionary arrays
                            windreg[rule+tuple(self.irf)][ind_dic]['non_reduced'] = np.append(windreg[rule+tuple(self.irf)][ind_dic]['non_reduced'], -prob_feas)
                            windreg[rule+tuple(self.irf)][ind_dic]['leftover'] = np.append(windreg[rule+tuple(self.irf)][ind_dic]['leftover'], prob_feas)
                            # windreg[rule+tuple(self.irf)][ind_dic]['non_reduced'][ind_pf] = -prob_feas
                            # windreg[rule+tuple(self.irf)][ind_dic]['leftover'][indices_not_in_B.index(ind_pf)] = prob_feas
                                        
                            # Add to proper running windfall count
                            run_reg[rule+tuple(self.irf)][ind_dic]['non_reduced'] += prob_feas
                            run_wind[rule+tuple(self.irf)][ind_dic]['reduced'] += prob_feas
                            
                # Loop through each design space of discipline
                for ds, arr in dic.items():
                
                    # Divide probabilistic sums by number of remaining points - CHECK THAT I AM DIVIDING BY CORRECT THING AND SHOULDN'T BE TP_ACTUAL
                    run_wind[rule+tuple(self.irf)][ind_dic][ds] = run_wind[rule+tuple(self.irf)][ind_dic][ds] / self.Df[ind_dic]['space_remaining'].shape[0]
                    run_reg[rule+tuple(self.irf)][ind_dic][ds] = run_reg[rule+tuple(self.irf)][ind_dic][ds] / self.Df[ind_dic]['space_remaining'].shape[0]
                        
        # Returning windfall and regret information for new rule(s)
        return windreg, run_wind, run_reg
    
    
    def quantRisk(self, run_wind, run_reg, windreg):
        
        # Initialize empty dictionary
        risk = {}
        
        # Loop through each new rule (set) being proposed
        for rule, lis in run_wind.items():
            
            # Add empty list to dictionary
            risk[rule] = []
            
            # Print rule (set) being considered
            print(f"For the rule set {str(rule)}...")
            
            # Loop through each discipline's regret and windfall data
            for ind_dic, (reg_dic, wind_dic) in enumerate(zip(run_reg[rule], run_wind[rule])):
                
                ########## Space Remaining ##########
                # Print percent of space that would remain in discipline
                print(f"Discipline {ind_dic+1} would go from "
                      f"{round((windreg[rule][ind_dic]['non_reduced'].shape[0]/self.Df[ind_dic]['tp_actual'])*100, 2)}% to "
                      f"{round((windreg[rule][ind_dic]['reduced'].shape[0]/self.Df[ind_dic]['tp_actual'])*100, 2)}%"
                      f" of its original design space remaining!")
                
                
                ########## Regret and Windfall ##########
                
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
    
    
    def plotWindRegret(self, windreg):
        
        # Loop through each new rule (set) being proposed
        for rule, lis in windreg.items():
            
            # Loop through each discipline's windfall-regret values
            for ind_dic, dic in enumerate(windreg[rule]):
                
                # Make a copy of discipline taking the input rules into account
                d_copy = copy.deepcopy(self.Df[ind_dic])
                
                # Move values to eliminated section of discipline copy
                d_copy = sortPoints([d_copy], list(rule)+self.irf)
                
                # Create different index lists for input rule
                all_indices, indices_in_both, indices_not_in_B = \
                    sharedIndices(self.Df[ind_dic]['space_remaining'],
                                  d_copy[0]['space_remaining'])
                
                # Add each list to a different dictionary key
                diction = {"non_reduced": all_indices, 
                           "reduced": indices_in_both, 
                           "leftover": indices_not_in_B}
                
                # Loop through each design space of discipline
                for ds, arr in dic.items():
                    
                    # Continue if array is empty
                    if arr.shape[0] == 0: continue
                    
                    # Initialize an empty list for storing numpy arrays
                    l = []
                    
                    # Surface plot
                    j = np.linspace(0, 1, 4000)
                    k = np.linspace(0, 1, 4000)
                    j, k = np.meshgrid(j, k)
                    
                    if ind_dic == 0:
                        l.append(0.8*j**2 + 2*k**2 - 0.0)
                        l.append(0.8*j**2 + 2*k**2 - 0.4)
                        l.append(0.8*j**2 + 2*k**2 - 1.2)
                        l.append(0.8*j**2 + 2*k**2 - 1.6)
                    elif ind_dic == 1:
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
                    for m in range(0, len(l)):
                        if ind_dic < 2:
                            ax.plot_surface(j, k, l[m], color=colors[m], alpha=0.1, rstride=100, cstride=100)
                        else:
                            ax.plot_surface(l[m], j, k, color=colors[m], alpha=0.1, rstride=100, cstride=100)
                    
                    # Define the levels and discretize the windfall-regret data
                    levels = np.linspace(-0.5, 0.5, 11)
                    wr_discrete = (np.digitize(arr, bins=levels) - 6) / 10.0
                    
                    # Plot discretized space remaining points for design space
                    scatter = ax.scatter(self.Df[ind_dic]['space_remaining'][diction[ds], 0], \
                                         self.Df[ind_dic]['space_remaining'][diction[ds], 1], \
                                         self.Df[ind_dic]['space_remaining'][diction[ds], 2], \
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
                    # pass_ind = np.where(self.Df[ind_dic]['pass?'])[0].tolist()
                    # fail_ind = np.where(np.array(self.Df[ind_dic]['pass?']) == False)[0].tolist()
                    # ax.scatter(self.Df[ind_dic]['tested_ins'][pass_ind,0], \
                    #            self.Df[ind_dic]['tested_ins'][pass_ind,1], \
                    #            self.Df[ind_dic]['tested_ins'][pass_ind,2], c='lightgreen', alpha=1)
                    # ax.scatter(self.Df[ind_dic]['tested_ins'][fail_ind,0], \
                    #            self.Df[ind_dic]['tested_ins'][fail_ind,1], \
                    #            self.Df[ind_dic]['tested_ins'][fail_ind,2], c='red', alpha=1)
                    
                    # Gather and plot passing and failing eliminated tested input indices
                    # if 'eliminated' in self.Df[ind_dic]:
                    #     pass_ind = np.where(self.Df[ind_dic]['eliminated']['pass?'])[0].tolist()
                    #     fail_ind = np.where(np.array(self.Df[ind_dic]['eliminated']['pass?']) == False)[0].tolist()
                    #     ax.scatter(self.Df[ind_dic]['eliminated']['tested_ins'][pass_ind,0], \
                    #                self.Df[ind_dic]['eliminated']['tested_ins'][pass_ind,1], \
                    #                self.Df[ind_dic]['eliminated']['tested_ins'][pass_ind,2], c='lightgreen', alpha=1)
                    #     ax.scatter(self.Df[ind_dic]['eliminated']['tested_ins'][fail_ind,0], \
                    #                self.Df[ind_dic]['eliminated']['tested_ins'][fail_ind,1], \
                    #                self.Df[ind_dic]['eliminated']['tested_ins'][fail_ind,2], c='red', alpha=1)
                    
                    # Set axis limits
                    ax.set_xlim([0, 1])
                    ax.set_ylim([0, 1])
                    ax.set_zlim([0, 1])
                    
                    # Set labels and title
                    ax.set_xlabel(self.Df[ind_dic]['ins'][0])
                    ax.set_ylabel(self.Df[ind_dic]['ins'][1])
                    ax.set_zlabel(self.Df[ind_dic]['ins'][2])
                    # ax.set_title(f"Discipline {ind_dic+1} {ds} input space")
                    # plt.figtext(0.5, 0.01, f"New input rule set: {str(rule)}", ha="center", fontsize=10, va="bottom")
                    
                    # Create proxy artists for the legend
                    # legend_elements = [Line2D([0], [0], marker='o', color='w', label='Feasible',
                    #                           markersize=10, markerfacecolor='lightgreen'),
                    #                     Line2D([0], [0], marker='o', color='w', label='Infeasible',
                    #                           markersize=10, markerfacecolor='red')]
                    
                    # Add the legend to your axis
                    # ax.legend(handles=legend_elements, loc='upper left')
                    
                    # Show plot
                    plt.show()
            
        # Nothing to return as I am plotting information
        return
    
