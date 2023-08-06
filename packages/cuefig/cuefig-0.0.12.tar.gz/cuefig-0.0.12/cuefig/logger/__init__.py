import logging
import os
import sys
from logging import config
from typing import Dict

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources
from cuefig import eprint

import yaml

try:
    import conf
    from conf import LOGGING_DIR
except ImportError:
    eprint("Need LOGGING_DIR, LOGGING_DIR config for logger")
    sys.exit(0)


def create_logger() -> Dict:
    if not LOGGING_DIR.exists():
        os.makedirs(LOGGING_DIR)
    try:
        from conf import LOGGING_CONFIG
        f = open(LOGGING_CONFIG)
    except ImportError:
        f = pkg_resources.open_text(__name__, 'logging.yaml')

    conf: Dict = yaml.load(f, Loader=yaml.FullLoader)
    for k, handler in conf["handlers"].items():
        if k != "console":
            # if handler["class"] == "logging.handlers.TimedRotatingFileHandler":
            handler["filename"] = LOGGING_DIR / handler["filename"]
    f.close()
    return conf


logger_conf = create_logger()
logging.config.dictConfig(logger_conf)
logger = logging.getLogger("logger")
__all__ = ["logger"]
