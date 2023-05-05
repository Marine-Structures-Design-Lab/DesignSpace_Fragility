"""
SUMMARY:
Contains methods with different logic and calculations for determining the
amount of time (iterations) that each discipline should take to explore their
design space before reconsidering potential space reductions.

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
class exploreSpace:
    
    def __init__(self,iters,iters_max,run_time):
        """
        Parameters
        ----------
        iters : Integer
            The amount of time iterations that have been completed for the
            design problem thus far
        iters_max : Integer
            The amount of time iterations that the design problem will last for
        run_time : List of integers
            The amount of time iterations that each discipline's analysis takes
            to execute
        """
        self.it = iters
        self.itm = iters_max
        self.rt = run_time
        return
    
    def fixedExplore(self):
        """
        Description
        -----------
        Commits a fixed amount of time for exploration based on the time that
        remains
        
        Parameters
        ----------
        None.
        
        Returns
        -------
        "Exploration time" : Integer
            The amount of time iterations to commit to exploration at the
            particular moment in time that is based on the time remaining in
            the project and the amount of time it takes each discipline to
            execute its analysis
        """
        
        # Calculate the time remaining
        time_rem = self.itm - self.it
        
        # Fixed if statements for exploration time based on time remaining
        ### Welcome to add to, eliminate, or manipulate these as desired
        if self.it < 0.2*self.itm:
            return max(int(0.20*time_rem),min(time_rem,max(self.rt)))
        elif self.it < 0.35*self.itm:
            return max(int(0.18*time_rem),min(time_rem,max(self.rt)))
        elif self.it < 0.5*self.itm:
            return max(int(0.15*time_rem),min(time_rem,max(self.rt)))
        elif self.it < 0.6*self.itm:
            return max(int(0.12*time_rem),min(time_rem,max(self.rt)))
        elif self.it < 0.7*self.itm:
            return max(int(0.10*time_rem),min(time_rem,max(self.rt)))
        elif self.it < 0.8*self.itm:
            return max(int(0.07*time_rem),min(time_rem,max(self.rt)))
        elif self.it < 0.9*self.itm:
            return max(int(0.04*time_rem),min(time_rem,max(self.rt)))
        else:
            return min(time_rem,max(self.rt))
