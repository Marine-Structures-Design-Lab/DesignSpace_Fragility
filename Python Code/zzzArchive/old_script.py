# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 15:08:09 2024

@author: joeyvan
"""

# Entropy KDE code (after universal space reductions)



##### ENTROPY-BASED #####
################################################################### MIGHT NOT NEED THIS FOR IMDC

# # Initialize an object for the distribution check class
# distribution = checkDistributions(Discips, KDE_data, joint_KDEs, \
#                          KDEs, posterior_KDEs, KL_divs)

# # Create data sets for calculating probability distributions
# KDE_data = distribution.createDataSets()

# # Calculate individual and joint KDEs
# KDEs, joint_KDEs = distribution.calcKDEs(KLgap)

# # Determine posterior KDEs with Bayes' Theorem
# posterior_KDEs = distribution.evalBayes()

# # Compute the KL divergence between successive posterior distributions
# KL_divs = distribution.computeKL()

# # Show the progression of KL divergence values as points are added
# distribution.plotKL()