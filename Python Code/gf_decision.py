"""
SUMMARY:
Makes the decision on whether the gathered gradient factor value is high enough
to implement a space reduction decision based on the chosen user decision
strategy.

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
    """
    Description
    -----------
    Determines whether the gradient factor value exceeds the decision 
    threshold.

    Parameters
    ----------
    gf : Float
        Gathered gradient factor value of the space reduction proposed
    threshold : Float
        Minimum gradient factor value for which it is okay to implement a space
        reduction

    Returns
    -------
    True or False
        Whether it is okay to implement a space reduction (True) or not (False)
    """
    
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
        """
        Parameters
        ----------
        coefficients : List of floats
            The chosen user inputs that descirbe the equation used for setting
            the threshold of gradient factor decision strategy
        gradient_factor : Float
            Gathered gradient factor value of the space reduction proposed
        iters : Integer
            Current time iteration of the SBD simulation
        iters_max : Integer
            Total amount of time iterations allotted to the SBD simulation
        """
        return
    
    
    def Fixed(self):
        """
        Description
        -----------
        Sets a fixed value for the minimum gradient factor threshold.

        Returns
        -------
        True or False
            Whether it is okay to implement a space reduction (True) or not 
            (False)
        """
        
        # Set the fixed value of the threshold
        threshold = self.coeff[0]
        
        # Check whether the gradient factor exceeds the threshold
        return thresholdCheck(self.gf, threshold)
    
    
    def Linear(self):
        """
        Description
        -----------
        Sets a linear equation for the minimum gradient factor threshold.

        Returns
        -------
        True or False
            Whether it is okay to implement a space reduction (True) or not 
            (False)
        """
        
        # Set the linear equation for the threshold
        threshold = self.coeff[0]*(float(self.it)/float(self.itm)*100) \
            + self.coeff[1]
        
        # Check whether the gradient factor exceeds the threshold
        return thresholdCheck(self.gf, threshold)

    
    def Quadratic(self):
        """
        Description
        -----------
        Sets a quadratic equation for the minimum gradient factor threshold.

        Returns
        -------
        True or False
            Whether it is okay to implement a space reduction (True) or not 
            (False)
        """
        
        # Set the quadratic equation for the threshold
        threshold = self.coeff[0]*((float(self.it)/float(self.itm)*100) \
                                   - self.coeff[1])**2 - self.coeff[2]
        
        # Check whether the gradient factor exceeds the threshold
        return thresholdCheck(self.gf, threshold)
    
    
