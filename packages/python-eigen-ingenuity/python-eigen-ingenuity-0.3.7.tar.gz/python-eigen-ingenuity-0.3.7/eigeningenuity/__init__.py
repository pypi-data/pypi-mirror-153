"""Eigen Ingenuity

Interface to the Eigen Ingenuity system.

Set the EIGENSERVER environment variable either to hostname, hostname:port
or http://hostname:port/prefix/path as appropriate. It defaults to
localhost:8080.

The various get_XXX methods instantiate connections to different parts
of the Eigen Ingenuity infrastructure.

Currently the only supported subsystem is historian.

h = get_historian("instancename")
h.listDataTags()
"""

from __future__ import (absolute_import, division, print_function, unicode_literals)
import pkg_resources
from eigeningenuity.historian import get_historian, list_historians, get_default_historian_name

from eigeningenuity.core import *

__all__ = ["get_historian", "list_historians", "get_default_historian_name"]
__version__ = pkg_resources.require("python-eigen-ingenuity")[0].version
