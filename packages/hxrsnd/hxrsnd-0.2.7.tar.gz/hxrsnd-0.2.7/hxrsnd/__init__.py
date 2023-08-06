from ._version import get_versions
from .plans.alignment import maximize_lorentz, rocking_curve

__version__ = get_versions()['version']
del get_versions

__all__ = ['maximize_lorentz', 'rocking_curve']
