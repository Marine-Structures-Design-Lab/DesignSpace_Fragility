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
import itertools
import matplotlib.pyplot as plt
# from matplotlib.lines import Line2D
from point_sorter import sortPoints
from merge_constraints import sharedIndices


"""
SECONDARY FUNCTIONS
"""
def initializeWR(irf, passfail, frag_ext, Df):
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
    frag_ext : Dictionary
        Different extensions to the initial fragility framework extension
        that a design manager wants to include in the assessment
    Df : Dictionary
        All information pertaining to each discipline at the beginning of
        the newest space reduction cycle

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
    
    # Make input rule list into a tuple
    irf_tuple = tuple(irf)
    
    # Loop through each new rule combo being proposed
    for rule, lis in passfail.items():
        
        # Create a dictionary key
        rule_key = rule + irf_tuple
        
        # Add empty list to dictionaries
        windreg[rule_key] = []
        run_wind[rule_key] = []
        run_reg[rule_key] = []
        
        # Loop through each discipline's passfail data
        for ind_dic, dic in enumerate(lis):
            
            # Initialize empty dictionaries
            new_dict1 = {}
            new_dict2 = {}
            
            # Loop through the discipline's subspace dimensions
            for r in frag_ext.get('sub_spaces', len(Df[ind_dic]['ins'])):
                
                # Continue if number of dimensions is greater than discipline's
                # number of design variables available
                if r > len(Df[ind_dic]['ins']): continue
                
                # Loop through each combination of design variables at r-size
                for combo in itertools.combinations(Df[ind_dic]['ins'], r):
                    
                    # Assign an empty dictionary to the nested dictionaries
                    new_dict1[combo] = {}
                    new_dict2[combo] = {}
            
            # Append dictionary to discipline
            windreg[rule_key].append({})
            run_wind[rule_key].append(new_dict1)
            run_reg[rule_key].append(new_dict2)
            
            # Loop through each design space of discipline
            for ds, arr in dic.items():
                
                # Initialize empty arrays and values
                windreg[rule_key][ind_dic][ds]=np.array([], dtype=float)
                for combo in run_wind[rule_key][ind_dic]:
                    run_wind[rule_key][ind_dic][combo][ds] = 0.0
                    run_reg[rule_key][ind_dic][combo][ds] = 0.0
    
    # Return initialized dictionaries for windfall and regret tracking
    return windreg, run_wind, run_reg


def getIndices(Df, irf, ind_dic, rule):
    """
    Description
    -----------
    Collects a list of indices for rows of space remaining data that would be
    found in the non-reduced, reduced, and leftover design spaces for a
    particular combination of input rule(s).

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


def minmaxNormalize(data):
    """
    Description
    -----------
    Normalizes data between 0 and 1.

    Parameters
    ----------
    data : Numpy array
        Data to be normalized

    Returns
    -------
    "normalized data" : Numpy array
        Array of floats that is normalized between 0 and 1
    """
    
    # Check if no data available
    if len(data) == 0:
        
        # Return an empty array
        return np.array([])
    
    # Determine minimum and maximum values in data
    min_val = np.min(data)
    max_val = np.max(data)
    
    # Check if max and min values are the same to avoid division by zero
    if max_val == min_val:
        
        # Return array of zeros
        return np.zeros_like(data)
    
    # Return normalized data
    return (data - min_val) / (max_val - min_val)


def assignWR(prob_tve, ind_pf, indices_in_both, pf):
    """
    Description
    -----------
    Prepares complementary probability of feasiblity or TVE for assignment to
    windfall and regret dictionaries based on initially formed perceptions of 
    feasiblity and design spaces in which a point falls.

    Parameters
    ----------
    prob_feas : Float
        Complementary probability of feasibility or TVE
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
            
            # Assign complementary probability or TVE with proper sign
            wr['non_reduced'] = prob_tve
            wr['reduced'] = prob_tve
            
            # Assign to proper running windfall count
            run_wind['non_reduced'] = prob_tve
            run_wind['reduced'] = prob_tve
                        
        # Do below if point predicted feasible (regret chance)
        else:
                        
            # Assign complementary probability or TVE with proper sign
            wr['non_reduced'] = -prob_tve
            wr['reduced'] = -prob_tve
            
            # Assign to proper running regret count
            run_reg['non_reduced'] = prob_tve
            run_reg['reduced'] = prob_tve
            
    # Do below if point is not in both non-reduced and reduced matrices
    else:
        
        # Check if point is predicted infeasible
        if pf < 0:
            
            # Assign complementary probability or TVE with proper sign
            wr['non_reduced'] = prob_tve
            wr['leftover'] = -prob_tve
            
            # Assign to proper running windfall and regret counts
            run_wind['non_reduced'] = prob_tve
            run_reg['reduced'] = prob_tve
        
        # Do below if point is predicted feasible
        else:
                        
            # Assign complementary probability or TVE with proper sign
            wr['non_reduced'] = -prob_tve
            wr['leftover'] = prob_tve
            
            # Assign to proper running windfall and regret counts
            run_reg['non_reduced'] = prob_tve
            run_wind['reduced'] = prob_tve
    
    # Return complementary probability or TVE dictionaries
    return wr, run_wind, run_reg


