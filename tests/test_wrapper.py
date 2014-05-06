"""Testing python-twitter wrapper functions for tTwinkerer
"""
import unittest

from twinkerer import wrapper

import ConfigParser

class SetupApiTests(unittest.TestCase):
    def test_not_like_configparser(self):
        invalid_patterns = [
            1,
            'sss',
            [1, 2],
            dict(),
        ]
        for invalid_param in invalid_patterns:
            with self.assertRaises(ValueError):
                wrapper.setup_api(invalid_param)

    def test_not_have_section(self):
        config = ConfigParser.ConfigParser()
        with self.assertRaises(ValueError):
            wrapper.setup_api(config)
        config.add_section('twitter')
        try:
            wrapper.setup_api(config)
        except ValueError:
            self.fail()
        with self.assertRaises(ValueError):
            wrapper.setup_api(config, 'twitter2')
        config.add_section('twitter2')
        try:
            wrapper.setup_api(config, 'twitter2')
        except ValueError:
            self.fail()
