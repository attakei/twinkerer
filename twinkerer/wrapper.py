"""python-twitter wrapper functions.
"""
import ConfigParser
import twitter


DEFAULT_SECTION = 'twitter'


def setup_api(config, section=None):
    if section is None:
        section = DEFAULT_SECTION
    else:
        section = str(section)
    if not isinstance(config, ConfigParser.ConfigParser):
        raise ValueError()
    elif not config.has_section(section):
        raise ValueError("Argument-config don't have section 'twitter'")
    return twitter.Api(
        consumer_key=config.get(section, 'consumer_key'),
        consumer_secret=config.get(section, 'consumer_secret'),
        access_token_key=config.get(section, 'access_token'),
        access_token_secret=config.get(section, 'access_token_secret')
    )
