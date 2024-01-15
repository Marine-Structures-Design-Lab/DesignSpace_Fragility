"""
Archived code from merge_constraints

@author: joeyvan
"""


    
    
    
    
    
    
    
    
    
    
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
        noncon_rules : List
            Contains sympy Or relationals and/or inequalities for rules that
            only consist of one argument without any contradictions
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
    # def removeRedundancy(self):
    #     # Do I only want to remove redundancies in the new rules?...or do I
    #     # want to do the entire list of rules established thus far?
        
    #     return
    
    

    









def test_remove_contradiction(self):
    """
    Unit tests for the removeContradiction method
    """
    
    # Initialize sympy variables
    x = self.x
    
    # Test noncontradictory rule lists
    mc = mergeConstraints(self.noncon_list1)
    list1 = mc.removeContradiction()
    self.assertEqual(self.noncon_list1, list1)
    
    mc = mergeConstraints(self.noncon_list2)
    list2 = mc.removeContradiction()
    self.assertEqual(self.noncon_list2, list2)
    
    mc = mergeConstraints(self.noncon_list3)
    list3 = mc.removeContradiction()
    self.assertEqual(self.noncon_list3, list3)
    
    mc = mergeConstraints(self.noncon_list4)
    list4 = mc.removeContradiction()
    self.assertEqual(self.noncon_list4, list4)
    
    
    # Test contradictory rule lists
    mc = mergeConstraints(self.con_list1)
    list1 = mc.removeContradiction()
    exp_list1 = []
    self.assertEqual(list1, exp_list1)
    
    mc = mergeConstraints(self.con_list2)
    list2 = mc.removeContradiction()
    exp_list2 = [x[2] > 0.5]
    self.assertEqual(list2, exp_list2)
    
    mc = mergeConstraints(self.con_list3)
    list3 = mc.removeContradiction()
    exp_list3 = [sp.Or(x[0] > 0.5, x[2] < 0.5)]
    self.assertEqual(list3, exp_list3)
    
    mc = mergeConstraints(self.con_list4)
    list4 = mc.removeContradiction()
    exp_list4 = []
    self.assertEqual(list4, exp_list4)









    
# def remove_redundancies(rules):
#     non_redundant_rules = []
#     for i in range(len(rules)):
#         is_redundant = False
#         for j in range(len(rules)):
#             if i != j:
#                 implication = sp.Implies(rules[j], rules[i])
#                 if sp.simplify(implication) == True:
#                     is_redundant = True
#                     break
#         if not is_redundant:
#             non_redundant_rules.append(rules[i])
#     return non_redundant_rules   
    
    
    
    
