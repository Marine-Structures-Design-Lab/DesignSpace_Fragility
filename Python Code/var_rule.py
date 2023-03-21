# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 15:03:49 2023

@author: joeyv
"""
import sympy as sp


class varRule:
    
    def __init__(self,rule):
        self.r = rule #List, but possibly only one item
        return
    
    # Organize the variable string and return the sympified rule
    def breakup(self):
        
        # Create an empty list
        rule_list = []
        
        # Loop through each string of the rule
        for i in range(0,len(self.r)):
            
            # Split the rule at the comma delimiter to produce a list
            rule_list.append(self.r[i].split(','))
            
        # Sympify the list
        rule_list = sp.sympify(rule_list)
        
        # Return the sympified nested list of the particular rule
        return rule_list
    
    # Return the free symbols that the rule is concerned with
    def gather(self):
        
        # Code this in one function then move it to a separate function (not get
        # constraints) that is called
        
        
        
        
        return
    
    
    def evaluate(self):
        
        
        
        return #True or false