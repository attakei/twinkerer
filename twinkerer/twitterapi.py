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

    def junction(self, target_obj, base_dict):
        if self.origin in base_dict:
            try:
                if self.converter:
                    attr_value_ = self.converter(base_dict[self.origin])
                else:
                    attr_value_ = base_dict[self.origin]
                setattr(target_obj, self.target, attr_value_)
            except:
                raise self.ConvertFailed()
        elif self.required:
            raise self.RequiredNotFound()


class Tweet(object):
    """Tweet object based from twitter-api json
    """
    __slots__ = ['id', 'created_at', 'text', ]

    CONVERT_PATTERNS = (
        _ConvertPattern('id', 'id_str'),
        _ConvertPattern('created_at', 'created_at', _strptime),
        _ConvertPattern('text', 'text'),
    )
    """convert patterns"""

    def __init__(self, json):
        for pattern in self.CONVERT_PATTERNS:
            pattern.junction(self, json)
