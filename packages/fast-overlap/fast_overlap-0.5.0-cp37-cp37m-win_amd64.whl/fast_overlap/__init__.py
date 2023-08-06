try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"
from ._engine import overlap, overlap_parallel

__all__ = ["__version__", "overlap", "overlap_parallel"]
