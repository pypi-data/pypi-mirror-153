"""OSEF library version."""
# Standard imports
from pkg_resources import get_distribution

# OSEF imports
import osef

__version__ = get_distribution(osef.__name__).version
