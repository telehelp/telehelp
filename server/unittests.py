import unittest
import math

from zipcode_utils import *

class TestZipcodeUtils(unittest.TestCase):

    def test_ZipNotInDB(self):
        self.assertEqual(getDistanceApart(170700, 74693), -1)

    def test_zipInDB(self):
        self.assertEqual(math.floor(getDistanceApart(17070, 74693)), 35.0)

    def test_districtInDB(self):
        self.assertEqual(getDistrict(17070), 'Stockholm')

    def test_districtNotInDB(self):
        self.assertEqual(getDistrict(170700), 'n/a')

if __name__ == '__main__':
    unittest.main()
