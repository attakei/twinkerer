import datetime


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
