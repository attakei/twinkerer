import os
import sys
import unittest
from twinkerer import cmd
import pytz
import datetime


HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.append(HERE)


class ArgParserTests(unittest.TestCase):
    def test_dates(self):
        args = cmd.ArgParser.parse_args('')
        self.assertIsInstance(args.to_date, datetime.date)


class BuildArgsTests(unittest.TestCase):
    def test_default_command(self):
        import testmodule1
        args = cmd.ArgParser.parse_args('')
        cmd.build_args(args, testmodule1)
        self.assertEqual(args.command, 'fetch')

    def test_target_datetime_utc(self):
        import testmodule1
        args = cmd.ArgParser.parse_args('')
        cmd.build_args(args, testmodule1)
        self.assertIsInstance(args.from_datetime, datetime.datetime)
        self.assertIsInstance(args.to_datetime, datetime.datetime)
        self.assertNotEqual(args.from_datetime.tzinfo, None)

    def test_target_datetime_locale(self):
        import testmodule2
        args = cmd.ArgParser.parse_args('')
        cmd.build_args(args, testmodule2)
        self.assertIsInstance(args.from_datetime, datetime.datetime)
        self.assertIsInstance(args.to_datetime, datetime.datetime)
        self.assertNotEqual(args.from_datetime.tzinfo, pytz.utc)
