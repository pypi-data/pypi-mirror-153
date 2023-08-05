"""
Package version and distribution
"""
import pkg_resources as pkr

__pkg__ = 'avotes-parser-core'

try:
    __distribution__ = pkr.get_distribution(__pkg__)
    __version__ = __distribution__.version
except pkr.DistributionNotFound:
    __distribution__ = pkr.Distribution()
    __version__ = '0.0.0'
