import math
import unittest

from .zipcode_utils import getDistanceApart
from .zipcode_utils import getDistrict
from .zipcode_utils import getLatLong
from .zipcode_utils import readZipCodeData

loc_d, dis_d = readZipCodeData("SE.txt")


class TestZipcodeUtils(unittest.TestCase):
    def test_getDistanceApart(self):
        self.assertEqual(getDistanceApart(170700, 74693, loc_d), -1)
        self.assertEqual(math.floor(getDistanceApart(17070, 74693, loc_d)), 35.0)

    def test_getDistrict(self):
        self.assertEqual(getDistrict(17070, dis_d), "Stockholm")
        self.assertEqual(getDistrict(170700, loc_d), "n/a")


if __name__ == "__main__":
    unittest.main()