def averageWR():
    """
    Description
    -----------
    Calculate the proper
    
    Parameters
    ----------
    

    Returns
    -------
    
    """
    
    
    return


"""
MAIN FUNCTIONS
"""

def evalCompProb(pf_fragility, pf_std_fragility):
    """
    Description
    -----------
    Calculates and normalizes the complementary probabilities of feasibility
    for remaining design solutions in each discipline's non-reduced design
    space.

    Parameters
    ----------
    pf_fragility : List
        Each discipline's pass-fail predictions for the non-reduced design
        space at the beginning of the space reduction cycle
    pf_std_fragility : List
        Each discipline's pass-fail standard deviations for the non-reduced
        design space at the beginning of the space reduction cycle

    Returns
    -------
    prob_feas : List of numpy arrays
        Normalized complementary probabilities of feasibility for each
        discipline's non-reduced design space
    """
    
    # Initialize empty complementary probability list
    prob_feas = [None for _ in pf_fragility]
    
    # Loop through each discipline
    for i, (discip_pf, discip_pf_std) in enumerate(zip(pf_fragility, 
                                                       pf_std_fragility)):
        
        # Initialize a numpy array for complementary probabilities
        prob_feas[i] = np.zeros_like(pf_fragility[i])
        
        # Loop through each passfail value of the NON-REDUCED array
        for ind_pf, pf in enumerate(pf_fragility[i]):
            
            # Convert passfail prediction to complementary probability
            prob_feas[i][ind_pf] = complementProb\
                (pf, pf_std_fragility[i][ind_pf])
        
        # Normalize the complementary probabilities
        prob_feas[i] = minmaxNormalize(prob_feas[i])
        
    # Return normalized complementary probabilities of feasibility
    return prob_feas


