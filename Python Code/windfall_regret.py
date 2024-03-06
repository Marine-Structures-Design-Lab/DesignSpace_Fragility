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
def initializeWR(irf, passfail):
    """
    Description
    -----------
    Initializes empty dictionaries for windfall and regret data-tracking that
    will be filled up later.

    Parameters
    ----------
    irf : List
        Sympy And or Or relationals or inequalities describing each new rule 
        being proposed of the current time stamp
    passfail : Dictionary
        Pass-fail predictions for the non-reduced, reduced, and leftover design
        spaces of rule combinations from newest round of fragility assessment

    Returns
    -------
    windreg : Dictionary
        Initialized for probability of windfall or regret data for each
        remaining discretized design point of various design spaces of a set of
        rules
    run_wind : Dictionary
        Initialized for total regret data for each remaining discretized design
        point of various design spaces of a set of rules
    run_reg : Dictionary
        Initialized for total windfall data for each remaining discretized
        design point of various design spaces of a set of rules
    """
    
    # Initialize empty dictionaries
    windreg = {}
    run_wind = {}
    run_reg = {}
    
    # Loop through each new rule combo being proposed
    for rule, lis in passfail.items():
        
        # Add empty list to dictionaries
        windreg[rule+tuple(irf)] = []
        run_wind[rule+tuple(irf)] = []
        run_reg[rule+tuple(irf)] = []
        
        # Loop through each discipline's passfail data
        for ind_dic, dic in enumerate(lis):
            
            # Create empty dictionaries for discipline
            windreg[rule+tuple(irf)].append({})
            run_wind[rule+tuple(irf)].append({})
            run_reg[rule+tuple(irf)].append({})
            
            # Loop through each design space of discipline
            for ds, arr in dic.items():
                
                # Initialize empty arrays and values
                windreg[rule+tuple(irf)][ind_dic][ds]=np.array([], dtype=float)
                run_wind[rule+tuple(irf)][ind_dic][ds] = 0.0
                run_reg[rule+tuple(irf)][ind_dic][ds] = 0.0
    
    # Return initialized dictionaries for windfall and regret tracking
    return windreg, run_wind, run_reg


def getIndices(Df, irf, ind_dic, rule):
    """
    Description
    -----------
    Collects a list of indices for rows of space remaining data that would be
    found in the non-reduced, reduced, and leftover design spaces for a
    particular combination of input rule(s)

    Parameters
    ----------
    Df : List of dictionaries
        Contains all of the relevant data pertaining to each discipline before
        any reductions have been made for the current time stamp
    irf : List
        Sympy And or Or relationals or inequalities describing each new rule
        being proposed of the current time stamp
    ind_dic : Integer
        Index of a particular discipline
    rule : tuple
        Current combination of input rule(s) being considered

    Returns
    -------
    all_indices : List
        Indices of points in A (non-reduced design space)
    indices_in_both : List
        Indices of points in A that are also found in B (reduced design space)
    indices_not_in_B : List
        Indices of points in A that are not found in B (leftover design space /
        area of the design space up for elimination)
    """
    
    # Make a copy of discipline taking the input rules into account
    d_copy = copy.deepcopy(Df[ind_dic])
    
    # Move values to eliminated section of discipline copy
    d_copy = sortPoints([d_copy], list(rule)+irf)
    
    # Create different index lists for input rule
    all_indices, indices_in_both, indices_not_in_B = sharedIndices\
        (Df[ind_dic]['space_remaining'], d_copy[0]['space_remaining'])
    
    # Return index information
    return all_indices, indices_in_both, indices_not_in_B


def complementProb(pf, pf_std_fragility):
    """
    Description
    -----------
    Calculates the complementary probability of feasibility from a predicted
    point's pass-fail value.

    Parameters
    ----------
    pf : Float
        Predicted pass-fail amount from the non-reduced design space
    pf_std_fragility : Float
        Standard deviation of predicted pass-fail amount

    Returns
    -------
    prob_feas : Float
        Complementary probability of feasibility
    """
    
    # Convert passfail prediction to complementary probability
    prob_feas = 1.0 - stats.norm.cdf(abs(pf) / pf_std_fragility)
    
    # Return complementary probability
    return prob_feas


