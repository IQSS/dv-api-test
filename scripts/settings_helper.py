from os.path import join, isfile, isdir
import json

from msg_util import *

SETTINGS_ATTRIBUTES = [ "DATAVERSE_URL", "API_TOKEN", ]
SETTINGS_DICT = None

def load_settings_dict(fname='settings.json'):
    assert isfile(fname), "File does not exist: %s" % fname

    global SETTINGS_DICT

    if SETTINGS_DICT is None:

        content = open(fname, 'r').read()

        try:
            SETTINGS_DICT = json.loads(content)
        except:
            msgx('Failed to convert file content to JSON\nFile:%s\nContent:%s' % (fname, content))

        for k in SETTINGS_DICT.keys():
            assert SETTINGS_DICT.has_key(k), "Settings file must have key '%s'" % k

    return SETTINGS_DICT


def get_setting(key_name):

    assert key_name is not None, 'key_name cannot be None'

    val = load_settings_dict().get(key_name, None)

    assert val is not None, 'Key "%s" not found in settings file' % key_name

    return val