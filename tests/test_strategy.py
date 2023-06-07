import unittest

from alphalib.analysis.strategy import recent_prices


class TestStrategy(unittest.TestCase):
    def test_enter_strategy(self):
        hist_prices = recent_prices("cim")
        assert hist_prices is not None
