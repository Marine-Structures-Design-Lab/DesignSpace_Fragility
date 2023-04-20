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
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, SpectralClustering, AgglomerativeClustering
from sklearn.decomposition import PCA

"""
CLASS
"""
# Have each discipline assess design space for potential space reductions
class checkSpace:
    
    # Initialize the class
    def __init__(self,Discips):
        self.d = Discips
        return
    
    def createClusters(self, n_clusters=2):
        """
        Clusters the data in a dictionary using various clustering methods,
        excluding the rows that have a True value in the corresponding index
        of the mask list. The clustered data is then reduced to 2 dimensions
        using PCA, and plotted on a 2D scatter plot with the color of the points
        indicating the cluster label. FIX THIS

        Parameters:
        data_dict (dict): A dictionary containing the data and mask arrays.
        data_key (str): The key in the dictionary corresponding to the data array.
        mask_key (str): The key in the dictionary corresponding to the mask list.

        Returns:
        None
        """
        
        # Create an empty list for clustered dictionaries of each dsicipline
        dict_clusters = [None]*len(self.d)
        
        # Establish type of clustering methods
        label_names = ['KMeans Clustering',
                       'Spectral Clustering',
                       'Agglomerative Clustering']
        
        # Create an empty list for each type of clustering method
        labels = [None]*len(label_names)
        
        # Loop through each discipline
        for i in range(0,len(self.d)):
            
            # Find indices of false values in the pass? list
            false_indices = np.where(np.array(self.d[i]['pass?']) == False)[0]
            
            # Isolate the data points corresponding to the false indices
            data_subset = self.d[i]['tested_outs'][false_indices]
            data_subset_in = self.d[i]['tested_ins'][false_indices]
            
            # Reduce the dimensionality of the data (if necessary)
            if np.shape(self.d[i]['tested_outs'])[1] > 2:
                pca = PCA(n_components=2)
                reduced_data = pca.fit_transform(data_subset)
            else:
                reduced_data = data_subset
            reduced_data_in = data_subset_in
            
            # Perform KMeans clustering on the subset of data points
            kmeans = KMeans(n_clusters=n_clusters)
            labels[0] = kmeans.fit_predict(data_subset)
            
            # Perform SpectralClustering on the subset of data points
            spectral = SpectralClustering(n_clusters=n_clusters)
            labels[1] = spectral.fit_predict(data_subset)

            # Perform AgglomerativeClustering on the subset of data points
            agglomerative = AgglomerativeClustering(n_clusters=n_clusters)
            labels[2] = agglomerative.fit_predict(data_subset)
            
            # Add key/value pairs to discipline's cluster dictionary
            dict_clusters[i] = {
                'KMeans': list(labels[0]),
                'SpectralClustering': list(labels[1]),
                'AgglomerativeClustering': list(labels[2])
            }
            
            # Loop through each clustering method
            for j in range(0,len(labels)):
                
                # Graph in the objective space...add objective rules as lines?
                if np.shape(self.d[i]['tested_outs'])[1] >= 2:
                    fig, ax = plt.subplots(figsize=(8, 6))
                    ax.scatter(reduced_data[:, 0], reduced_data[:, 1], c=labels[j], cmap='nipy_spectral', label=label_names[j])
                    if np.shape(self.d[i]['tested_outs'])[1] == 2:
                        ax.set_xlabel(self.d[i]['outs'][0], fontsize=12)
                        ax.set_ylabel(self.d[i]['outs'][1], fontsize=12)
                    else:
                        ax.set_xlabel('PC1', fontsize=12)
                        ax.set_ylabel('PC2', fontsize=12)
                    plt.tick_params(axis='x', which='major', labelsize=12)
                    plt.tick_params(axis='y', which='major', labelsize=12)
                else:
                    fig, ax = plt.subplots(figsize=(8, 2))
                    ax.scatter(reduced_data[:, 0], np.zeros_like(reduced_data[:, 0]), c=labels[j], cmap='nipy_spectral', label=label_names[j])
                    plt.gca().axes.get_yaxis().set_visible(False)
                    ax.set_xlabel(self.d[i]['outs'][0], fontsize=12)
                    plt.tick_params(axis='x', which='major', labelsize=12)
                
                plt.grid(True)
                plt.title("Discipline "+str(i+1)+" Failed Outputs - "+label_names[j])
                plt.show()
                
                # Graph in the input space - Need to adjust above for 3D space
                # and have scatter plot 1 2 or 3 depend on the data provided - Check that axis labels are correct for each discipline
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')
                ax.scatter(reduced_data_in[:, 0], reduced_data_in[:, 1], reduced_data_in[:,2], c=labels[j], cmap='nipy_spectral', label=label_names[j])
                ax.set_xlabel(self.d[i]['ins'][0], fontsize=12)
                ax.set_ylabel(self.d[i]['ins'][1], fontsize=12)
                ax.set_zlabel(self.d[i]['ins'][2], fontsize=12)
                plt.grid(True)
                plt.title("Discipline "+str(i+1)+" Failed Inputs - "+label_names[j])
        
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
    
    