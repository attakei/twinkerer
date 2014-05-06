"""python-twitter wrapper functions.
"""
import ConfigParser


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
