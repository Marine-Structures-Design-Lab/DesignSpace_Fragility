"""
SUMMARY:
Unit tests for the getOutput class from output_vals.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from output_vals import getOutput
from vars_def import setProblem
from create_key import createKey
import unittest
import copy
import numpy as np

"""
CLASSES
"""
class test_output_vals(unittest.TestCase):

    def setUp(self):
        """
        Establish dictionaries for each discipline and rules as object
        definitions
        """
        
        # Set up the initial list of dictionaries for each discipline and rules
        prob = setProblem()
        self.Discips, self.Input_Rules, self.Output_Rules = prob.SBD1()
        self.DiscipsSY,self.Input_RulesSY,self.Output_RulesSY = prob.SenYang()
        
        # Loop through each discipline
        for i in range(0,len(self.Discips)):
            
            # Create new keys
            self.Discips[i] = createKey('tested_ins',self.Discips[i])
            self.Discips[i] = createKey('tested_outs',self.Discips[i])
            self.DiscipsSY[i] = createKey('tested_ins',self.DiscipsSY[i])
            self.DiscipsSY[i] = createKey('tested_outs',self.DiscipsSY[i])
        
            # Add input values to all disciplines in dictionary
            ### As well as partially filled output values
            self.Discips[i]['tested_ins'] = \
                np.random.rand(20,len(self.Discips[i]['ins']))
            self.DiscipsSY[i]['tested_ins'] = np.empty((0,6))
            self.Discips[i]['tested_outs'] = \
                np.zeros((10,len(self.Discips[i]['outs'])))
            
            # Add known input values to the very end of tested inputs array
            self.Discips[i]['tested_ins'] = \
                np.append(self.Discips[i]['tested_ins'],[[5,4,2]],axis=0)
            self.DiscipsSY[i]['tested_ins'] = \
                np.append(self.DiscipsSY[i]['tested_ins'],
                          [[0.3,0.0,0.1,0.8,0.0,0.4]],axis=0)
        
        # Create copy of the dictionary
        self.Discips1 = copy.deepcopy(self.Discips)
        
        # Create an empty list of zero numpy arrays
        self.answers = [np.zeros((1,1)),np.zeros((1,2)),np.zeros((1,2))]
        self.answersSY = [np.zeros((1,1)),np.zeros((1,1)),np.zeros((1,1))]
        
        # Loop through each discipline
        for i in range(0,len(self.Discips)):
            
            # Initialize object for each discipline
            outpts = getOutput(self.Discips1[i])
            outptsSY = getOutput(self.DiscipsSY[i])
            
            # Produce new discipline
            self.Discips1[i] = outpts.getValues()
            self.DiscipsSY[i] = outptsSY.getValues()
            
            # Establish "should-be" answers for last row of each discipline
            if i == 0:
                self.answers[i] = np.array([50.0])
                self.answersSY[i] = np.array([0.3181060495])
            elif i == 1:
                self.answers[i] = np.array([-1403.75,4356.0])
                self.answersSY[i] = np.array([-3.032175779])
            elif i == 2:
                self.answers[i] = np.array([6.567795368,0.8661219879])
                self.answersSY[i] = np.array([4996.572712])
        
        
    def test_get_values(self):
        """
        Unit tests for the getValues method
        """
        # Loop through each discipline
        for i in range(0,len(self.Discips)):
            
            # Check that there is NOT rewriting of previous output values
            self.assertEqual\
                (self.Discips1[i]['tested_outs'][0:10,:].tolist(),\
                 self.Discips[i]['tested_outs'].tolist())
            
            # Check that there is calculation of new output values
            self.assertTrue\
                (np.all(self.Discips1[i]['tested_outs'][10:20,:]))
            
            # Check that there is NOT calculation of old output values
            self.assertTrue\
                (not np.all(self.Discips1[i]['tested_outs'][0:10,:]))
            
            # Check that correct values are being calculated
            np.testing.assert_array_almost_equal\
                (self.Discips1[i]['tested_outs'][20,:],
                 self.answers[i])
            np.testing.assert_array_almost_equal\
                (self.DiscipsSY[i]['tested_outs'][0,:],
                 self.answersSY[i])
    
    # Other methods
        
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_output_vals)
unittest.TextTestRunner(verbosity=2).run(suite)