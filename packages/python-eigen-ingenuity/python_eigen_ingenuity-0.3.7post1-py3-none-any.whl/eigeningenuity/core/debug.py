
from __future__ import (absolute_import, division, print_function, unicode_literals)

import sys, os

debuglevels = {"CRITICAL": 1, "ERROR": 2, "WARNING":3, "INFO":4, "DEBUG":5, "TRACE":6}

def _debug(debuglevelstr, message):
    """Checks for current level of debug requested, and prints message on condition that the level is met or exceeded"""
    userrequestlevelstr = os.getenv("DEBUG")
    if userrequestlevelstr:  
        if (userrequestlevelstr == "0") or (userrequestlevelstr == "no"):
            userrequestlevelstr = "ERROR"
        elif (userrequestlevelstr == "1") or (userrequestlevelstr == "yes"):
            userrequestlevelstr = "DEBUG"
    else:
        userrequestlevelstr = "ERROR" 
    try:
        requestedlevel = debuglevels.get(userrequestlevelstr)
    except KeyError:
        raise EigenException("Unable to recognise this DEBUG option " + userrequestlevelstr)

    try:
        debuglevel = debuglevels.get(debuglevelstr)
    except KeyError:
        raise EigenException("Unable to recognise this DEBUG option " + userrequestlevelstr)

    if requestedlevel > debuglevel:
        sys.stderr.write(message + "\n")
