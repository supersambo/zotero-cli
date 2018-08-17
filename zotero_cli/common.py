import os
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
try:
    UNICODE_EXISTS = bool(type(unicode))
except NameError:
    unicode = lambda s: str(s)
from collections import namedtuple

import click

APP_NAME = "zotcli"

Item = namedtuple("Item", ("key", "creator", "title", "abstract", "date", "citekey"))


def _get_config_path():
    return os.path.join(click.get_app_dir(APP_NAME), 'config.ini')


def load_config():
    """ Load configuration from application directory.

    :returns:           Configuration
    :rtype:             (flat) dict
    """
    cfg_path = _get_config_path()
    if not os.path.exists(cfg_path):
        raise ValueError("Could not find configuration file. Please run "
                         "`zotcli configure` to perform the first-time "
                         "setup.")
    parser = configparser.RawConfigParser()
    parser.read([cfg_path])
    rv = {}
    for section in parser.sections():
        for key, value in parser.items(section):
            rv['%s.%s' % (section, key)] = value
    return rv


def save_config(cfgdata):
    """ Save configuration to application directory.

    :param cfgdata: Configuration
    :type cfgdata:  (flat) dict
    """
    cfg_path = _get_config_path()
    cfg_dir = os.path.dirname(cfg_path)
    if not os.path.exists(cfg_dir):
        os.makedirs(cfg_dir)
    cfg = configparser.SafeConfigParser()
    cfg.add_section("zotcli")
    for key, value in cfgdata.items():
        cfg.set("zotcli", key, unicode(value))
    with open(cfg_path, "w") as fp:
        cfg.write(fp)

