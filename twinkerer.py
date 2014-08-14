"""python-twitter wrapper functions.
"""
import sys
import configparser
import twitter


DEFAULT_SECTION = 'twitter'


class Twinkerer(object):
    def __init__(self, api):
        self._api = api

    @classmethod
    def from_config(cls, config, section=None):
        if section is None:
            section = DEFAULT_SECTION
        else:
            section = str(section)
        if not isinstance(config, configparser.ConfigParser):
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


def main(argv=None):
    """console script
    """
    if not argv:
        argv = sys.argv
