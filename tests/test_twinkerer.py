import unittest
import os
import sys
import datetime
try:
    from ConfigParser import ConfigParser, NoOptionError
except:
    from configparser import ConfigParser, NoOptionError
from twinkerer import Twinkerer
import twitter


HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.append(HERE)


class Tests(unittest.TestCase):
    def test_it(self):
        pass


class TwinkererTests(unittest.TestCase):
    def test_from_config(self):
        config = ConfigParser()
        config.add_section('twitter')
        config.set('twitter', 'consumer_key', 'consumer_key')
        config.set('twitter', 'consumer_secret', 'consumer_secret')
        config.set('twitter', 'access_token_key', 'access_token_key')
        config.set('twitter', 'access_token_secret', 'access_token_secret')
        tw_ = Twinkerer.from_config(config)
        self.assertIsInstance(tw_, Twinkerer)
        self.assertIsInstance(tw_._api, twitter.Twitter)

    def test_from_module(self):
        import testmodule1
        tw_ = Twinkerer.from_module(testmodule1)
        self.assertIsInstance(tw_, Twinkerer)
        self.assertIsInstance(tw_._api, twitter.Twitter)


class TwinkererFromConfigTests(unittest.TestCase):
    def test_not_like_configparser(self):
        invalid_patterns = [
            1,
            'sss',
            [1, 2],
            dict(),
            ]
        for invalid_param in invalid_patterns:
            with self.assertRaises(ValueError):
                Twinkerer.from_config(invalid_param)

    def test_not_have_section(self):
        config = ConfigParser()
        with self.assertRaises(ValueError):
            Twinkerer.from_config(config)
        config.add_section('twitter')
        try:
            Twinkerer.from_config(config)
        except ValueError:
            self.fail()
        except:
            pass
        with self.assertRaises(ValueError):
            Twinkerer.from_config(config, 'twitter2')
        config.add_section('twitter2')
        try:
            Twinkerer.from_config(config, 'twitter2')
        except ValueError:
            self.fail()
        except:
            pass

    def test_not_value_in_section(self):
        config = ConfigParser()
        config.add_section('twitter')
        with self.assertRaises(NoOptionError):
            Twinkerer.from_config(config)
        for conf_name in ['consumer_key', 'consumer_secret', 'access_token_key', 'access_token_secret']:
            with self.assertRaises(NoOptionError):
                Twinkerer.from_config(config)
            config.set('twitter', conf_name, conf_name)
        tw_ = Twinkerer.from_config(config)
        self.assertIsInstance(tw_._api, twitter.Twitter)


class TwinkererBuildTitleTests(unittest.TestCase):
    template = 'tweets from {from_date} to {to_date}'

    def setUp(self):
        import testmodule1
        self.tw = Twinkerer.from_module(testmodule1)
        self.today = datetime.date.today()
        self.yesterday = self.today - datetime.timedelta(1)

    def test_it(self):
        title_ = self.tw.build_title(self.yesterday, self.today, self.template)
        self.assertEqual(title_, 'tweets from %s to %s' %(str(self.yesterday), str(self.today)))

    def test_formated(self):
        title_ = self.tw.build_title(self.today, self.today, '')
        self.assertEqual(title_, '')

    def test_default_template(self):
        title_ = self.tw.build_title(self.yesterday, self.today)
        self.assertEqual(title_, 'tweets from %s to %s' %(str(self.yesterday), str(self.today)))
        title_ = self.tw.build_title(self.today, self.today)
        self.assertEqual(title_, 'tweets at %s' % str(self.today))

    def test_module_config(self):
        import testmodule2
        tw = Twinkerer.from_module(testmodule2)
        title_ = tw.build_title(self.yesterday, self.today)
        self.assertEqual(title_, 'from %s to %s' %(str(self.yesterday), str(self.today)))
        title_ = tw.build_title(self.today, self.today)
        self.assertEqual(title_, '%s' % str(self.today))
