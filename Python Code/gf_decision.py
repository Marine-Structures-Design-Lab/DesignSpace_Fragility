"""
SUMMARY:


CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""

"""
FUNCTION
"""
def thresholdCheck(gf, threshold):
    
    if gf >= threshold:
        return True
    else:
        return False
    
    


"""
CLASS
"""
class gfDecider:
    
    def __init__(self, coefficients, gradient_factor, iters, iters_max):
        self.coeff = coefficients
        self.gf = gradient_factor
        self.it = iters
        self.itm = iters_max
        return
    
    
    def Fixed(self):
        
        threshold = self.coeff[0]
        
        return thresholdCheck(self.gf, threshold)
    
    
    def Linear(self):
        
        threshold = self.coeff[0]*(float(self.it)/float(self.itm)*100) + self.coeff[1]
        
        return thresholdCheck(self.gf, threshold)

    
    def Quadratic(self):
        
        threshold = self.coeff[0]*((float(self.it)/float(self.itm)*100) - self.coeff[1])**2 - self.coeff[2]
        
        return thresholdCheck(self.gf, threshold)
    
    
    
