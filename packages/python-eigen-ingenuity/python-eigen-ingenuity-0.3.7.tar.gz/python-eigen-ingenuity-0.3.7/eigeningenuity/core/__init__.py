"""Eigen Ingenuity - Core Functions

This module deals with basic common tasks to do with interacting with an
Eigen Ingenuity server.

In order to find a particular subsystem ("app"), you can use e.g.

   ei = EigenServer(servername)
   ei.get_historian(datasource)

If no server name or URL is given it searches sys.argv for a --eigenserver
argument, falling back on the environment variable EIGENSERVER.
This may either be in the form of a URL (http://foo:8087/) or a
hostname, or hostname:port combination. If no variable is set, it defaults
to http://localhost:8080/
"""

from __future__ import (absolute_import, division, print_function, unicode_literals)

import sys, os
from eigeningenuity.util import _do_eigen_json_request, EigenException, RemoteServerException, serverTimeToPythonTime

_INSTANCE = None
class EigenServer (object):
    def __init__(self, name = None, disableSsl = False):
        """Find the base URL for the Eigen Ingenuity server.
        """
        if name is None:
            try:
                for i in range(len(sys.argv)):
                    arg = sys.argv[i]
    
                    if arg.startswith("--eigenserver="):
                        name = arg[14 : ]
                        break
                    elif arg == "--eigenserver":
                        name = sys.argv[i + 1]
                        break
                else:
                    name = os.environ['EIGENSERVER']
            except:
                pass
        
        try:
            if name.startswith("http://") or name.startswith("https://"):
                if name.endswith("/"):
                    baseurl = name
                else:
                    baseurl = name + "/"
            else:
                baseurl = "http://" + name + "/"
        except:
            baseurl = "http://localhost:8080/"

        self.__baseurl = baseurl
        self.__disablessl = disableSsl


    def getEigenServerUrl(self):
        """Find the base URL for the Eigen Ingenuity server.
        """
        return self.__baseurl
    
    def getAppsInfo(self):
        """Request information about install Eigen Ingenuity apps/components.
        """
        return  _do_eigen_json_request(self.__baseurl + "eigenpluscore-servlet/prodseminfo", cmd = "GETAPPS", _cachetime = 10)
    
    def listApps(self):
        return list(self.getAppsInfo().keys())
    
    def getAppUrl(self, appname):
        """Find the base URL for a specified Eigen Ingenuity apps. Note this is
        something like "historian-servlet" not "trend" or "jsonbridgehistorian".
        Think "module" rather than "tool".
        Returns None if the app is not installed.
        """
        apps = self.getAppsInfo()
        if appname in apps:
           # Remove leading / from appname if present
           appurl = apps[appname]['url']
           if appurl.startswith('/'):
              appurl = appurl[1:]

           return self.__baseurl + appurl
        else:
           return None
    
    def listDataSourceTypes(self):
        """Request information about installed Eigen Ingenuity Factory Types.
        """
        return  _do_eigen_json_request(self.__baseurl + "eigenpluscore-servlet/prodseminfo", cmd = "LISTFACTORYTYPES", _cachetime = 10)
    
    def listDataSources(self, type):
        """List the instances for a specified Eigen Ingenuity Factory Type
        Returns None if there are no instances
        """
        data_source_types = self.listDataSourceTypes()
        if type in data_source_types:
           args = {}
           args['cmd'] = "LISTFACTORYINSTANCES"
           args['type'] = type
           return  _do_eigen_json_request(self.__baseurl + "eigenpluscore-servlet/prodseminfo", **args)
        else:
           return None
    
    def getDefaultDataSource(self, type):
        """Gets the default instance for the named Factory Type. Returns None if none has been specified."""
        data_source_types = self.listDataSourceTypes()
        if type in data_source_types:
            args = {}
            args['cmd'] = "GETDEFAULTFACTORYINSTANCE"
            args['type'] = type
            try: 
                return  _do_eigen_json_request(self.__baseurl + "eigenpluscore-servlet/prodseminfo", **args)
            except RemoteServerException:
                return None
        else:
            return None
    
    def listFeatureProperties(self):
        """Request information about installed Eigen Ingenuity Feature Properties.
        """
        return  _do_eigen_json_request(self.__baseurl + "eigenpluscore-servlet/prodseminfo", cmd = "LISTFEATUREPROPERTIES")
    
    def getFeatureProperty(self, property):
        """Get the value of the specified Eigen Ingenuity Feature Property
        """
        args = {}
        args['cmd'] = "GETFEATUREPROPERTY"
        args['property'] = property
        try:
            return  _do_eigen_json_request(self.__baseurl + "eigenpluscore-servlet/prodseminfo", **args)
        except RemoteServerException:
            return None
    
    def getServerTimeInFloatingPointMillis(self):
        """Get the current time from the Server in floating point milliseconds.
        """
        args = {}
        args['cmd'] = "GETSERVERTIME"
        try:
            ts = _do_eigen_json_request(self.__baseurl + "eigenpluscore-servlet/prodseminfo", **args)
            return serverTimeToPythonTime(ts)
        except RemoteServerException:
            return None
    
    def getServerTimezone(self):
        """Get the current timezone and DST status from the Server
        """
        args = {}
        args['cmd'] = "GETSERVERTIMEZONE"
        try:
            tz = _do_eigen_json_request(self.__baseurl + "eigenpluscore-servlet/prodseminfo", **args)
            return tz
        except RemoteServerException:
            return None

    def getHistorian(self, *args, **kwargs):
        from eigeningenuity.historian import get_historian
        return get_historian(*args, eigenserver=self, **kwargs)
    
    def getAssetModel(self, *args, **kwargs):
        from eigeningenuity.assetmodel import get_assetmodel
        return get_assetmodel(*args, eigenserver=self, **kwargs)
    
    def getSmartdash(self, *args, **kwargs):
        from eigeningenuity.smartdash import get_smartdash
        return get_smartdash(*args, eigenserver=self, **kwargs)
    
    def getDebugletsForApp(self, *args, **kwargs):
        from eigeningenuity.debuglets import get_debuglets_for_app
        return get_debuglets_for_app(*args, eigenserver=self, **kwargs)
    
    def getDebuglets(self, *args, **kwargs):
        from eigeningenuity.debuglets import get_debuglets
        return get_debuglets(*args, eigenserver=self, **kwargs)
    
def get_default_server():
    global _INSTANCE

    if _INSTANCE is None:
        _INSTANCE = EigenServer()

    return _INSTANCE

def get_eigenserver_url():
    return get_default_server().getEigenserverUrl()

def get_apps_info():
    return get_default_server().getAppsInfo()
    
def list_apps():
    return get_default_server().listApps()

def get_app_url(appname):
    return get_default_server().getAppUrl(appname)

def list_data_source_types():
    return get_default_server().listDataSourceTypes()

def list_data_sources(type):
    return get_default_server().listDataSources(type)
    
def get_default_data_source(type):
    return get_default_server().getDefaultDataSource(type)

def list_feature_properties():
    return get_default_server().listFeatureProperties()

def get_feature_property(property):
    return get_default_server().getFeatureProperty(property)

def get_server_time_in_floating_point_millis():
    return get_default_server().getServerTimeInFloatingPointMillis()

def get_server_timezone():
    return get_default_server().getServerTimezone()
