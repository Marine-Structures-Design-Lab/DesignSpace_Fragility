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
from dit import ScalarDistribution
from dit.other import generalized_cumulative_residual_entropy as gcre
from dit.other import cumulative_residual_entropy as cre
from windfall_regret import getIndices


"""
FUNCTION
"""
def initializePF(passfail, Discips_fragility):
    
    # Initialize dictionary of passfail predictions
    passfail_frag = {}
    
    # Loop through each instance of gathered pass-fail data
    for data in passfail:
        
        # Continue to next set of data if dictionary key is not None
        if None not in data: continue
        
        # Initialize an empty list for disciplines' data
        passfail_frag[data['time']] = []
        
        # Loop through each discipline's data
        for discip in data[None]:
            
            # Append discipline's data to the list - only append indices that still exist?
            passfail_frag[data['time']].append(discip['non_reduced'])
    
    # Identify the smallest key in the dictionary
    min_key = min(passfail_frag.keys())
    
    # Get the list of numpy arrays from the smallest key
    arrays = passfail_frag[min_key]
    
    # Create numpy arrays of zeros with matching sizes to smallest key
    new_arrays = [np.zeros_like(array) for array in arrays]
    
    # Add list of arrays to dictionary under key 0
    passfail_frag[0] = new_arrays
    
    # Return the consolidated sorted passfail data
    return passfail_frag


def timeHistory(Discips_fragility):
    
    # Initialize a list of passfail tracking lists for the disciplines
    passfail_frag = [[] for _ in Discips_fragility]
    
    # Loop through each discipline
    for i, discip in enumerate(Discips_fragility):
        
        # Loop over each row in the space remaining array
        for _ in range(0, discip['space_remaining'].shape[0]):
            
            # Append an empty numpy array to the inner list
            passfail_frag[i].append(np.array([]))
    
    # Return initalized lists ready to receive history of passfail values
    return passfail_frag




# THIS FUNCTION NEEDS TO HAVE SOME SORT OF SHAREDINDICES OR SOMETHING...SO
# THAT ONLY THE PROPER PF_OLD NUMPY ARRAY KEYS ARE BEING ASSIGNED TO PF_NEW
def reassignPF(pf_old, pf_new):
    
    # Sort the old passfail keys by their time values
    sorted_keys = sorted(pf_old.keys())
    
    # Loop through the list of sorted keys
    for time in sorted_keys:
        
        # Loop through each discipline
        for i, discip in enumerate(pf_old[time]):
            
            # Loop through discipline's passfail data at the current time stamp!!!!!!!!!!!!!!
            for index, value in enumerate(discip):
                
                # Append the data to the proper index in new passfail list
                pf_new[i][index] = np.append(pf_new[i][index], value)
        
    # Return the passfail list ready for TVE and DTVE evaluation
    return pf_new


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
                
                # Create empty dictionaries for discipline
                windreg[rule+tuple(irf)][ind_dic][ds] = {'TVE': np.array([], dtype=float), 'DTVE': np.array([], dtype=float)}
                run_wind[rule+tuple(irf)][ind_dic][ds] = {'TVE': 0.0, 'DTVE': 0.0}
                run_reg[rule+tuple(irf)][ind_dic][ds] = {'TVE': 0.0, 'DTVE': 0.0}
    
    # Return initialized dictionaries for windfall and regret tracking
    return windreg, run_wind, run_reg


