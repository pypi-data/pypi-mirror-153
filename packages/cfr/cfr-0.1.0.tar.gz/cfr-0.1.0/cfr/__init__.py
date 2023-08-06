from .climate import *
from .proxy import *
from .da import *
from .reconjob import *
from .reconres import *
try:
    from . import ml
except:
    pass

from .visual import (
    set_style,
    showfig,
    closefig,
    savefig,
)
set_style(style='journal', font_scale=1.2)

# get the version
from importlib.metadata import version
__version__ = version('cfr')