# Why testing?
# The testing is important since it discovers defects/bugs before the delivery to the client. 
# which guarantees the quality of the software. It makes the software more reliable and easy to use. 
# Thoroughly tested software ensures reliable and high-performance software operation.

import sys
import unittest
import pandas as pd

import calorie_count.core as cc

class testFile(unittest.TestCase):

    def test_sys(self):
        """
        checks for Python Version 3.0 or higher
        """
        assert sys.version.split()[0].startswith("3.")

    def test_outcome_bmr(self):
        """
        checks the result of function calculate_bmr_amr
        """
        bmr, amr = cc.calculate_bmr_amr({'height': 170,
                                'weight': 55,
                                'age': 25,
                                'gender': 'w',
                                'activity': 1})
        self.assertEqual(int(bmr), 1378)
        self.assertEqual(int(amr), 1654)

    def test_data(self):
        """
        checks the first line of data file with met values
        """
        mets = pd.read_csv('data/met_list_activities.csv',
                            sep=';', 
                            decimal=',')
        self.assertEqual(
            float(mets[mets['SPECIFIC MOTION'] == 'bicycling, mountain, uphill, vigorous']['METs']),
            14)
       
if __name__ == '__main__':
    unittest.main()