def assignWR(prob_feas, ind_pf, indices_in_both, pf):
    """
    Description
    -----------
    Prepares complementary probability of feasiblity for assignment to windfall
    and regret dictionaries based on initially formed perceptions of feasiblity
    and design spaces in which a point falls.

    Parameters
    ----------
    prob_feas : Float
        Complementary probability of feasibility
    ind_pf : Integer
        Index of the discretized design point in the non-reduced data array
    indices_in_both : List
        Indices of points in both the non-reduced and reduced data arrays
    pf : Float
        Predicted pass-fail amount from the non-reduced design space

    Returns
    -------
    wr : Dictionary
        Potentials for regret or windfall of the non-reduced design space and
        the reduced or leftover design space with proper signage
    run_wind : Dictionary
        Newest contributions to running windfall totals of the non-reduced and
        reduced design spaces
    run_reg : Dictionary
        Newest contributions to running regret totals of the non-reduced and
        reduced design spaces
    """
    
    # Initialize empty dictionaries
    wr = {}
    run_wind = {}
    run_reg = {}
    
    # Check if point is in both non-reduced and reduced matrices
    if ind_pf in indices_in_both:
        
        # Check if point predicted infeasible (windfall chance)
        if pf < 0:
            
            # Assign complementary probability with proper sign
            wr['non_reduced'] = prob_feas
            wr['reduced'] = prob_feas
            
            # Assign to proper running windfall count
            run_wind['non_reduced'] = prob_feas
            run_wind['reduced'] = prob_feas
                        
        # Do below if point predicted feasible (regret chance)
        else:
                        
            # Assign complementary probability with proper sign
            wr['non_reduced'] = -prob_feas
            wr['reduced'] = -prob_feas
            
            # Assign to proper running regret count
            run_reg['non_reduced'] = prob_feas
            run_reg['reduced'] = prob_feas
            
    # Do below if point is not in both non-reduced and reduced matrices
    else:
        
        # Check if point is predicted infeasible
        if pf < 0:
            
            # Assign complementary probability with proper sign
            wr['non_reduced'] = prob_feas
            wr['leftover'] = -prob_feas
            
            # Assign to proper running windfall and regret counts
            run_wind['non_reduced'] = prob_feas
            run_reg['reduced'] = prob_feas
        
        # Do below if point is predicted feasible
        else:
                        
            # Assign complementary probability with proper sign
            wr['non_reduced'] = -prob_feas
            wr['leftover'] = prob_feas
            
            # Assign to proper running windfall and regret counts
            run_reg['non_reduced'] = prob_feas
            run_wind['reduced'] = prob_feas
    
    # Return complementary probability dictionaries
    return wr, run_wind, run_reg


