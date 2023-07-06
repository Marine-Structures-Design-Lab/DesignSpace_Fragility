"""
SUMMARY:

(May want to consider adding a StandardScalar from sklearn for x-input values)

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from sklearn.gaussian_process import GaussianProcessClassifier
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

"""
SECONDARY FUNCTIONS
"""
def check_classes(y):
    unique_classes = np.unique(y)
    if len(unique_classes) < 2:
        print("Insufficient unique classes in the data to train GPC.")
        return False
    else:
        return True


"""
CLASS
"""
class predictSpace:

    def __init__(self):
        self.model = GaussianProcessClassifier()
        return
    
    def trainFeasibility(self, x_train, y_train):
        if check_classes(y_train):
            self.model.fit(x_train, y_train)
            return True
        else:
            print("Training skipped due to insufficient unique classes.")
            return False
    
    def predictFeas(self, x_test):
        return self.model.predict(x_test)
    
    def predictProb(self, x):
        return self.model.predict_proba(x)
    
    def calcEntropy(self, pof):
        entropy = -pof[:,0]*np.log2(pof[:,0]) - pof[:,1]*np.log2(pof[:,1])
        return entropy
    
    def plotPoints(self, points, probs_and_colors, entropies, var, i, min_point_size=20, max_point_size=200):
        
        # Check that input arrays have compatible shapes
        assert points.shape[0] == probs_and_colors.shape[0] == entropies.shape[0]
        assert points.shape[1] == 3
        assert probs_and_colors.shape[1] == 2
        
        # Initialize an empty list for storing numpy arrays
        l = []
        
        # Surface plot
        j = np.linspace(0, 1, 4000)
        k = np.linspace(0, 1, 4000)
        j, k = np.meshgrid(j, k)
        
        if i == 0:
            l.append(0.8*j**2 + 2*k**2 - 0.0)
            l.append(0.8*j**2 + 2*k**2 - 0.4)
            l.append(0.8*j**2 + 2*k**2 - 1.2)
            l.append(0.8*j**2 + 2*k**2 - 1.6)
        elif i == 1:
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
        
        # Normalize the entropies so that they span the full range of sizes
        normalized_entropies = (entropies - np.min(entropies)) / np.ptp(entropies)
        sizes = min_point_size + normalized_entropies * (max_point_size - min_point_size)
    
        # Create a new figure
        fig = plt.figure()
    
        # Create a 3D axis
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot every surface
        for m in range(0,len(l)):
            ax.plot_surface(j, k, l[m], alpha=0.5, rstride=100, cstride=100)
    
        # Scatter plot: x, y, z coordinates are the columns of the 'points' array
        # Color ('c') is mapped to the second column of the 'probs_and_colors' array
        # Size ('s') is mapped to the 'sizes' array, scaled for better visibility
        sc = ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=probs_and_colors[:, 1], 
                        s=sizes, cmap='viridis', alpha=0.6)
        
        # Add a color bar
        cbar = plt.colorbar(sc)
        cbar.set_label('Probability')
    
        # Create a legend for sizes. Adjust values as needed
        min_entropy = np.min(entropies)
        max_entropy = np.max(entropies)
        for entropy in [min_entropy, (min_entropy + max_entropy) / 2, max_entropy]:
            plt.scatter([], [], c='k', alpha=0.3, s=min_point_size + ((entropy - min_entropy) / np.ptp(entropies)) * (max_point_size - min_point_size),
                        label="{:.2f}".format(entropy))
        plt.legend(scatterpoints=1, frameon=False,
                   labelspacing=1, title='Entropy')
        
        # Set axis limits
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])
        ax.set_zlim([0, 1])
        
        # Set labels
        ax.set_xlabel(var[0])
        ax.set_ylabel(var[1])
        ax.set_zlabel(var[2])
    
        plt.show()
        
        return
    