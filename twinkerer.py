"""python-twitter wrapper functions.
"""
import sys
import argparse
import datetime
try:
    from ConfigParser import ConfigParser
except:
    from configparser import ConfigParser
import twitter


DEFAULT_SECTION = 'twitter'


class Twinkerer(object):
    def __init__(self, api):
        self._api = api
        self._me = None

    @classmethod
    def from_config(cls, config, section=None):
        if section is None:
            section = DEFAULT_SECTION
        else:
            section = str(section)
        if not isinstance(config, ConfigParser):
            raise ValueError()
        elif not config.has_section(section):
            raise ValueError("Argument-config don't have section 'twitter'")
        api_ = twitter.Twitter(
            auth=twitter.OAuth(
                config.get(section, 'access_token_key'),
                config.get(section, 'access_token_secret'),
                config.get(section, 'consumer_key'),
                config.get(section, 'consumer_secret'),
                )
        )
        return cls(api_)

    @classmethod
    def from_module(cls, module):
        api_ = twitter.Twitter(
            auth=twitter.OAuth(
                module.twitter_access_token_key,
                module.twitter_access_token_secret,
                module.twitter_consumer_key,
                module.twitter_consumer_secret,
                )
        )
        return cls(api_)

    @property
    def me(self):
        if not self._me:
            user_settings = self._api.account.settings(_method='GET')
            user = self._api.users.show(screen_name=user_settings['screen_name'])
            user['_settings'] = user_settings
            self._me = user
        return self._me

    def get_my_timeline(self):
        user_id_ = self.me['id']
        tweets_ = self._api.statuses.user_timeline(user_id=user_id_)
        return tweets_


class DateStringAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        formats_ = [
            '%Y-%m-%d',
            '%Y/%m/%d',
        ]
        for format_ in formats_:
            try:
                dt_ = datetime.datetime.strptime(values, format_).date()
                setattr(namespace, self.dest, dt_)
                return
            except:
                continue
        raise Exception()

def build_args(args):
    args.from_date = args.to_date - datetime.timedelta(days=(args.days - 1))
    args.from_datetime = datetime.datetime(
        args.from_date.year,
        args.from_date.month,
        args.from_date.day,
    )
    args.to_datetime = datetime.datetime(
        args.to_date.year,
        args.to_date.month,
        args.to_date.day,
    ) + datetime.timedelta(days=1)

def main(argv=None):
    """console script
    """
    if not argv:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--date', dest='to_date',
        action=DateStringAction,
        default=(datetime.date.today() - datetime.timedelta(days=1)),
    )
    parser.add_argument(
        '--days', dest='days',
        type=int,
        default=7,
    )

    args = parser.parse_args(argv)
    build_args(args)
