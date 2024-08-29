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
TERTIARY FUNCTIONS
"""
def createBins(Df, indices_rem, total_points):
    """
    Description
    -----------
    Creates unique bins for the space remaining points of a particular subspace
    being assessed.

    Parameters
    ----------
    Df : Dictionary
        All information pertaining to a discipline at the beginning of the
        newest space reduction cycle
    indices_rem : List of integers
        Indices of the design variables for the subspace being assessed
    total_points : Integer
        Total number of space remaining points created at the beginning of the
        simulation

    Returns
    -------
    unique_bins : Numpy array (2D)
        Integer value labels for unique bins in each dimension of the subspace
        for each remaining design point
    inverse_indices : Numpy array (1D)
        Integer value labels corresponding to each unique bin for each
        remaining design point
    """
    
    # Extract the relevant subspaces of data remaining
    subset_data_rem = Df['space_remaining'][:, indices_rem]
    
    # Calculate the max number of space remaining points in each dimension
    npoints_dim = int(round(total_points ** (1. / len(Df['ins']))))
    
    # Generate evenly spaced points between 0 and 1
    points = np.linspace(0, 1, npoints_dim)
    
    # Create bin edges by finding midpoints between the points
    midpoints = (points[:-1] + points[1:]) / 2
    
    # Create the bin edges with -∞ for the leftmost and +∞ for the rightmost
    b_edges = np.concatenate(([-np.inf], midpoints, [np.inf]))
    
    # Return the same bin edges for all dimensions
    bin_edges = [b_edges] * len(indices_rem)
    
    # Initialize a numpy array for bin indices
    bin_indices = np.zeros_like(subset_data_rem, dtype=int)
    
    # Loop through each dimension remaining
    for dim in range(0, len(indices_rem)):
        
        # Determine which bin each consolidated data point will fall in
        bin_indices[:, dim] = \
            np.digitize(subset_data_rem[:, dim], bins=bin_edges[dim]) - 1
        
    # Find unique bins and corresponding indices
    unique_bins, inverse_indices = np.unique(bin_indices, axis=0, 
                                             return_inverse=True)
    
    # Return the list of bin edges
    return unique_bins, inverse_indices


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
        All information pertaining to each discipline at the beginning of the
        newest space reduction cycle

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
            
            # Loop through the discipline's subspace dimensions (default is to
            # not assess fragility of any subspaces)
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
                
                # Initialize empty arrays for windfall-regret
                windreg[rule_key][ind_dic][ds]=np.array([], dtype=float)
                
                # Continue to next design space if "leftover"
                if ds == "leftover": continue
                
                # Initialize empty values for running regret and windfall
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


def assignWR(prob_tve, indices_in_both, pf, windreg):
    """
    Description
    -----------
    Prepares complementary probability of feasiblity or TVE for assignment to
    windfall and regret dictionaries based on initially formed perceptions of 
    feasiblity and design spaces in which a point falls.

    Parameters
    ----------
    prob_tve : Numpy array
        Complementary probabilities of feasibility or TVEs for discipline
    indices_in_both : List
        Indices of points in both the non-reduced and reduced data arrays
    pf : Numpy array
        Predicted pass-fail amounts from the non-reduced design space
    windreg : Dictionary
        Empty numpy arrays for each design space of rule for a discipline

    Returns
    -------
    windreg : Dictionary
        Potentials for regret or windfall of the non-reduced design space and
        the reduced or leftover design space with proper signage
    run_wind : List of dictionaries
        Newest contributions to running windfall totals of the non-reduced and
        reduced design spaces
    run_reg : List of dictionaries
        Newest contributions to running regret totals of the non-reduced and
        reduced design spaces
    """
    
    # Initialize empty list of dictionaries
    run_wind = [{} for _ in prob_tve]
    run_reg = [{} for _ in prob_tve]
    
    # Loop through each complementary probability or TVE value
    for ind_pf, p_tve in enumerate(prob_tve):
        
        # Check if point is in both non-reduced and reduced matrices
        if ind_pf in indices_in_both:
            
            # Check if point predicted infeasible (windfall chance)
            if pf[ind_pf] < 0:
                
                # Assign complementary probability or TVE with proper sign
                windreg['non_reduced']=np.append(windreg['non_reduced'],p_tve)
                windreg['reduced']=np.append(windreg['reduced'],p_tve)
                
                # Assign to proper running windfall count
                run_wind[ind_pf]['non_reduced'] = p_tve
                run_wind[ind_pf]['reduced'] = p_tve
                            
            # Do below if point predicted feasible (regret chance)
            else:
                            
                # Assign complementary probability or TVE with proper sign
                windreg['non_reduced']=np.append(windreg['non_reduced'],-p_tve)
                windreg['reduced'] = np.append(windreg['reduced'], -p_tve)
                
                # Assign to proper running regret count
                run_reg[ind_pf]['non_reduced'] = p_tve
                run_reg[ind_pf]['reduced'] = p_tve
                
        # Do below if point is not in both non-reduced and reduced matrices
        else:
            
            # Check if point is predicted infeasible
            if pf[ind_pf] < 0:
                
                # Assign complementary probability or TVE with proper sign
                windreg['non_reduced']=np.append(windreg['non_reduced'],p_tve)
                windreg['leftover'] = np.append(windreg['leftover'], -p_tve)
                
                # Assign to proper running windfall and regret counts
                run_wind[ind_pf]['non_reduced'] = p_tve
                run_reg[ind_pf]['reduced'] = p_tve
            
            # Do below if point is predicted feasible
            else:
                            
                # Assign complementary probability or TVE with proper sign
                windreg['non_reduced']=np.append(windreg['non_reduced'],-p_tve)
                windreg['leftover'] = np.append(windreg['leftover'], p_tve)
                
                # Assign to proper running windfall and regret counts
                run_reg[ind_pf]['non_reduced'] = p_tve
                run_wind[ind_pf]['reduced'] = p_tve
    
    # Return discipline's complementary probability or TVE dictionaries
    return windreg, run_wind, run_reg


def averageWR(r_WorR, combo, Df, run_WorR, total_points):
    """
    Description
    -----------
    Consolidates regret or windfall data into the subspace being assessed and
    then sums the averages within the subspace.
    
    Parameters
    ----------
    r_WorR : ist of dictionaries
        Newest contributions to running windfall or running regret totals of 
        the non-reduced and reduced design spaces
    combo : Tuple of sympy variables
        The design variables making up the subspace being assessed
    Df : Dictionary
        All information pertaining to a discipline at the beginning of the
        newest space reduction cycle
    run_WorR : Dictionary
        Initialized regret or windfall potential in remaining design spaces for
        for all the rules proposed in the current time stamp
    total_points : Integer
        Total number of space remaining points created at the beginning of the
        simulation

    Returns
    -------
    run_WorR : Dictionary
        Sum of regret or windfall potential in remaining design spaces for all
        of the rules proposed in the current time stamp
    """
    
    # Determine the dimensions of the (sub)space being assessed
    indices_rem = [Df['ins'].index(symbol) for symbol in combo]
    
    # Check if index list is as long as the discipline's design variable list
    if len(indices_rem) >= len(Df['ins']):
        
        # Loop through each point contributing to the sum
        for diction in r_WorR:
            
            # Loop through each design space
            for ds in run_WorR:
                
                # Add to running total if point has regret or windfall amount
                if ds in diction: run_WorR[ds] += diction[ds]
    
    # Perform the following commands for the subspace
    else:
            
        # Find unique bins and corresponding indices
        unique_bins, inverse_indices = createBins(Df,indices_rem,total_points)
        
        # Initialize 0.0 values for first averages
        first_averages = {
            "non_reduced": np.zeros(len(unique_bins)),
            "reduced": np.zeros(len(unique_bins))
        }
        
        # Loop through each unique bin
        for bin_index in range(0, len(unique_bins)):
            
            # Initialize a counting variable for first average
            count = 0
            
            # Extract the subset that corresponds to the current bin
            selected_indices = np.where(inverse_indices == bin_index)[0]
            selected_r_WorR = [r_WorR[i] for i in selected_indices]
            
            # Loop through each point contributing to first average
            for diction in selected_r_WorR:
                
                # Loop through each design space
                for ds in run_WorR:
                    
                    # Add to running total if point has regret or windfall
                    if ds in diction: first_averages[ds][bin_index] += \
                        diction[ds]
                
                # Add 1 to the count
                count += 1
            
            # Loop through each design space
            for ds in run_WorR:
                
                # Divide first average sums by counting variable
                if count > 0:
                    first_averages[ds][bin_index] = \
                        first_averages[ds][bin_index] / count
                else:
                    first_averages[ds][bin_index] = 0.0
        
        # Loop through each design space
        for ds in run_WorR:
            
            # Determine regret or windfall sums of the subspace
            run_WorR[ds] = np.sum(first_averages[ds])
    
    # Return design subspace average
    return run_WorR
    
    
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


def calcWindRegret(irf, Df, passfail, prob_tve, pf_fragility, frag_ext,
                   total_points):
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
    total_points : Integer
        An approximate total number of evenly spaced points the user
        desires for tracking the space remaining in a discipline's design
        space
    
    Returns
    -------
    windreg : Dictionary
        Windfall and regret data for each discretized point remaining in
        the non-reduced, reduced, and leftover design spaces of each 
        discipline for all of the rules proposed in the current time stamp
    run_wind : Dictionary
        Sum of windfall potential in remaining design spaces for all of the
        rules proposed in the current time stamp
    run_reg : Dictionary
        Sum of regret potential in remaining design spaces for all of the rules
        proposed in the current time stamp
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
            
            # Prepare complementary probabilities or TVEs for assignments
            windreg[rule_key][ind_dic], r_wind, r_reg = \
                assignWR(prob_tve[ind_dic], indices_in_both, 
                         pf_fragility[ind_dic], windreg[rule_key][ind_dic])
            
            # Loop through each subspace being assessed
            for combo, des_spaces in run_wind[rule_key][ind_dic].items():
            
                # Determine average potential for windfall for subspace
                run_wind[rule_key][ind_dic][combo] = \
                    averageWR(r_wind, combo, Df[ind_dic], 
                              run_wind[rule_key][ind_dic][combo],
                              total_points)
                
                # Determine average potential for regret for subspace
                run_reg[rule_key][ind_dic][combo] = \
                    averageWR(r_reg, combo, Df[ind_dic],
                              run_reg[rule_key][ind_dic][combo],
                              total_points)
                
    # Returning average windfall and regret information for new rule(s)
    return windreg, run_wind, run_reg


def quantRisk(Df, run_wind, run_reg, windreg):
    """
    Description
    -----------
    Determines the amount of space that would remain in each discipline
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
        
        # Add a rule key with a list of empty dictionaries for each discipline
        risk[rule] = [{} for _ in lis]
        
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
            
            # Loop through each subspace being assessed
            for combo, des_spaces in run_wind[rule][ind_dic].items():
                
                ########## Regret and Windfall ##########
                
                # Create an empty dictionary for regret and windfall tracking
                risk[rule][ind_dic][combo] = {
                    "regret" : None, 
                    "windfall" : None
                }
                
                ########## Regret ##########
                
                # Calculate the potential for regret for the space reduction
                ### + value indicates added potential for regret
                ### - value indicates reduced potential for regret
                reg_value = reg_dic[combo]['reduced'] / \
                    reg_dic[combo]['non_reduced'] - 1 \
                    if reg_dic[combo]['non_reduced'] != 0 else 0.0
                
                # Replace regret value in risk dictionary
                risk[rule][ind_dic][combo]['regret'] = reg_value
                
                ########## Windfall ##########
                
                # Calculate the potential for windfall for the space reduction
                ### + value indicates added potential for windfall
                ### - value indicates reduced potential for windfall
                wind_value = wind_dic[combo]['reduced'] / \
                    wind_dic[combo]['non_reduced'] - 1\
                    if wind_dic[combo]['non_reduced'] != 0 else 0.0
                
                # Replace windfall value in risk dictionary
                risk[rule][ind_dic][combo]['windfall'] = wind_value
            
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
    
    
    
    
    
    
    
