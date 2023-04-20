"""
SUMMARY:
Takes class objects containing strings of various rules that disciplines need
to meet and converts these strings into actual sympy expressions and variable
sets that can be utilized.

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""
"""
LIBRARIES
"""
import sympy as sp
import re

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
    
    def findVars(self,rule):
        """
        Description
        -----------
        Determines all of the sympy variables that are prevalent in a
        particular nested rule
        
        Parameters
        ----------
        rule : Nested list of sympy expressions
            The list of expressions broken up from their strings and converted
            into sympy expressions
        
        Returns
        -------
        var_set : Set
            All of the sympy variables occurring in the nested rule
        """
        
        # Create a temporary empty set of variables
        var_set = set()
        
        # Loop through the nested rule list
        for i in range(0,len(rule)):
            for j in range(0,len(rule[i])):
                
                # Add variable(s) to the set if it does not already exist there
                var_set.update(rule[i][j].free_symbols)
        
        # Return the set of variables
        return var_set
    
    # Find the expressions(s) of each rule
    def findExpr(self):
        
        # Create an empty list
        expr_list = []
        
        # Loop through each string of the rule
        for i in range(0,len(self.r)):
            
            # Split the rule at the inequality symbol and take first string
            expr_list.append(re.split('>|<',self.r[i])[0])
        
        # Return the list of expressions
        return expr_list
    
    # Find the number(s) that the rule needs to meet
    def findNum(self):
        
        # Create empty lists for numbers and rules
        num_list = []
        rule_list = []
        
        # Loop through each string of the rule
        for i in range(0,len(self.r)):
            
            # Split rule at comma delimiter if it exists
            rule_list.append(self.r[i].split(','))
            
        # Loop through each "or" statement of the rule
        for i in range(0,len(rule_list)):
            
            # Initialize and inner rule list that is empty
            num_list_inner = []
            
            # Loop through each "and" statement of the rule
            for j in range(0,len(rule_list[i])):
                
                # Split the rule at the inequality symbols and take last string
                num_list_inner.append(re.split('>|<|=',rule_list[i][j])[-1])
                
            # Append the inner rule list to the nested rule list
            num_list.append(num_list_inner)
                
        # Return the list of numbers
        return num_list
    
