import unittest
import unittest.mock

from alphalib.utils import logger


class TestFundamental(unittest.TestCase):
    """Test out the fundamental indicator.

    - EPS
    - P/E
    - PEG
    - FCF
    - P/B
    - ROE
    - DPR
    - P/S
    - DYR
    - DE

    """

    def setUp(self):
        logger.info("Setup")

    def tearDown(self):
        logger.info("Tear down")

    def test_logger(self):
        logger.info("test_logger")
