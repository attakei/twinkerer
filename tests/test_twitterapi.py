import unittest
from twinkerer.twitterapi import Tweet
import datetime


class TweetTests(unittest.TestCase):
    def test_from_json(self):
        tw_ = Tweet({"id": 12738165059, "id_str": "12738165059", "created_at": "Thu Oct 14 22:20:15 +0000 2010", "text": "tweet"})
        self.assertIsInstance(tw_, Tweet)
        self.assertEqual(tw_.id, "12738165059")
        self.assertIsInstance(tw_.created_at, datetime.datetime)
        self.assertIsInstance(tw_.text, str)
        # TODO: add next attributes...
