from cuefig.utils import eprint

try:
    from conf import *
    from conf.logger import logger
except ImportError:
    eprint("You dont have create conf package")

try:
    from conf.config import *
except ImportError:
    eprint("You dont have create conf/config.py file")

try:
    from conf.config_deploy import *
except ImportError:
    eprint("You dont have create conf/config_deploy.py file")

