import unittest
from twinkerer.twitterapi import Tweet, _ConvertPattern
import datetime


class TweetTests(unittest.TestCase):
    def test_from_json(self):
        tw_ = Tweet({"id": 12738165059, "id_str": "12738165059", "created_at": "Thu Oct 14 22:20:15 +0000 2010", "text": "tweet"})
        self.assertIsInstance(tw_, Tweet)
        self.assertEqual(tw_.id, "12738165059")
        self.assertIsInstance(tw_.created_at, datetime.datetime)
        self.assertIsInstance(tw_.text, str)
        # TODO: add next attributes...


class ConvertPatternTests(unittest.TestCase):
    def test_convert(self):
        p_ = _ConvertPattern('id_str', 'id', str)
        self.assertIsInstance(p_.convert({'id': 1}), str)

    def test_no_convert(self):
        p_ = _ConvertPattern('id_str', 'id')
        value = p_.convert({'id': 111})
        self.assertEqual(value, 111)

    def test_convert_failed(self):
        def _strptime(bs):
            return datetime.datetime.strptime(bs, '%a')
        p_ = _ConvertPattern('id_str', 'id', _strptime)
        with self.assertRaises(p_.ConvertFailed):
            p_.convert({'id': 111})

    def test_required(self):
        p_ = _ConvertPattern('id_str', 'id', str)
        with self.assertRaises(p_.RequiredNotFound):
            p_.convert({'id2': 111})

    def test_not_required(self):
        p_ = _ConvertPattern('id_str', 'id', str, False)
        try:
            p_.convert({'id2': 111})
        except p_.RequiredNotFound:
            self.fail('caught Exception')
