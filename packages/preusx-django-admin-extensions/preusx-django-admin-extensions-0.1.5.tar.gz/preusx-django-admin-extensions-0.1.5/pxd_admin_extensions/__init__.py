__version__ = '0.1.5'

from .annotations import *
from .multidb import *
from .form_types import *
from .changelist_template_names import *

from .filters import *

VERSION = tuple(__version__.split('.'))
