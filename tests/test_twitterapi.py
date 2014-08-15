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
    class Target(object):
        id_str = _ConvertPattern('id_str', 'id', str)

    def test_convert(self):
        p_ = _ConvertPattern('id_str', 'id', str)
        self.assertIsInstance(p_.convert({'id':1}), str)

    def test_no_convert(self):
        p_ = _ConvertPattern('id_str', 'id')
        data_ = {'id': 111}
        value = p_.convert(data_)
        self.assertEqual(value, 111)

    def test_convert_failed(self):
        def _strptime(bs):
            return datetime.datetime.strptime(bs, '%a')
        p_ = _ConvertPattern('id_str', 'id', _strptime)
        data_ = {'id': 111}
        with self.assertRaises(p_.ConvertFailed):
            p_.convert(data_)

    def test_required(self):
        p_ = _ConvertPattern('id_str', 'id', str)
        data_ = {'id2': 111}
        with self.assertRaises(p_.RequiredNotFound):
            p_.convert(data_)

    def test_not_required(self):
        p_ = _ConvertPattern('id_str', 'id', str, False)
        data_ = {'id2': 111}
        try:
            p_.convert(data_)
        except p_.RequiredNotFound:
            self.fail('caught Exception')
