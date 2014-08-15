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


class Tweet(object):
    """Tweet object based from twitter-api json
    """
    __slot__ = ['id', 'created_at', 'text', ]

    JSON_OBJ_MAPS = (
        ('id', 'id_str', None),
        ('created_at', 'created_at', _strptime),
        ('text', 'text', None),
    )
    """convert patterns"""

    def __init__(self, json):
        for map_ in self.JSON_OBJ_MAPS:
            if map_[1] in json:
                if map_[2] is None:
                    value = json[map_[1]]
                else:
                    value = map_[2](json[map_[1]])
                setattr(self, map_[0], value)
