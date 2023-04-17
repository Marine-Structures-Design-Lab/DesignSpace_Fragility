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
import numpy as np
from sklearn.cluster import KMeans, SpectralClustering, AgglomerativeClustering

"""
CLASS
"""
# Have each discipline assess design space for potential space reductions
class checkSpace:
    
    # Initialize the class
    def __init__(self,Discips):
        self.d = Discips
        return
    
    # Cluster data using RMS information
    def variousClusters(self, n_clusters=2):
        
        # Create an empty list for clustered dictionaries of each dsicipline
        dict_clusters = [None]*len(self.d)
        
        # Loop through each discipline
        for i in range(0,len(self.d)):
            
            # Find indices of false values in the pass? list
            false_indices = np.where(np.array(self.d[i]['pass?']) == False)[0]
            
            # Isolate the data points corresponding to the false indices
            data_subset = self.d[i]['tested_outs'][false_indices]
            
            # Perform KMeans clustering on the subset of data points
            kmeans = KMeans(n_clusters=n_clusters)
            kmeans_labels = kmeans.fit_predict(data_subset)
            
            # Perform SpectralClustering on the subset of data points
            spectral = SpectralClustering(n_clusters=n_clusters)
            spectral_labels = spectral.fit_predict(data_subset)

            # Perform AgglomerativeClustering on the subset of data points
            agglomerative = AgglomerativeClustering(n_clusters=n_clusters)
            agglomerative_labels = agglomerative.fit_predict(data_subset)
            
            # Add key/value pairs to discipline's cluster dictionary
            dict_clusters[i] = {
                'KMeans': list(kmeans_labels),
                'SpectralClustering': list(spectral_labels),
                'AgglomerativeClustering': list(agglomerative_labels)
            }
        
        # Return a dictionary of the clustered results
        return dict_clusters

    
    
    
    
    
    
    
    
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
    
    