import unittest
import unittest.mock

from alphalib.utils import logger


class TestDataSources(unittest.TestCase):
    """Test out the different data sources.
    """

    def setUp(self):
        logger.info("Setup")

    def tearDown(self):
        logger.info("Tear down")

    def test_logger(self):
        logger.info("test_logger")
