import unittest
from twinkerer.twitterapi import (
    _ConvertPattern,
    Tweet, ReTweet, parse_tweet,
    User,
)
import datetime


class TweetTests(unittest.TestCase):
    def setUp(self):
        self.tw = Tweet({
            "id": 12738165059, "id_str": "12738165059", "created_at": "Thu Oct 14 22:20:15 +0000 2010", "text": "tweet",
            "user": {"id": 2, "name": "testet", "screen_name": "test_user"},
        })


    def test_from_json(self):
        self.assertIsInstance(self.tw, Tweet)
        self.assertEqual(self.tw.id, 12738165059)
        self.assertIsInstance(self.tw.created_at, datetime.datetime)
        self.assertIsInstance(self.tw.text, str)
        self.assertIsInstance(self.tw.user, User)
        # TODO: add next attributes...

    def test_url(self):
        self.assertEqual(self.tw.url, 'https://twitter.com/{0}/statuses/{1}'.format(self.tw.user.name, self.tw.id))

    def test_as_html(self):
        html_ = self.tw.as_html()
        self.assertIn(self.tw.created_at.strftime('%Y-%m-%d %H:%M'), html_)
        self.assertIn(self.tw.text, html_)
        self.assertIn(self.tw.url, html_)
        self.assertIn('Tweet:', html_)

    def test_as_html_multilines(self):
        self.tw.text = '''test
test2'''
        html_ = self.tw.as_html()
        self.assertIn('<br />', html_)


class ReTweetTests(unittest.TestCase):
    def setUp(self):
        self.tw = ReTweet({
            "id": 12738165059, "id_str": "12738165059", "created_at": "Thu Oct 14 22:20:15 +0000 2010", "text": "tweet",
            "user": {"id": 2, "name": "testet", "screen_name": "test_user"},
        })

    def test_from_json(self):
        self.assertIsInstance(self.tw, ReTweet)
        self.assertEqual(self.tw.id, 12738165059)
        self.assertIsInstance(self.tw.created_at, datetime.datetime)
        self.assertIsInstance(self.tw.text, str)

    def test_url(self):
        self.assertEqual(self.tw.url, 'https://twitter.com/{0}/statuses/{1}'.format(self.tw.user.name, self.tw.id))

    def test_as_html(self):
        html_ = self.tw.as_html()
        self.assertIn(self.tw.created_at.strftime('%Y-%m-%d %H:%M'), html_)
        self.assertIn(self.tw.text, html_)
        self.assertIn(self.tw.url, html_)
        self.assertIn('ReTweet:', html_)


class UserTests(unittest.TestCase):
    def test_from_json(self):
        user_ = User({"id": 1, "name": "user", "screen_name": "tweetie"})
        self.assertIsInstance(user_, User)
        self.assertEqual(user_.id, 1)
        self.assertEqual(user_.name, 'user')
        self.assertEqual(user_.screen_name, 'tweetie')
        self.assertEqual(user_.url, 'https://twitter.com/{0}'.format(user_.name))
        # TODO: add next attributes...


class ParseTweetTests(unittest.TestCase):
    def test_tweet(self):
        tw_ = parse_tweet({
            "id": 12738165059, "id_str": "12738165059", "created_at": "Thu Oct 14 22:20:15 +0000 2010", "text": "tweet",
            "user": {"id": 2, "name": "testet", "screen_name": "test_user"},
        })
        self.assertIsInstance(tw_, Tweet)

    def test_retweet(self):
        tw_ = parse_tweet({
            "id": 12738165059, "id_str": "12738165059", "created_at": "Thu Oct 14 22:20:15 +0000 2010", "text": "tweet",
            "user": {"id": 2, "name": "testet", "screen_name": "test_user"},
            "retweeted_status": {
                "retweeted": True, "created_at": "Fri Aug 15 02:22:31 +0000 2014", "id": 1, "text": "text",
                "user": {"id": 2, "name": "testet", "screen_name": "test_user"},
            }
        })
        self.assertIsInstance(tw_, ReTweet)
        self.assertEqual(tw_.id, 1)


class ConvertPatternTests(unittest.TestCase):
    def test_convert(self):
        p_ = _ConvertPattern('id', str)
        self.assertIsInstance(p_.convert({'id': 1}), str)

    def test_no_convert(self):
        p_ = _ConvertPattern('id')
        value = p_.convert({'id': 111})
        self.assertEqual(value, 111)

    def test_convert_failed(self):
        def _strptime(bs):
            return datetime.datetime.strptime(bs, '%a')
        p_ = _ConvertPattern('id', _strptime)
        with self.assertRaises(p_.ConvertFailed):
            p_.convert({'id': 111})

    def test_required(self):
        p_ = _ConvertPattern('id', str)
        with self.assertRaises(p_.RequiredNotFound):
            p_.convert({'id2': 111})

    def test_not_required(self):
        p_ = _ConvertPattern('id', str, False)
        try:
            p_.convert({'id2': 111})
        except p_.RequiredNotFound:
            self.fail('caught Exception')
