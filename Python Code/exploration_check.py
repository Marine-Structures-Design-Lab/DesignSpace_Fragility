"""
SUMMARY:
Contains methods with different strategies for checking the design spaces of
each discipline, proposing space reductions, and potentially adjusting the
threshold of criteria that dictate whether a space reduction is ready to be
proposed.

i.e. clustering, rough sets

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from sklearn.cluster import KMeans

"""
CLASS
"""
# Have each discipline assess design space for potential space reductions
class checkSpace:
    
    # Initialize the class
    def __init__(self,force_reduction_counter,force_reduction_max):
        self.frc = force_reduction_counter
        self.frm = force_reduction_max
        return
    
    # Cluster data using RMS information
    def kmeansCluster(self):
        
        return
    
    
    
    
    
    
    
    
    
    
    # Cluster all data that has been explored
    ### Find centroid of clusters then create a best fit line between them?
    ### Create cluster groups for passing data sets and failing data sets that
    ### create these clusters based on how MUCH (variance) each set passes or fails
    
    
    # Print a graph of clustered data and centroids and zero/first/second order
    # lines that are dividing the clusters
    
    
    
    
    
    
    
    # Manual rule addition
    
    # Clustering for reduction propositions...turn clusters into first/second order
    # rules?
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # Loop through each discipline
    
    # Another method for setting the criteria for reducing a design space?
    
    # I need to run a separate clustering algorithm on groups of input data that
    ### definitely pass, kind of pass/fail, and definitely fail
    
    # Some sort of clustering algorithms that changes its parameter based on iterations
    ### and iterations that remain
    
    # Some sort of rough set theory algorithm?
    
    # Need to establish some sort of criteria for what is enough to actually propose a reduction
    
    # Return a list with None if no space reductions to propose
    
    # Another method in this class that is called if no reductions to determine
    # if design manager thinks it is necessary to actually have a reduction
    
    # Another method for reducing the criteria for a reduction
    
    