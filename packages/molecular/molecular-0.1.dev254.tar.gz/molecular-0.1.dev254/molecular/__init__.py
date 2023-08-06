
from . import analysis
from .analysis import *

from . import bioinformatics
from .bioinformatics import *

from . import constants
from .constants import *

from . import core
from .core import *

from . import energy
from .energy import *

from . import geometry
from .geometry import *

from . import io
from .io import *

from . import simulations
from .simulations import *

from . import statistics
from .statistics import *

from . import transform
from .transform import *


# from . import external
# from .external import *


# from . import viz
# from .viz import *

from .misc import *
from .version import __version__

# Contents
# __all__ = [
#     'io',
#     'include_dir',
#     'misc',
#     # 'simulation',
#     '__version__'
# ]
__all__ = ['__version__']
__all__.extend(analysis.__all__)
__all__.extend(bioinformatics.__all__)
__all__.extend(core.__all__)
__all__.extend(energy.__all__)
# __all__.extend(external.__all__)
__all__.extend(geometry.__all__)
__all__.extend(io.__all__)
__all__.extend(simulations.__all__)
__all__.extend(statistics.__all__)
__all__.extend(transform.__all__)
# __all__.extend(viz.__all__)

# Add include path
import os

include_dir = os.path.abspath(__file__ + '/../../include')


# logging
# TODO let people disable this, or send it to a file
import logging
logging.basicConfig(
    filename='molecular.log',
    filemode='w',
    format='%(asctime)s %(levelname)s (%(name)s) %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)
logger = logging.getLogger('molecular')
logger.info(f'loaded version {__version__}')