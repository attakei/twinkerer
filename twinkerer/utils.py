import sys
import datetime
import collections

PYTHON_MAJOR_VERSION = int(sys.version_info[0])


def update_dict(d, u):
    """update dict-instance recursive.
    """
    if PYTHON_MAJOR_VERSION == 3:
        it_ = u.items
    else:
        it_ = u.iteritems
    for k, v in it_():
        if isinstance(v, collections.Mapping):
            r = update_dict(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


def strptime(date_string):
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
