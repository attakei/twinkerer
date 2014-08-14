"""Testing python-twitter wrapper functions for tTwinkerer
"""
import unittest

import twinkerer
import configparser
import twitter

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
                twinkerer.setup_api(invalid_param)

    def test_not_have_section(self):
        config = configparser.ConfigParser()
        with self.assertRaises(ValueError):
            twinkerer.setup_api(config)
        config.add_section('twitter')
        try:
            twinkerer.setup_api(config)
        except ValueError:
            self.fail()
        except:
            pass
        with self.assertRaises(ValueError):
            twinkerer.setup_api(config, 'twitter2')
        config.add_section('twitter2')
        try:
            twinkerer.setup_api(config, 'twitter2')
        except ValueError:
            self.fail()
        except:
            pass

    def test_not_value_in_section(self):
        config = configparser.ConfigParser()
        config.add_section('twitter')
        with self.assertRaises(configparser.NoOptionError):
            twinkerer.setup_api(config)
        for conf_name in ['consumer_key', 'consumer_secret', 'access_token', 'access_token_secret']:
            with self.assertRaises(configparser.NoOptionError):
                twinkerer.setup_api(config)
            config.set('twitter', conf_name, conf_name)
        api_ = twinkerer.setup_api(config)
        self.assertIsInstance(api_, twitter.Twitter)