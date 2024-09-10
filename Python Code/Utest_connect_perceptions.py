"""
SUMMARY:
Unit tests for the functions in connect_perceptions.py

CREATOR:
Joseph B. Van Houten
joeyvan@umich.edu
"""

"""
LIBRARIES
"""
from connect_perceptions import organizeData, prepareData, connectPerceptions
import unittest


"""
CLASSES
"""
class test_connect_perceptions(unittest.TestCase):

    def setUp(self):
        """
        Initialize variables and object call for functions
        """
        
    def test_organize_data(self):
        """
        Unit tests for the organizeData function
        """
    
    
    def test_prepare_data(self):
        """
        Unit tests for the prepareData function
        """
    
    
    def test_connect_perceptions(self):
        """
        Unit tests for the connectPerceptions function
        """



"""
SCRIPT
"""
suite = unittest.TestLoader().loadTestsFromTestCase(test_connect_perceptions)
unittest.TextTestRunner(verbosity=2).run(suite)