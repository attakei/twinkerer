# -*- coding:utf8 -*-
"""Tweet operate classes.
"""
import datetime


def _strptime(date_string):
    """wrapper to parse datetime-string for Twitter-API
    """
    try:
        datetime_data = datetime.datetime.strptime(
            date_string,
            '%a %b %d %H:%M:%S %z %Y'
        )
    except:
        datetime_data = datetime.datetime.strptime(
            date_string,
            '%a %b %d %H:%M:%S +0000 %Y'
        )
    return datetime_data


class _ConvertPattern(object):
    class ConvertFailed(Exception):
        pass

    class RequiredNotFound(Exception):
        pass

    def __init__(self, target, origin, converter=None, required=True):
        self.target = target
        self.origin = origin
        self.converter = converter
        self.required = required

    def convert(self, base_dict):
        if self.origin in base_dict:
            try:
                if self.converter:
                    attr_value_ = self.converter(base_dict[self.origin])
                else:
                    attr_value_ = base_dict[self.origin]
                return attr_value_
            except:
                raise self.ConvertFailed('target is %s: %s' % (self.origin, base_dict[self.origin]))
        elif self.required:
            raise self.RequiredNotFound('target is %s' % (self.origin,))


class Model(object):
    def __init__(self, json):
        for name_, pattern_ in self.__class__.__base__.__dict__.items():
            if isinstance(pattern_, _ConvertPattern):
                setattr(self, name_, pattern_.convert(json))
        for name_, pattern_ in self.__class__.__dict__.items():
            if isinstance(pattern_, _ConvertPattern):
                setattr(self, name_, pattern_.convert(json))


class Tweet(Model):
    """Tweet object based from twitter-api json
    """
    id = _ConvertPattern('id', 'id')
    created_at = _ConvertPattern('created_at', 'created_at', _strptime)
    text = _ConvertPattern('text', 'text')


class ReTweet(Tweet):
    """ReTweet object based from twitter-api json
    """
    pass


def parse_tweet(json):
    if 'retweeted_status' in json:
        return ReTweet(json['retweeted_status'])
    return Tweet(json)
