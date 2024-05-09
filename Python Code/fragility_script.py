"""
SUMMARY:
[Working through scripts for PFM and EFM]

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from windfall_regret import windfallRegret
from entropy_tracker import entropyTracker
from fragility_check import checkFragility
import copy



"""
CLASS
"""
class fragilityCommands:
    
    def __init__(self, Discips_fragility, irules_fragility, pf_combos,
                 pf_fragility, pf_std_fragility, passfail):
        self.Df = Discips_fragility
        self.irf = irules_fragility
        self.pf_combos = pf_combos
        self.pf_frag = pf_fragility
        self.pf_std_frag = pf_std_fragility
        self.pf = passfail
        return
    
    
    def PFM(self):
            
        # Initialize a windfall and regret object
        windregret = windfallRegret(self.Df, self.irf)
        
        # Calculate windfall and regret for remaining design spaces
        wr, run_wind, run_reg = windregret.calcWindRegret\
            (self.pf_combos, self.pf_frag, self.pf_std_frag)
        
        # Quantify risk or potential of space reduction
        ### Positive value means pot. regret or windfall ADDED
        ### Negative value means pot. regret or windfall REDUCED
        ris = windregret.quantRisk(run_wind, run_reg, wr)
        
        # Return the probability-based fragility results
        return wr, run_wind, run_reg, ris
    
    
    def EFM(self):
        
        # Initialize an entropy tracking object
        entropytrack = entropyTracker(self.pf, self.Df, self.irf)
        
        # Organize the history of recorded pass-fail data in non-reduced space
        passfail_frag = entropytrack.prepEntropy()
        
        # Evaluate the TVE and DTVE throughout remaining design spaces
        TVE, DTVE = entropytrack.evalEntropy(passfail_frag)
        
        # Calculate windfall and regret for remaining design spaces
        wr, run_wind, run_reg = entropytrack.calcWindRegret(self.pf_combos, 
                                                            TVE, DTVE, 
                                                            self.pf_frag)
        
        # Quantify risk or potential of space reduction -----------------------JUST USE WINDFALL_REGRETS????...but do not turn into a function because I may want new methods for doing the same thing at some point...
        ### Positive value means pot. regret or windfall ADDED
        ### Negative value means pot. regret or windfall REDUCED
        ris = entropytrack.quantRisk(run_wind, run_reg, wr)
        
        # Return the entropy-based fragility results
        return wr, run_wind, run_reg, ris, passfail_frag, TVE, DTVE
    
    
    def assessRisk(self, ris, iters, iters_max, exp_parameters, irules_new, 
                   fragility_shift, banned_rules, windreg, wr, 
                   running_windfall, run_wind, running_regret, run_reg, risk):
        
        # Initialize a fragility check object
        fragile = checkFragility(ris)
        
        # Execute fragility assessment
        net_wr = fragile.basicCheck(iters, iters_max, exp_parameters, 
                                    fragility_shift)
        
        # Indicate that the fragility loop should not be broken
        break_loop = False

        # Check if ANY rule combos do not lead to fragile space
        if any(dic["fragile"] == False for dic in net_wr.values()):
            
            # Select rule combination to move forward with and add
            # to banned rule set
            final_combo, banned_rules = \
                fragile.newCombo(net_wr, banned_rules)
            
            # Append all findings to the list of dictionaries
            windreg.append(copy.deepcopy\
                ({final_combo: wr[final_combo]}))
            running_windfall.append(copy.deepcopy\
                ({final_combo: run_wind[final_combo]}))
            running_regret.append(copy.deepcopy\
                ({final_combo: run_reg[final_combo]}))
            risk.append(copy.deepcopy\
                ({final_combo: ris[final_combo]}))
            
            # Plot the potential for windfall and regret throughout each 
            # discipline's design space for the final combo
            # windregret = windfallRegret(self.Df, self.irf)
            # windregret.plotWindRegret({final_combo: wr[final_combo]})
                
            # Append time to the dictionaries
            windreg[-1]['time'] = iters
            running_windfall[-1]['time'] = iters
            running_regret[-1]['time'] = iters
            risk[-1]['time'] = iters
            
            # Reassign NEW input rules as the items in the final combo
            irules_new = list(set(final_combo) ^ set(self.irf))
            
            # Add new input rules to the list of the current time stamp
            self.irf += irules_new
            
            # Indicate that the fragility loop should be broken
            break_loop = True
        
        # Return the documented fragility results (AM I SURE I DO NOT NEED TO RETURN net_wr, final_combo????)
        return banned_rules, windreg, running_windfall, running_regret, risk, \
            irules_new, self.irf, break_loop