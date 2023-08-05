# __init__.py

# These are the categorised functions
from . import aws_utils
from . import utils
from . import models

# This allows people to get functions from dsgl directly.
# eg. import dsgl as ds
from .core import *

# This determines the import structure
# __all__ contains all of the functions in a given module
__all__ = []
__all__.extend(utils.__all__)
__all__.extend(aws_utils.__all__)
__all__.extend(models.__all__)
