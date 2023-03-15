"""
SUMMARY:
Takes the calculated output values and assesses whether or not they meet the
current set of constraints/rules (should there be a difference between the
current set of rules as opposed to the original set of rules?).  If they do not
meet the rules, then it provides different methods for assessing the extent to
which this failure occurs.

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
class checkOutput:
    
    def __init__(self,discip,output_rules):
        self.d = discip
        self.outr = output_rules
        return
    
    # Only check whether the output points pass or fail
    def basicCheck(self):
        
        
        
        return