def calcWindRegret(irf, Df, passfail, prob_tve, pf_fragility, frag_ext):
    """
    Description
    -----------
    Gathers windfall and regret data for non-reduced, reduced, and leftover
    design spaces.  The windreg data is used for plotting purposes.  The
    run_wind and run_reg data is used for risk quantification.

    Parameters
    ----------
    irf : List
        Sympy and/or relationals detailing all of the new space reduction
        rules of the current space reduction cycle
    Df : Dictionary
        All information pertaining to each discipline at the beginning of
        the newest space reduction cycle
    passfail : Dictionary
        Pass-fail predictions for the non-reduced, reduced, and leftover
        design spaces of rule combinations from newest round of fragility
        assessment
    prob_tve : List of numpy arrays
        Either each discipline's complementary probabilities of feasibility or
        TVE values for the non-reduced design space
    pf_fragility : List of numpy arrays
        Pass-fail predictions for the non-reduced design spaces of each
        discipline before any new rule(s) are proposed in the current time
        stamp
    frag_ext : Dictionary
        Different extensions to the initial fragility framework extension
        that a design manager wants to include in the assessment
    
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
    windreg, run_wind, run_reg = initializeWR(irf, passfail, frag_ext, Df)
    
    # Make input rule list into a tuple
    irf_tuple = tuple(irf)
    
    # Loop through each new rule combo being proposed
    for rule, lis in passfail.items():
        
        # Create a dictionary key
        rule_key = rule + irf_tuple
        
        # Loop through each discipline's passfail data
        for ind_dic, dic in enumerate(lis):
            
            # Create different index lists for input rule
            all_indices, indices_in_both, indices_not_in_B = \
                getIndices(Df, irf, ind_dic, rule)
            
            # Loop through each complementary probability or TVE value
            for ind_pf, p_tve in enumerate(prob_tve[ind_dic]):
                
                # Prepare complementary probability or TVE for assignments
                wr, r_wind, r_reg = assignWR(p_tve, ind_pf,
                                             indices_in_both, 
                                             pf_fragility[ind_dic][ind_pf])
                
                # Loop through each key-value pair in wr dictionary
                for ds, comp_prob in wr.items():
                    
                    # Append value to list of values of proper windreg key
                    windreg[rule_key][ind_dic][ds] = np.append\
                        (windreg[rule_key][ind_dic][ds],
                         comp_prob)
                
                # Loop through each subspace being assessed
                for combo in run_wind[rule_key][ind_dic]:
                    
                    
                    
                    
                
                # Loop through each key-value pair in r_wind dictionary - Fix this starting here!!!
                for ds, comp_prob in r_wind.items():
                    
                    # Add probability or TVE to proper running windfall sum
                    run_wind[rule_key][ind_dic][ds]+=r_wind[ds]
                
                # Loop through each key-value pair in r_reg dictionary
                for ds, comp_prob in r_reg.items():
                    
                    # Add probability or TVE to proper running regret sum
                    run_reg[rule_key][ind_dic][ds] += r_reg[ds]
                        
            # Loop through each design space of discipline
            for ds, arr in dic.items():
            
                # Divide probability or TVE sums by number of remaining points
                if Df[ind_dic]['space_remaining'].shape[0] > 0:
                    run_wind[rule_key][ind_dic][ds] = \
                        run_wind[rule_key][ind_dic][ds] / \
                            Df[ind_dic]['space_remaining'].shape[0]
                    run_reg[rule_key][ind_dic][ds] = \
                        run_reg[rule_key][ind_dic][ds] / \
                            Df[ind_dic]['space_remaining'].shape[0]
                else:
                    run_wind[rule_key][ind_dic][ds] = 0.0
                    run_reg[rule_key][ind_dic][ds] = 0.0
                    
    # Returning windfall and regret information for new rule(s)
    return windreg, run_wind, run_reg


def quantRisk(Df, run_wind, run_reg, windreg):
    """
    Description
    -----------
    Determines the amount of space that would remaing in each discipline
    if they were to move forward with the new rule combo(s) being
    considered for the current time stamp and calculates the entire design
    spaces' added potentials for regret and windfall.

    Parameters
    ----------
    Df : Dictionary
        Contains all of the information relevant to each discipline prior to
        the newest space reduction cycle
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
        
        # Add empty dictionary to dictionary
        risk[rule] = {}
        
        # Print rule (set) being considered
        print(f"For the rule set {str(rule)}...")
        
        # Loop through each discipline's regret and windfall data
        for ind_dic, (reg_dic, wind_dic) in enumerate(zip(run_reg[rule], 
                                                          run_wind[rule])):
            
            ########## Space Remaining ##########
            
            # Calculate non-reduced and reduced percentages
            nrp = round((windreg[rule][ind_dic]['non_reduced'].shape[0] / \
                Df[ind_dic]['tp_actual'])*100, 2)
            rp = round((windreg[rule][ind_dic]['reduced'].shape[0] / \
                Df[ind_dic]['tp_actual'])*100, 2)
            
            # Print percent of space that would remain in discipline
            print(f"Discipline {ind_dic+1} would go from {nrp}% to {rp}% "
                  f"of its original design space remaining!")
            
            # Loop through the discipline's subspace dimensions
            for r in frag_ext.get('sub_spaces', len(Df[ind_dic]['ins'])):
                
                # Continue if number of dimensions is greater than discipline's
                # number of design variables available
                if r > len(Df[ind_dic]['ins']): continue
                
                # Loop through each combination of design variables at r-size
                for combo in itertools.combinations(Df[ind_dic]['ins'], r):
                    
                    # Assign an empty list to the nested dictionary
                    risk[rule][combo] = []
            
            
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
            reg_value = reg_dic['reduced'] / reg_dic['non_reduced'] - 1 \
                if reg_dic['non_reduced'] != 0 else 0.0
            
            # Print the potential for regret results of space reduction
            print(f"Discipline {ind_dic+1} has {round(reg_value, 2)} added"
                  f" potential for regret.")
            
            # Replace regret value in risk dictionary
            risk[rule][ind_dic]['regret'] = reg_value
            
            
            ########## Windfall ##########
            
            # Calculate the potential for windfall for the space reduction
            ### + value indicates added potential for windfall
            ### - value indicates reduced potential for windfall
            wind_value = wind_dic['reduced'] / wind_dic['non_reduced'] - 1\
                if wind_dic['non_reduced'] != 0 else 0.0
            
            # Print the potential for windfal results of space reduction
            print(f"Discipline {ind_dic+1} has {round(wind_value, 2)} "
                  f"added potential for windfall.")
            
            # Replace windfall value in risk dictionary
            risk[rule][ind_dic]['windfall'] = wind_value
            
    # Return the dictionary for risk tracking
    return risk


