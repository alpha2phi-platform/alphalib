import unittest
import unittest.mock

import pandas as pd

from alphalib.analysis import all_sources, seeking_alpha

# For testing
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
# pd.set_option("display.max_colwidth", None)


class TestAnalysis(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_stock_analysis(self):
        stock_analysis = all_sources("orc")
        print(stock_analysis)

    def test_seeking_alpha(self):
        analysis = seeking_alpha("gogl")
        print(analysis)
