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
    