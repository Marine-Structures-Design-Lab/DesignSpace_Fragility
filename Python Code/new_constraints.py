"""
SUMMARY:
[Summarize all three methods!]
Adds or updates rule(s) to the current set of rules as an object with a
character string parameter depending on if variables of the new rule(s) involve
all of the same variables as any of the current set of rules.

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
class newConstraints:
    
    def __init__(self,old_rules,new_rules):
        """
        Parameters
        ----------
        old_rules : TYPE
            DESCRIPTION.
        new_rules : TYPE
            DESCRIPTION.
        """
        self.old = old_rules
        self.new = new_rules
        return
    
    # The current method for identifying indices only works for rules that do
    # not involve coefficients in front of variables or more than one term in
    # the expression...might need to import real expressions library if I want
    # this to change...or just add each new rule as a brand spanking new rule!!!!!
    # Can still have and/or statement for the new rule where when it is multiple
    # strings separated by commas, only one of the strings within a single rule
    # needs to be true, but at least one string in each rule must be true!
    def getIndex(self):
        
        # Create empty list the same size as old rules for variable tracking
        old_vars = [None]*len(self.old)
        
        # Loop through the old rules
        for i in range(0,len(self.old)):
            
            # Break the old rule up into a sympified (nested) list
            temp_rule = self.old[i].breakup()
            
            # Collect the variables of the rule as a set for old variables list
            old_vars[i] = self.old[i].findVars(temp_rule)
            
        # Create empty list the same size as new rules for index tracking
        ind = [None]*len(self.new)
        
        # Loop through the new rules
        for i in range(0,len(self.new)):
            
            # Break the new rule up into a sympified (nested) list
            temp_rule = self.new[i].breakup()
            
            # Collect the variables of the rule as a set
            temp_set = self.new[i].findVars(temp_rule)
            
            # Loop through the variable sets of the old rules
            for j in range(0,len(old_vars)):
                
                # Check if the variables of the new rule align with an old rule
                if temp_set == old_vars[j]:
                    
                    # Collect index of old rule and break the loop
                    ind[i] = j
                    break
        
        # Return index list indicating how each new rule fits into old rules
        return ind
    
    def updateRules(self,ind):
        
        return
    
    def addRules(self,ind):
        
        # Loop through the new rule indices
        for i in range(0,len(ind)):
            
            # Execute following command if new rule index is of None type
            if ind[i] is None:
                
                # Append the new rule object to the old set of rules
                self.old.append(self.new[i])
        
        # Return the old (now updated) set of rules
        return self.old
