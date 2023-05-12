"""
SUMMARY:


CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#from sklearn.decomposition import PCA


"""
FUNCTIONS
"""

def graphClusters(Discips):
    
    # Loop through each discipline
    for i in range(0,len(Discips)):
        
        # Loop through each clustering method
        for key in Discips[i]['Clusters']:
            
            # Graph clustered data points in the input space
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            sc = ax.scatter(Discips[i]['tested_ins'][:,0],\
                       Discips[i]['tested_ins'][:,1],\
                       Discips[i]['tested_ins'][:,2],\
                       c=Discips[i]['Clusters'][key],\
                       cmap='nipy_spectral', label=key, s=100)
            ax.set_xlabel(Discips[i]['ins'][0])
            ax.set_ylabel(Discips[i]['ins'][1])
            ax.set_zlabel(Discips[i]['ins'][2])
            plt.grid(True)
            plt.title("Discipline "+str(i+1)+" Inputs - "+key)
            #cbar = plt.colorbar(sc)
            #cbar.ax.set_ylabel('Cluster')
            plt.show()
            
            
            
            # Graph clustered data points in the output space
    
    
    
    return