def assignWR(tve, dtve, ind_pf, indices_in_both, pf):
    
    # Initialize empty dictionaries
    wr = {'non_reduced': {},
          'reduced': {},
          'leftover': {}}
    run_wind = {'non_reduced': {},
                'reduced': {}}
    run_reg = {'non_reduced': {},
               'reduced': {}}
    
    # Check if point is in both non-reduced and reduced matrices
    if ind_pf in indices_in_both:
        
        # Check if point predicted infeasible (windfall chance)
        if pf < 0:
            
            # Assign TVE and DTVE with proper sign
            wr['non_reduced']['TVE'] = tve
            wr['non_reduced']['DTVE'] = dtve
            wr['reduced']['TVE'] = tve
            wr['reduced']['DTVE'] = dtve
            
            # Assign to proper running windfall count
            run_wind['non_reduced']['TVE'] = tve
            run_wind['non_reduced']['DTVE'] = dtve
            run_wind['reduced']['TVE'] = tve
            run_wind['reduced']['DTVE'] = dtve
                        
        # Do below if point predicted feasible (regret chance)
        else:
                        
            # Assign TVE and DTVE with proper sign
            wr['non_reduced']['TVE'] = -tve
            wr['non_reduced']['DTVE'] = -dtve
            wr['reduced']['TVE'] = -tve
            wr['reduced']['DTVE'] = -dtve
            
            # Assign to proper running regret count
            run_reg['non_reduced']['TVE'] = tve
            run_reg['non_reduced']['DTVE'] = dtve
            run_reg['reduced']['TVE'] = tve
            run_reg['reduced']['DTVE'] = dtve
            
    # Do below if point is not in both non-reduced and reduced matrices
    else:
        
        # Check if point is predicted infeasible
        if pf < 0:
            
            # Assign complementary probability with proper sign
            wr['non_reduced']['TVE'] = tve
            wr['non_reduced']['DTVE'] = dtve
            wr['leftover']['TVE'] = -tve
            wr['leftover']['DTVE'] = -dtve
            
            # Assign to proper running windfall and regret counts
            run_wind['non_reduced']['TVE'] = tve
            run_wind['non_reduced']['DTVE'] = dtve
            run_reg['reduced']['TVE'] = tve
            run_reg['reduced']['DTVE'] = dtve
        
        # Do below if point is predicted feasible
        else:
                        
            # Assign complementary probability with proper sign
            wr['non_reduced']['TVE'] = -tve
            wr['non_reduced']['DTVE'] = -dtve
            wr['leftover']['TVE'] = tve
            wr['leftover']['DTVE'] = dtve
            
            # Assign to proper running windfall and regret counts
            run_reg['non_reduced']['TVE'] = tve
            run_reg['non_reduced']['DTVE'] = dtve
            run_wind['reduced']['TVE'] = tve
            run_wind['reduced']['DTVE'] = dtve
    
    # Return windfall and regret potentials
    return wr, run_wind, run_reg



