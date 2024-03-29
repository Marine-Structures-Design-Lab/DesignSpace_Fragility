"""
SUMMARY:
Unit tests for the getInput class from input_vals.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from input_vals import getInput
from vars_def import setProblem
from create_key import createKey
from get_constraints import getConstraints
import unittest
import copy
import numpy as np
import sympy as sp

"""
CLASSES
"""
class test_input_vals(unittest.TestCase):

    def setUp(self):
        """
        Establish dictionaries for each discipline and rules as object
        definitions
        """
        
        # Set up the initial list of dictionaries for each discipline and rules
        prob = setProblem()
        self.Discips1, self.Input_Rules, self.Output_Rules = prob.SBD1()
        
        # Add time to each discipline
        for i in range(0,len(self.Discips1)):
            self.Discips1[i]['time'] = i+2
        
        # Create copy of each discipline and give it a partially filled list of
        # inputs
        self.Discips2 = copy.deepcopy(self.Discips1)
        for i in range(0,len(self.Discips2)):
            self.Discips1[i] = createKey('tested_ins',self.Discips1[i])
            self.Discips2[i] = createKey('tested_ins',self.Discips2[i])
            self.Discips2[i]['tested_ins'] = np.ones((10,\
                                                len(self.Discips2[i]['ins'])))
        
        # Create an impossible list of rules to satisfy
        x = sp.symbols('x:6')
        self.Input_Rules_bad =\
            [sp.And(x[i] < 0.0, x[i] > 1.0) for i in range(len(x))]
        
        # Initialize test disciplines
        self.Dtest1 = [None]*len(self.Discips1)
        self.Dtest2 = [None]*len(self.Discips2)
        self.Dtest3 = [None]*len(self.Discips1)
        self.Dtest4 = [None]*len(self.Discips2)
        
        # Loop through each discipline
        for i in range(0,len(self.Discips1)):
            
            # Get the input value rules
            ir1 = getConstraints(self.Discips1[i]['ins'],self.Input_Rules)
            ir2 = getConstraints(self.Discips1[i]['ins'],self.Input_Rules_bad)
            
            # Initialize different objects for each discipline and rules combo
            inppts1 = getInput(copy.deepcopy(self.Discips1[i]),ir1,20,i)
            inppts2 = getInput(copy.deepcopy(self.Discips2[i]),ir1,20,i)
            inppts3 = getInput(copy.deepcopy(self.Discips1[i]),ir2,20,i)
            inppts4 = getInput(copy.deepcopy(self.Discips2[i]),ir2,20,i)
            
            # Produce new disciplines
            self.Dtest1[i] = inppts1.getUniform(100)
            self.Dtest2[i] = inppts2.getUniform(100)
            self.Dtest3[i] = inppts3.getUniform(100)
            self.Dtest4[i] = inppts4.getUniform(100)
        
    def test_get_uniform(self):
        """
        Unit tests for the getUniform method
        """
        
        # Loop through each discipline
        for i in range(0,len(self.Discips1)):
            
            # Check that more points are not created than there should be
            self.assertEqual(np.shape(self.Dtest1[i]['tested_ins'])[0],\
                             20//self.Dtest1[i]['time'])
            self.assertEqual(np.shape(self.Dtest2[i]['tested_ins'])[0],\
                             (20//self.Dtest2[i]['time'])+10)
            self.assertEqual(np.shape(self.Dtest3[i]['tested_ins'])[0],0)
            self.assertEqual(np.shape(self.Dtest4[i]['tested_ins'])[0],10)
            
            # Check that program is not rewriting previously established points
            self.assertEqual(self.Dtest2[i]['tested_ins'][0:10,:].tolist(),\
                             self.Discips2[i]['tested_ins'].tolist())
            self.assertEqual(self.Dtest4[i]['tested_ins'][0:10,:].tolist(),\
                             self.Discips2[i]['tested_ins'].tolist())
        
    
    # Other methods
        
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_input_vals)
unittest.TextTestRunner(verbosity=2).run(suite)