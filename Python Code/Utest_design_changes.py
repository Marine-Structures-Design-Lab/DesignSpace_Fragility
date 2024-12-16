"""
SUMMARY:
Unit tests for the changeDesign class from design_changes.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from design_changes import changeDesign
import unittest


"""
CLASSES
"""
class test_design_changes(unittest.TestCase):

    def setUp(self):
        """
        Initialize variables and object call for methods
        """
        
    
    def test_reqs(self):
        """
        Unit tests for the Reqs method
        """
        
    
    def test_reevaluate_points(self):
        """
        Unit tests for the reevaluatePoints method
        """
        
        


"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_design_changes)
unittest.TextTestRunner(verbosity=2).run(suite)