"""
CLASS
"""
class entropyTracker:
    
    def __init__(self, passfail, Discips_fragility, irules_fragility):
        self.pf = passfail
        self.Df = Discips_fragility
        self.irf = irules_fragility
        return
    
    
    def prepEntropy(self):
        
        # Initialize an empty dictionary for consolidated passfail data
        passfail_frag1 = initializePF(self.pf, self.Df)
        
        # Initalize a list for time history of passfail values
        passfail_frag2 = timeHistory(self.Df)
        
        # Populate list with time history of passfail values
        passfail_frag2 = reassignPF(passfail_frag1, passfail_frag2)
        
        # Return each discipline's time history of passfail predictions for 
        # remaining design solutions in non-reduced design space
        return passfail_frag2
    
    
    def evalEntropy(self, passfail_frag):
        
        # Initialize empty TVE and DTVE lists
        TVE = [[] for _ in passfail_frag]
        DTVE = [[] for _ in passfail_frag]
        
        # Loop through each discipline
        for i, discip in enumerate(passfail_frag):
            
            # Loop through each history of data points' passfail predictions
            for index in discip:
                
                # Determine equal probability for each passfail prediction
                prob = 1 / len(index)
                
                # Create a scalar distribution for the data
                dist = ScalarDistribution({value: prob for value in index})
                
                # Calculate the TVE value
                tve = gcre(dist)
                
                # Append the TVE value to the inner TVE list
                TVE[i].append(tve)
                
                # Calculate the difference between consecutive predictions
                diffs = np.diff(index)
                
                # Determine new equal probability for each passfail prediction
                prob = 1 / len(diffs)
                
                # Create a scalar distribution for the difference data
                dist = ScalarDistribution({value: prob for value in diffs})
                
                # Calculate the DTVE value
                dtve = gcre(dist)
                
                # Append the DTVE value to the inner DTVE list
                DTVE[i].append(dtve)
        
        # Return TVE and DTVE values for each design point in non-reduced space remaining
        return TVE, DTVE
    
    
    
    def calcWindRegret(self, passfail, TVE, DTVE, pf_fragility):
        
        # Initialize empty dictionaries
        windreg, run_wind, run_reg = initializeWR(self.irf, passfail)
        
        # Loop through each new rule combo being proposed
        for rule, lis in passfail.items():
            
            # Loop through each discipline's passfail data
            for ind_dic, dic in enumerate(lis):
                
                # Create different index lists for input rule
                all_indices, indices_in_both, indices_not_in_B = \
                    getIndices(self.Df, self.irf, ind_dic, rule)
                
                # Loop through time history data of non-reduced design points
                for ind_pf, (tve, dtve) in enumerate(zip(TVE[ind_dic], DTVE[ind_dic])):
                    
                    # Gather windfall and regret potentials
                    wr, r_wind, r_reg = assignWR(tve, dtve, ind_pf, 
                        indices_in_both, pf_fragility[ind_dic][ind_pf])
                    
                    # Loop through each entropy dictionary in wr
                    for ds, entropies in wr.items():
                        
                        # Loop through TVE and DTVE entropies
                        for entr, val in entropies.items():
                        
                            # Append values to list of values of windreg key
                            windreg[rule+tuple(self.irf)][ind_dic][ds][entr] =\
                                np.append(windreg[rule+tuple(self.irf)]\
                                          [ind_dic][ds][entr], val)
                    
                    # Loop through each entropy dictionary in r_wind
                    for ds, entropies in r_wind.items():
                        
                        # Loop through TVE and DTVE entropies
                        for entr, val in entropies.items():
                            
                            # Add probability to proper running windfall sum
                            run_wind[rule+tuple(self.irf)][ind_dic][ds][entr] \
                                += r_wind[ds][entr]
                            
                    # Loop through each entropy dictionary in r_reg
                    for ds, entropies in r_reg.items():
                        
                        # Loop through TVE and DTVE entropies
                        for entr, val in entropies.items():
                            
                            # Add probability to proper running regret sum
                            run_reg[rule+tuple(self.irf)][ind_dic][ds][entr] \
                                += r_reg[ds][entr]
                    
                # Loop through each design space of discipline
                for ds in dic.keys():
                    
                    # Loop through each entropy type of the design space
                    for entr in run_wind[rule+tuple(self.irf)][ind_dic][ds].keys():
                        
                        # Divide probabilistic sums by remaining points
                        if self.Df[ind_dic]['space_remaining'].shape[0] > 0:
                            run_wind[rule+tuple(self.irf)][ind_dic][ds][entr] \
                                = run_wind[rule+tuple(self.irf)][ind_dic][ds][entr] / \
                                    self.Df[ind_dic]['space_remaining'].shape[0]
                            run_reg[rule+tuple(self.irf)][ind_dic][ds][entr] \
                                = run_reg[rule+tuple(self.irf)][ind_dic][ds][entr] / \
                                    self.Df[ind_dic]['space_remaining'].shape[0]
                        else:
                            run_wind[rule+tuple(self.irf)][ind_dic][ds][entr] = 0.0
                            run_reg[rule+tuple(self.irf)][ind_dic][ds][entr] = 0.0
        
        # Return windfall and regret data
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
            for ind_dic, (reg_dic, wind_dic) in enumerate(zip(run_reg[rule], 
                                                              run_wind[rule])):
                
                # Calculate non-reduced and reduced percentages
                nrp = round((windreg[rule][ind_dic]['non_reduced']['TVE'].shape[0] / \
                    self.Df[ind_dic]['tp_actual'])*100, 2)
                rp = round((windreg[rule][ind_dic]['reduced']['TVE'].shape[0] / \
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
                if abs(reg_dic['non_reduced']['TVE']) < 1e-10: 
                    reg_dic['non_reduced']['TVE'] +=1e-10
                reg_value = reg_dic['reduced']['TVE'] / reg_dic['non_reduced']['TVE'] - 1
                
                # Print the potential for regret results of space reduction
                print(f"Discipline {ind_dic+1} has {round(reg_value, 2)} added"
                      f" potential for regret.")
                
                # Replace regret value in risk dictionary
                risk[rule][ind_dic]['regret'] = reg_value
                
                
                ########## Windfall ##########
                
                # Calculate the potential for windfall for the space reduction
                ### + value indicates added potential for windfall
                ### - value indicates reduced potential for windfall
                if abs(wind_dic['non_reduced']['TVE']) < 1e-10: 
                    wind_dic['non_reduced']['TVE']+=1e-10
                wind_value = wind_dic['reduced']['TVE'] / wind_dic['non_reduced']['TVE'] - 1
                
                # Print the potential for windfal results of space reduction
                print(f"Discipline {ind_dic+1} has {round(wind_value, 2)} "
                      f"added potential for windfall.")
                
                # Replace windfall value in risk dictionary
                risk[rule][ind_dic]['windfall'] = wind_value
                
        # Return the dictionary for risk tracking
        return risk
    
    
    
    def plotWindRegret():
        # subplots of both the tve and dtve values right next to each other
        
        
        
        
        return
    
    
    

    