def plotWindRegret(Df, irf, windreg):
    """
    Description
    -----------
    Visualizes the windfall and regret potentials of remaining design
    points for each design space of each discipline specifically for the
    SBD1 problem.

    Parameters
    ----------
    Df : Dictionary
        Contains all of the information relevant to each discipline prior to
        the newest space reduction cycle
    irf : List
        Sympy And or Or relationals or inequalities describing each new
        rule being proposed of the current time stamp
    windreg : Dictionary
        Windfall and regret data for each discretized point remaining
        in the non-reduced, reduced, and leftover design spaces of each 
        discipline for all of the rules proposed in the current time stamp
    """
    
    # Loop through each new rule (set) being proposed
    for rule, lis in windreg.items():
        
        # Loop through each discipline's windfall-regret values
        for ind_dic, dic in enumerate(windreg[rule]):
            
            # Create different index lists for input rule
            all_indices, indices_in_both, indices_not_in_B = \
                getIndices(Df, irf, ind_dic, rule)
            
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
                levels = np.linspace(-1.0, 1.0, 21)
                wr_discrete = (np.digitize(arr, bins=levels) - 11) / 10.0
                
                # Plot discretized space remaining points for design space
                scatter = ax.scatter(
                    Df[ind_dic]['space_remaining'][diction[ds], 0],
                    Df[ind_dic]['space_remaining'][diction[ds], 1],
                    Df[ind_dic]['space_remaining'][diction[ds], 2],
                    c=wr_discrete, s=10, cmap='RdBu', alpha=1.0, 
                    vmin=-1, vmax=1  # Set vmin and vmax to -1 and 1
                )
                
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
                # fail_ind = np.where(
                #     np.array(self.Df[ind_dic]['pass?']) == False)[0].tolist()
                # ax.scatter(self.Df[ind_dic]['tested_ins'][pass_ind,0],
                #             self.Df[ind_dic]['tested_ins'][pass_ind,1],
                #             self.Df[ind_dic]['tested_ins'][pass_ind,2], 
                #             c='lightgreen', alpha=1)
                # ax.scatter(self.Df[ind_dic]['tested_ins'][fail_ind,0],
                #             self.Df[ind_dic]['tested_ins'][fail_ind,1],
                #             self.Df[ind_dic]['tested_ins'][fail_ind,2], 
                #             c='red', alpha=1)
                
                # Plot passing and failing eliminated tested input indices
                # if 'eliminated' in self.Df[ind_dic]:
                #     pass_ind = np.where(self.Df[
                #         ind_dic]['eliminated']['pass?'])[0].tolist()
                #     fail_ind = np.where(np.array(self.Df[ind_dic]
                #         ['eliminated']['pass?']) == False)[0].tolist()
                #     ax.scatter(self.Df[ind_dic]['eliminated']
                #         ['tested_ins'][pass_ind,0],
                #         self.Df[ind_dic]['eliminated']
                #         ['tested_ins'][pass_ind,1],
                #         self.Df[ind_dic]['eliminated']
                #         ['tested_ins'][pass_ind,2], c='lightgreen',
                #         alpha=1)
                #     ax.scatter(self.Df[ind_dic]['eliminated']
                #         ['tested_ins'][fail_ind,0],
                #         self.Df[ind_dic]['eliminated']
                #         ['tested_ins'][fail_ind,1],
                #         self.Df[ind_dic]['eliminated']
                #         ['tested_ins'][fail_ind,2], c='red', alpha=1)
                
                # Set axis limits
                ax.set_xlim([0, 1])
                ax.set_ylim([0, 1])
                ax.set_zlim([0, 1])
                
                # Set labels and title
                ax.set_xlabel(Df[ind_dic]['ins'][0])
                ax.set_ylabel(Df[ind_dic]['ins'][1])
                ax.set_zlabel(Df[ind_dic]['ins'][2])
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
    
    
    
    
    
    
    
