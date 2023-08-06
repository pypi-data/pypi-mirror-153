from typing import TYPE_CHECKING

from nxml.core import LazyModule

from .launch import __all__ as launch__all__
from .comm import __all__ as comm__all__
from .utils import __all__ as utils__all__
from .launch import *
from .comm import *
from .utils import *

if TYPE_CHECKING:
    from . import xla
else:
    xla = LazyModule("nxml.torch.engine.xla")


__all__ = launch__all__ + comm__all__ + utils__all__ + ["xla"]
