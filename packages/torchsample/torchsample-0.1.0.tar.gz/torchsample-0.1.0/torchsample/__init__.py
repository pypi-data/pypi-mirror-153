from . import __meta__

try:
    from ._version import version as __version__
    from ._version import version_tuple
except ImportError:
    __version__ = "unknown version"
    version_tuple = (0, 0, "unknown version")

from . import coord, default, encoding, models
from ._sample import sample, sample2d, sample3d
from .coord import feat_first, feat_last, tensor_to_size
