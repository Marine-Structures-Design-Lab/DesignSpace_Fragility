"""
SUMMARY:
Unit tests for the windfallRegret class from windfall_regret.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
import unittest


"""
CLASSES
"""
class test_windfall_regret(unittest.TestCase):

    def setUp(self):
        """
        
        """
        
        
        
        
        
    def test_initialize_wr(self):
        """
        Unit tests for the initalizeWR function
        """
    
    
    def test_get_indices(self):
        """
        Unit tests for the getIndices function
        """
    
    
    def test_complement_prob(self):
        """
        Unit tests for the complementProb function
        """
    
    
    def test_assign_wr(self):
        """
        Unit tests for the assignWR function
        """
    
    
    def test_calc_wind_regret(self):
        """
        Unit tests for the calcWindRegret method
        """
    
    
    def test_quant_risk(self):
        """
        Unit tests for the quantRisk method
        """
    
    
    
    
    
    
    
"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_windfall_regret)
unittest.TextTestRunner(verbosity=2).run(suite)