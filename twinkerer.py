"""python-twitter wrapper functions.
"""
import sys
import configparser
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


def main(argv=None):
    """console script
    """
    if not argv:
        argv = sys.argv
