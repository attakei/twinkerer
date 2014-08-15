# -*- coding:utf8 -*-
"""Tweet operate classes.
"""
import datetime
from twinkerer import utils


class _ConvertPattern(object):
    class ConvertFailed(Exception):
        pass

    class RequiredNotFound(Exception):
        pass

    def __init__(self, base_name, converter=None, required=True):
        self.base_name = base_name
        self.converter = converter
        self.required = required

    def convert(self, base_dict):
        if self.base_name in base_dict:
            try:
                if self.converter:
                    attr_value_ = self.converter(base_dict[self.base_name])
                else:
                    attr_value_ = base_dict[self.base_name]
                return attr_value_
            except:
                raise self.ConvertFailed('target is %s: %s' % (self.base_name, base_dict[self.base_name]))
        elif self.required:
            raise self.RequiredNotFound('target is %s' % (self.base_name,))


class Model(object):
    def __init__(self, json):
        for name_, pattern_ in self.__class__.__base__.__dict__.items():
            if isinstance(pattern_, _ConvertPattern):
                setattr(self, name_, pattern_.convert(json))
        for name_, pattern_ in self.__class__.__dict__.items():
            if isinstance(pattern_, _ConvertPattern):
                setattr(self, name_, pattern_.convert(json))


class User(Model):
    """twitter user-account object based from twitter-api json
    """
    id = _ConvertPattern('id')
    name = _ConvertPattern('name')
    screen_name = _ConvertPattern('screen_name')
    profile_image_url = _ConvertPattern('profile_image_url', required=False)
    profile_image_url_https = _ConvertPattern('profile_image_url_https', required=False)


class Tweet(Model):
    """Tweet object based from twitter-api json
    """
    id = _ConvertPattern('id')
    created_at = _ConvertPattern('created_at', utils.strptime)
    text = _ConvertPattern('text')

    def __init__(self, json):
        super(Tweet, self).__init__(json)
        self.user = User(json['user'])


class ReTweet(Tweet):
    """ReTweet object based from twitter-api json
    """
    pass


def parse_tweet(json):
    if 'retweeted_status' in json:
        return ReTweet(json['retweeted_status'])
    return Tweet(json)
