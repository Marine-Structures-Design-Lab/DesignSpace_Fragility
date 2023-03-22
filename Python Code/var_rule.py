"""
SUMMARY:
Takes class objects containing strings of various rules that disciplines need
to meet and converts these strings into actually sympy expressions that can be 
utilized.  Consider adding other methods for gathering the variables and/or
evaluating the rules!

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
class varRule:
    
    def __init__(self,rule):
        """
        Parameters
        ----------
        rule : List of strings
            Must always be in list while containing one or more strings as
            items.  Commas within a single string act as delimters for multiple
            rules that must abide by an "and" statement.  Rules in separate
            strings within the list must only abide by an "or" statement.
        """
        self.r = rule
        return
    
    # Organize the variable string and return the sympified rule
    def breakup(self):
        """
        Description
        -----------
        Break up the rule string as different items in various nested lists
        depending on if the rules involved must both be true or individually
        true
        
        Parameters
        ----------
        None.

        Returns
        -------
        rule_list : Nested list of sympy expressions
            The list of expressions broken up from their strings and converted
            into sympy expressions
        """
        
        # Create an empty list
        rule_list = []
        
        # Loop through each string of the rule
        for i in range(0,len(self.r)):
            
            # Split the rule at the comma delimiter to produce a list
            rule_list.append(self.r[i].split(','))
            
        # Sympify the entire list
        rule_list = sp.sympify(rule_list)
        
        # Return the sympified (nested) list of the particular rule
        return rule_list
