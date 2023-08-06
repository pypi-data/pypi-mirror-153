import pprint

from .runtime_config import RuntimeConfig


def mformat(msg):

    if RuntimeConfig().misc["use_pprint"]:
        return pprint.pformat(msg)
    else:
        return msg
