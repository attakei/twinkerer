"""python-twitter wrapper functions.
"""
try:
    from ConfigParser import ConfigParser
except:
    from configparser import ConfigParser
import twitter
from twinkerer import utils


DEFAULT_SECTION = 'twitter'

DEFAULT_CONFIGS = {
    'twinkerer_templates': {
        'title_oneday': 'tweets at {from_date}',
        'title_between': 'tweets from {from_date} to {to_date}',
    }
}


class Twinkerer(object):
    def __init__(self, api, config={}):
        self._api = api
        self._me = None
        self._config = utils.update_dict(DEFAULT_CONFIGS, config)

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
        config_ = {k: v for k, v in module.__dict__.items() if k.startswith('twinkerer_')}
        return cls(api_, config_)

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

    def fetch(self, args):
        from twinkerer.twitterapi import parse_tweet, ReTweet
        for tweet in self.get_my_timeline():
            tweet_inst = parse_tweet(tweet)
            if isinstance(tweet_inst, ReTweet):
                print(u'Re>\n'+tweet_inst.text)
            else:
                print(u'Tw>\n'+tweet_inst.text)
            print('========')

    def build_title(self, from_date, to_date, template=None):
        if template is None:
            if from_date == to_date:
                template = self._config['twinkerer_templates']['title_oneday']
            else:
                template = self._config['twinkerer_templates']['title_between']
        return template.format(from_date=from_date, to_date=to_date)
