# -*- coding:utf8 -*-
"""Tweet operate classes.
"""
import datetime


def _strptime(date_string):
    """wrapper to parse datetime-string for Twitter-API
    """
    return datetime.datetime.strptime(
        date_string,
        '%a %b %d %H:%M:%S %z %Y'
    )


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
                raise self.ConvertFailed()
        elif self.required:
            raise self.RequiredNotFound()


class Model(object):
    def __init__(self, json):
        for name_, pattern_ in self.__class__.__dict__.items():
            if isinstance(pattern_, _ConvertPattern):
                setattr(self, name_, pattern_.convert(json))


class Tweet(Model):
    """Tweet object based from twitter-api json
    """
    id = _ConvertPattern('id', 'id_str')
    created_at = _ConvertPattern('created_at', 'created_at', _strptime)
    text = _ConvertPattern('text', 'text')
