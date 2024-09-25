"""
SUMMARY:


CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from fragility_script import fragilityCommands



"""
FUNCTIONS
"""
def optimizeGradientFactor():
    
    gradient_factor = 0.1
    
    return gradient_factor








# Establish an initial gradient factor value
gradient_factor = 0.1



################## LOOP BEGIN

# Determine new pass-fail values for worst-case scenario --- STILL NEED TO DO THIS!
pf_fragility_new = pf_fragility

# Initalize new fragility assessment object
fragnalysis = fragilityCommands(Discips_fragility, 
    irules_fragility, pf_combos, pf_fragility_new,
    pf_std_fragility, passfail, passfail_std, 
    fragility_extensions, total_points)

# Perform desired fragility assessment
wr, run_wind, run_reg, ris = \
    getattr(fragnalysis, fragility_type)()

# Assess risk from fragility assessment
_, _, _, _, _, _, _, _, net_wr = fragnalysis.assessRisk(ris, iters, iters_max,
    exp_parameters, irules_new, fragility_shift, banned_rules, windreg, wr, 
    running_windfall, run_wind, running_regret, run_reg, risk)

# Determine the added risk robustness
### NOTE: ONLY WORKS WITH basicCheck2 IN fragility_script
risk_rob = fragnalysis.assessRobustness(net_wr)

# Check if added risk robustness is about 0


# If yes, repeat everything after gradient calculation / initial prediction with an updated gradient_factor


# If no, return the gradient_factor