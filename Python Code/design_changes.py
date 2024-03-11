"""
SUMMARY:
Set up for SBD1 problem specifically!!!

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""



"""
CLASS
"""
class changeDesign:
    
    def __init__(self, Discips, Input_Rules, Output_Rules):
        """
        Parameters
        ----------
        Discips : Dictionary
            DESCRIPTION.
        Output_Rules : 
            DESCRIPTION
        """
        self.D = Discips
        self.In_Rules = Input_Rules
        self.Out_Rules = Output_Rules
        return
    
    
    # Addition or subtraction of any input variables for a discipline
    def Inputs(self):
        
        
        return self.D, self.In_Rules, self.Out_Rules
    
    
    # Changes to the analyses used to calculate output points from input points
    def Analyses(self):
        
        
        return self.D, self.In_Rules, self.Out_Rules
    
    
    # Addition or subtraction of any output variables for a discipline
    def Outputs(self):
        
        
        return self.D, self.In_Rules, self.Out_Rules
    
    
    # Changes to objective space requirements
    def Requirements(self):
        
        
        return self.D, self.In_Rules, self.Out_Rules
    
    
    # Reevaluate ALL previously explored points and update results...
    def reevaluatePoints(self):
        
        
        
        return self.D
    
    
    
