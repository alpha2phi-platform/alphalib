import unittest

from alphalib.utils import dateutils


class TestDateUtils(unittest.TestCase):
    def test_years_from_now(self):
        assert dateutils.years_from_now(10) != None