"""
CLASS
"""
class windfallRegret:
    
    def __init__(self, Discips_fragility, irules_fragility):
        """
        Parameters
        ----------
        Discips_fragility : List of dictionaries
            Contains all of the relevant data pertaining to each discipline
            before any reductions have been made for the current time stamp
        irules_fragility : List
            Sympy And or Or relationals or inequalities describing each new
            rule being proposed of the current time stamp
        """
        self.Df = Discips_fragility
        self.irf = irules_fragility
        return
    
    
    def calcWindRegret(self, passfail, passfail_std, pf_fragility,
                       pf_std_fragility):
        """
        Description
        -----------
        Gathers windfall and regret data for non-reduced, reduced, and leftover
        design spaces.  The windreg data is used for plotting purposes.  The
        run_wind and run_reg data is used for risk quantification.

        Parameters
        ----------
        passfail : Dictionary
            Pass-fail predictions for the non-reduced, reduced, and leftover
            design spaces of rule combinations from newest round of fragility
            assessment
        passfail_std : Dictionary
            Standard deviations of pass-fail predictions described above
        pf_fragility : List of numpy arrays
            Pass-fail predictions for the non-reduced design spaces of each
            discipline before any new rule(s) are proposed in the current time
            stamp
        pf_std_fragility : List of numpy arrays
            Standard deviations of pass-fail predictions described above
        
        Returns
        -------
        windreg : Dictionary
            Windfall and regret data for each discretized point remaining in
            the non-reduced, reduced, and leftover design spaces of each 
            discipline for all of the rules proposed in the current time stamp
        run_wind : Dictionary
            Fraction of windfall potential in remaining design spaces for all
            of the rules proposed in the current time stamp
        run_reg : Dictionary
            Fraction of regret potential in remaining design spaces for all of
            the rules proposed in the current time stamp
        """
        
        # Initialize empty dictionaries
        windreg, run_wind, run_reg = initializeWR(self.irf, passfail)
        
        # Loop through each new rule combo being proposed
        for rule, lis in passfail.items():
            
            # Loop through each discipline's passfail data
            for ind_dic, dic in enumerate(lis):
                
                # Create different index lists for input rule
                all_indices, indices_in_both, indices_not_in_B = \
                    getIndices(self.Df, self.irf, ind_dic, rule)
                
                # Loop through each passfail value of the NON-REDUCED array
                for ind_pf, pf in enumerate(pf_fragility[ind_dic]):
                    
                    # Convert passfail prediction to complementary probability
                    prob_feas = complementProb\
                        (pf, pf_std_fragility[ind_dic][ind_pf])
                    
                    # Prepare complementary probabilities for proper assignment
                    wr, r_wind, r_reg = assignWR(prob_feas, ind_pf,
                                                 indices_in_both, pf)
                    
                    # Loop through each key-value pair in wr dictionary
                    for ds, comp_prob in wr.items():
                        
                        # Append value to list of values of proper windreg key
                        windreg[rule+tuple(self.irf)][ind_dic][ds] = np.append\
                            (windreg[rule+tuple(self.irf)][ind_dic][ds],
                             comp_prob)
                    
                    # Loop through each key-value pair in r_wind dictionary
                    for ds, comp_prob in r_wind.items():
                        
                        # Add probability to proper running windfall sum
                        run_wind[rule+tuple(self.irf)][ind_dic][ds]+=r_wind[ds]
                    
                    # Loop through each key-value pair in r_reg dictionary
                    for ds, comp_prob in r_reg.items():
                        
                        # Add probability to proper running regret sum
                        run_reg[rule+tuple(self.irf)][ind_dic][ds] += r_reg[ds]
                            
                # Loop through each design space of discipline
                for ds, arr in dic.items():
                
                    # Divide probabilistic sums by number of remaining points
                    run_wind[rule+tuple(self.irf)][ind_dic][ds] = \
                        run_wind[rule+tuple(self.irf)][ind_dic][ds] / \
                            self.Df[ind_dic]['space_remaining'].shape[0]
                    run_reg[rule+tuple(self.irf)][ind_dic][ds] = \
                        run_reg[rule+tuple(self.irf)][ind_dic][ds] / \
                            self.Df[ind_dic]['space_remaining'].shape[0]
                        
        # Returning windfall and regret information for new rule(s)
        return windreg, run_wind, run_reg
    
    
    def quantRisk(self, run_wind, run_reg, windreg):
        """
        Description
        -----------
        Determines the amount of space that would remaing in each discipline
        if they were to move forward with the new rule combo(s) being
        considered for the current time stamp and calculates the entire design
        spaces' added potentials for regret and windfall.

        Parameters
        ----------
        run_wind : Dictionary
            Fraction of windfall potential in remaining design spaces for all
            of the rules proposed in the current time stamp
        run_reg : Dictionary
            Fraction of regret potential in remaining design spaces for all of
            the rules proposed in the current time stamp
        windreg : Dictionary
            Windfall and regret data for each discretized point remaining in
            the non-reduced, reduced, and leftover design spaces of each 
            discipline for all of the rules proposed in the current time stamp

        Returns
        -------
        risk : Dictionary
            Added potentials for regret and windfall accompanying a set of
            input rule(s) for the current timestamp
        """
        
        # Initialize empty dictionary
        risk = {}
        
        # Loop through each new rule (set) being proposed
        for rule, lis in run_wind.items():
            
            # Add empty list to dictionary
            risk[rule] = []
            
            # Print rule (set) being considered
            print(f"For the rule set {str(rule)}...")
            
            # Loop through each discipline's regret and windfall data
            for ind_dic, (reg_dic, wind_dic) in enumerate(zip(run_reg[rule], 
                                                              run_wind[rule])):
                
                # Calculated non-reduced and reduced percentages
                nrp = round((windreg[rule][ind_dic]['non_reduced'].shape[0] / \
                    self.Df[ind_dic]['tp_actual'])*100, 2)
                rp = round((windreg[rule][ind_dic]['reduced'].shape[0] / \
                    self.Df[ind_dic]['tp_actual'])*100, 2)
                
                ########## Space Remaining ##########
                # Print percent of space that would remain in discipline
                print(f"Discipline {ind_dic+1} would go from {nrp}% to {rp}% "
                      f"of its original design space remaining!")
                
                
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
                print(f"Discipline {ind_dic+1} has {round(reg_value, 2)} added"
                      f" potential for regret.")
                
                # Replace regret value in risk dictionary
                risk[rule][ind_dic]['regret'] = reg_value
                
                
                ########## Windfall ##########
                
                # Calculate the potential for windfall for the space reduction
                ### + value indicates added potential for windfall
                ### - value indicates reduced potential for windfall
                if wind_dic['non_reduced'] == 0: wind_dic['non_reduced']+=1e-10
                wind_value = wind_dic['reduced'] / wind_dic['non_reduced'] - 1
                
                # Print the potential for windfal results of space reduction
                print(f"Discipline {ind_dic+1} has {round(wind_value, 2)} "
                      f"added potential for windfall.")
                
                # Replace windfall value in risk dictionary
                risk[rule][ind_dic]['windfall'] = wind_value
                
        # Return the dictionary for risk tracking
        return risk
    
    
    def plotWindRegret(self, windreg):
        """
        Description
        -----------
        Visualizes the windfall and regret potentials of remaining design
        points for each design space of each discipline specifically for the
        SBD1 problem.

        Parameters
        ----------
        windreg : Windfall and regret data for each discretized point remaining
        in the non-reduced, reduced, and leftover design spaces of each 
        discipline for all of the rules proposed in the current time stamp
        """
        
        # Loop through each new rule (set) being proposed
        for rule, lis in windreg.items():
            
            # Loop through each discipline's windfall-regret values
            for ind_dic, dic in enumerate(windreg[rule]):
                
                # Create different index lists for input rule
                all_indices, indices_in_both, indices_not_in_B = \
                    getIndices(self.Df, self.irf, ind_dic, rule)
                
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
                    
                    # Create surface plots
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
                            ax.plot_surface(j, k, l[m], color=colors[m], 
                                            alpha=0.1, rstride=100, 
                                            cstride=100)
                        else:
                            ax.plot_surface(l[m], j, k, color=colors[m], 
                                            alpha=0.1, rstride=100, 
                                            cstride=100)
                    
                    # Define the levels and discretize the windfall-regret data
                    levels = np.linspace(-0.5, 0.5, 11)
                    wr_discrete = (np.digitize(arr, bins=levels) - 6) / 10.0
                    
                    # Plot discretized space remaining points for design space
                    scatter = ax.scatter \
                        (self.Df[ind_dic]['space_remaining'][diction[ds], 0],
                         self.Df[ind_dic]['space_remaining'][diction[ds], 1],
                         self.Df[ind_dic]['space_remaining'][diction[ds], 2],
                         c=wr_discrete, s=10, cmap='RdBu', alpha=1.0, 
                         vmin=-0.5, vmax=0.5)
                    
                    # Adjust the colorbar to reflect the levels
                    cbar = plt.colorbar(scatter, ax=ax, ticks=levels,
                                        boundaries=levels)
                    cbar.set_label('Windfall-Regret Scale')
                    
                    # Edit the color bar
                    tick_labels = [f"{round(level, 1)}" for level in levels]
                    tick_labels[0] = f"{tick_labels[0]} (Regret)"
                    tick_labels[-1] = f"{tick_labels[-1]} (Windfall)"
                    cbar.ax.set_yticklabels(tick_labels)
                    
                    # Plot passing and failing remaining tested input indices
                    # pass_ind = np.where(self.Df[ind_dic]['pass?'])[0].tolist()
                    # fail_ind = np.where\
                    #     (np.array(self.Df[ind_dic]['pass?']) == False)[0]\
                    #         .tolist()
                    # ax.scatter(self.Df[ind_dic]['tested_ins'][pass_ind,0], \
                    #             self.Df[ind_dic]['tested_ins'][pass_ind,1], \
                    #             self.Df[ind_dic]['tested_ins'][pass_ind,2], 
                    #             c='lightgreen', alpha=1)
                    # ax.scatter(self.Df[ind_dic]['tested_ins'][fail_ind,0], \
                    #             self.Df[ind_dic]['tested_ins'][fail_ind,1], \
                    #             self.Df[ind_dic]['tested_ins'][fail_ind,2], 
                    #             c='red', alpha=1)
                    
                    # Plot passing and failing eliminated tested input indices
                    # if 'eliminated' in self.Df[ind_dic]:
                    #     pass_ind = np.where(self.Df\
                    #         [ind_dic]['eliminated']['pass?'])[0].tolist()
                    #     fail_ind = np.where(np.array(self.Df[ind_dic]\
                    #         ['eliminated']['pass?']) == False)[0].tolist()
                    #     ax.scatter(self.Df[ind_dic]['eliminated']\
                    #         ['tested_ins'][pass_ind,0],
                    #         self.Df[ind_dic]['eliminated']\
                    #         ['tested_ins'][pass_ind,1],
                    #         self.Df[ind_dic]['eliminated']\
                    #         ['tested_ins'][pass_ind,2], c='lightgreen',
                    #         alpha=1)
                    #     ax.scatter(self.Df[ind_dic]['eliminated']\
                    #         ['tested_ins'][fail_ind,0],
                    #         self.Df[ind_dic]['eliminated']\
                    #         ['tested_ins'][fail_ind,1],
                    #         self.Df[ind_dic]['eliminated']\
                    #         ['tested_ins'][fail_ind,2], c='red', alpha=1)
                    
                    # Set axis limits
                    ax.set_xlim([0, 1])
                    ax.set_ylim([0, 1])
                    ax.set_zlim([0, 1])
                    
                    # Set labels and title
                    ax.set_xlabel(self.Df[ind_dic]['ins'][0])
                    ax.set_ylabel(self.Df[ind_dic]['ins'][1])
                    ax.set_zlabel(self.Df[ind_dic]['ins'][2])
                    # ax.set_title(f"Discipline {ind_dic+1} {ds} input space")
                    # plt.figtext(0.5, 0.01, f"New input rule set: {str(rule)}", 
                    #             ha="center", fontsize=10, va="bottom")
                    
                    # Create proxy artists for the legend
                    # legend_elements = [Line2D([0], [0], marker='o', color='w', 
                    #                           label='Feasible', markersize=10, 
                    #                           markerfacecolor='lightgreen'),
                    #                    Line2D([0], [0], marker='o', color='w', 
                    #                           label='Infeasible',markersize=10, 
                    #                           markerfacecolor='red')]
                    
                    # Add the legend to your axis
                    # ax.legend(handles=legend_elements, loc='upper left')
                    
                    # Show plot
                    plt.show()
            
        # Nothing to return
        return
    
