from cuefig.utils import eprint
from cuefig.logger import logger

try:
    from conf import *
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

