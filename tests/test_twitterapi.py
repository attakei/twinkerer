import unittest
from twinkerer.twitterapi import (
    _ConvertPattern,
    Tweet, ReTweet, parse_tweet,
    User,
)
import datetime


class TweetTests(unittest.TestCase):
    def test_from_json(self):
        tw_ = Tweet({
            "id": 12738165059, "id_str": "12738165059", "created_at": "Thu Oct 14 22:20:15 +0000 2010", "text": "tweet",
            "user": {"id": 2, "name": "testet", "screen_name": "test_user"},
        })
        self.assertIsInstance(tw_, Tweet)
        self.assertEqual(tw_.id, 12738165059)
        self.assertIsInstance(tw_.created_at, datetime.datetime)
        self.assertIsInstance(tw_.text, str)
        self.assertIsInstance(tw_.user, User)

    def test_url(self):
        tw_ = Tweet({
            "id": 12738165059, "id_str": "12738165059", "created_at": "Thu Oct 14 22:20:15 +0000 2010", "text": "tweet",
            "user": {"id": 2, "name": "testet", "screen_name": "test_user"},
        })
        self.assertEqual(tw_.url, 'https://twitter.com/{0}/statuses/{1}'.format(tw_.user.name, tw_.id))
        # TODO: add next attributes...

class ReTweetTests(unittest.TestCase):
    def test_from_json(self):
        tw_ = ReTweet({
            "id": 12738165059, "id_str": "12738165059", "created_at": "Thu Oct 14 22:20:15 +0000 2010", "text": "tweet",
            "user": {"id": 2, "name": "testet", "screen_name": "test_user"},
        })
        self.assertIsInstance(tw_, ReTweet)
        self.assertEqual(tw_.id, 12738165059)
        self.assertIsInstance(tw_.created_at, datetime.datetime)
        self.assertIsInstance(tw_.text, str)

    def test_url(self):
        tw_ = ReTweet({
            "id": 12738165059, "id_str": "12738165059", "created_at": "Thu Oct 14 22:20:15 +0000 2010", "text": "tweet",
            "user": {"id": 2, "name": "testet", "screen_name": "test_user"},
        })
        self.assertEqual(tw_.url, 'https://twitter.com/{0}/statuses/{1}'.format(tw_.user.name, tw_.id))


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
