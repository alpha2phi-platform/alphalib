import unittest

from numpy import histogram_bin_edges

from alphalib.analysis.strategy import recent_prices


class TestStrategy(unittest.TestCase):
    def test_enter_strategy(self):
        hist_prices = recent_prices("ecc")
        assert hist_prices is not None
