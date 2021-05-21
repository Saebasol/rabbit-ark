import sys
from collections import namedtuple

__version__ = "0.1.0"

__author__ = "Ryu JuHeon"

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(major=0, minor=1, micro=0, releaselevel="alpha", serial=0)
