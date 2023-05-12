# -*- coding: utf-8 -*-
"""
Created on Fri May 12 13:07:11 2023

@author: joeyv
"""

import numpy as np
import sympy as sp
from sklearn.cluster import KMeans, SpectralClustering, AgglomerativeClustering

class checkSpace2:
    
    # Initialize the class
    def __init__(self,Discips):
        self.d = Discips
        return
    
    
    def createClusters(self,n_clusters=2):
        
        # Establish type of clustering methods
        label_names = ['KMeans Clustering',
                       'Spectral Clustering',
                       'Agglomerative Clustering']
        
        # Create an empty list for each type of clustering method
        labels = [None]*len(label_names)
        
        # Loop through each discipline
        for i in range(0,len(self.d)):
            
            # Reshape the failure amount data
            data = np.reshape(self.d[i]['Fail_Amount'],(-1,1))
            
            # Append the failure amount data to the tested input data
            data = np.hstack((self.d[i]['tested_outs'],data))
            
            # Perform KMeans clustering on the dataset
            kmeans = KMeans(n_clusters=n_clusters)
            labels[0] = kmeans.fit_predict(data)
            
            # Perform Spectral clustering on the dataset
            spectral = SpectralClustering(n_clusters=n_clusters)
            labels[1] = spectral.fit_predict(data)
    
            # Perform Agglomerative clustering on the dataset
            agglomerative = AgglomerativeClustering(n_clusters=n_clusters)
            labels[2] = agglomerative.fit_predict(data)
            
            # Add key/value pairs to cluster dictionary
            dict_clusters = {
                'KMeans': list(labels[0]),
                'Spectral': list(labels[1]),
                'Agglomerative': list(labels[2])
            }
            
            # Add clustered dictionary to the discipline
            self.d[i]['Clusters'] = dict_clusters
        
        # Return updated discipline with clustered data
        return self.d
    
    
    
    # Partition the design space for possible space reductions
    def getPartitions2(self):
        # Create an empty list the same length as the disciplines
        ineq_list = [None] * len(self.d)
    
        # Loop through each discipline
        for i in range(0, len(self.d)):
            
            # Create a nested list within the discipline the same length as the input variables
            ineq_list[i] = [None] * len(self.d[i]['ins'])
    
            # Loop through each input variable of the discipline
            for var in self.d[i]['ins']:
                threshold = None
                max_sum = -np.inf
    
                # Convert input points to a numpy array
                tested_ins = np.array(self.d[i]['tested_ins'])
    
                # Loop through each input point of the discipline
                for j, point in enumerate(tested_ins):
                    if not self.d[i]['pass?'][j]:
                        temp_threshold = point[self.d[i]['ins'].index(var)]
                        mask = tested_ins[:, self.d[i]['ins'].index(var)] > temp_threshold
                        temp_list = np.array(self.d[i]['pass?'])[mask]
                        temp_failures = np.array(self.d[i]['Fail_Amount'])[mask]
    
                        if not any(temp_list) and sum(temp_failures) > max_sum:
                            max_sum = sum(temp_failures)
                            threshold = temp_threshold
    
                inequality = sp.Gt(var, threshold)
                if inequality == NotImplemented:
                    inequality = None
    
                # Add inequality to list
                ineq_list[i][self.d[i]['ins'].index(var)] = inequality
    
        return ineq_list
    
    
            
        
        
        
        
        
        
        
        # What is needed to go through with a reduction after partition(s) found:
            # - Kernel density function does not fall below a certain value in that space
            # - Less than a certain percentage of successful points are found in that space