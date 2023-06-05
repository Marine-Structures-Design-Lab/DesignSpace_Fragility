"""
SUMMARY:
First merges the rule(s) being proposed by each discipline such that there are
no contradictions by removing any rules apart of a contradiction.  Dominance
will be saved for consideration in the fragility framework.  There is also
potential for adding a method that removes any redundancies in the new rules
being proposed or possibly in all of the rules up to this point if the Input
Rules list is passed as another argument.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import sympy as sp

"""
CLASS
"""
class mergeConstraints:
    
    def __init__(self,rules_new):
        """
        Parameters
        ----------
        rules_new : List
            Contains sympy Or relationals and/or inequalities for rules that
            only consist of one argument
        """
        self.rn = rules_new
        return
    
    
    def removeContradiction(self):
        """
        Description
        -----------
        Considers the independent rule (consisting of a single inequality or a
        sympy Or relational containing multiple inequalities) being proposed by
        one or more disciplines and merges them such that from the top-level,
        the rule(s) do not contradict each other
        
        Parameters
        ----------
        None.

        Returns
        -------
        noncon_rules : TYPE
            DESCRIPTION.
        """
        
        # Initialize a noncontradictory rule list
        noncon_rules = []
        
        # Loop through each new rule
        for i in range(0,len(self.rn)):
            
            # Set a boolean variable tracking contradiction to False
            is_contra = False
            
            # Loop through each new rule again
            for j in range(0,len(self.rn)):
                
                # Check that rules being checked for contradiction are not same
                if i != j:
                    
                    # Place rules inside a sympy And relational
                    contra = sp.And(self.rn[j], self.rn[i])
                    
                    # Check if simplified And relational evaluates to False
                    if sp.simplify(contra) == False:
                        
                        # Change contradiction variable to true and break loop
                        is_contra = True
                        break
            
            # Check if contradiction variable is still false
            if not is_contra:
                
                # Append the rule to the noncontradictory rule list
                noncon_rules.append(self.rn[i])
        
        # Return the noncontradictory rule list
        return noncon_rules
    
    
    
    
    # No 'Or' rule redundancies
    def removeRedundancy(self):
        # Do i only want to remove redundancies in the new rules?...or do i 
        # want to do the entire list of rules established thus far?
        
        return
    
    
def remove_redundancies(rules):
    non_redundant_rules = []
    for i in range(len(rules)):
        is_redundant = False
        for j in range(len(rules)):
            if i != j:
                implication = sp.Implies(rules[j], rules[i])
                if sp.simplify(implication) == True:
                    is_redundant = True
                    break
        if not is_redundant:
            non_redundant_rules.append(rules[i])
    return non_redundant_rules   
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    # No dominance until at least 50% of spaces have been eliminated
    ### One option is to have the requests pop up with stats and I decide
    ### Or program decides with stats
    ### Stats: How many disciplines are requesting what vs. the other
    ### How each side would be affected by the other discipline's proposal
    
    
    ### Could call a getInput method here...but not have it be a uniform method
    ### Could also do this for the fragility or other methods that may need to
    ### search points further
    
    
    