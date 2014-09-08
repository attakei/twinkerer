import unittest
from twinkerer import utils
import datetime


class StrptimeTests(unittest.TestCase):
    def test_it(self):
        dt_ = utils.strptime('Sat Sep 06 16:45:01 +0000 2014')
        self.assertIsInstance(dt_, datetime.datetime)
        self.assertNotEqual(dt_.tzinfo, None)
        dt_ = utils.strptime('Sat Sep 06 16:45:01 +9000 2014')
        self.assertIsInstance(dt_, datetime.datetime)
        self.assertNotEqual(dt_.tzinfo, None)
