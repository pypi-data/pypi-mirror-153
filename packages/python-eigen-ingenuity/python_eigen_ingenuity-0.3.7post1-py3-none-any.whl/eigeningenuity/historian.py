"""Eigen Ingenuity - Historian

This package deals with the Eigen Ingenuity Historian API, mostly by means
of the JSON Bridge Historian.

To get a historian object to work with, use get_historian(xxx) with either
an instance name (which will be resolved via the the usual methods in
eigeningenuity.core) or a full URL to a JSON Bridge Historian instance.

  from eigeningenuity.historian import get_historian
  from time import gmtime, asctime

  h = get_historian("pi-opc")
  tags = h.listDataTags()
  
  for tag in tags:
      dp = h.getCurrentDataPoint(tag)
      print(asctime(time.gmtime(dp['timestamp'])), dp['value'])  

"""

from __future__ import (absolute_import, division, print_function, unicode_literals)

import logging
import sys, os, json, datetime, math
from urllib.parse import quote as urlquote

from eigeningenuity.core import get_default_server
from eigeningenuity.util import _do_eigen_json_request, force_list, time_to_epoch_millis, is_list, get_datetime, number_to_string, EigenException, get_timestamp_string, pythonTimeToFloatingSecs, serverTimeToPythonTime, pythonTimeToServerTime, get_time_tuple, parse_duration

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

class Historian (object):
    """A class implementing the Eigen Ingenuity Historian API"""
    def listDataTags(self, wildcards = None):
        """List all tags in Historian, or those matching the wildcard if one is given"""
        raise NotImplementedError()

    def getMetaData(self, tags):
        """Returns name, description and units for each tag"""
        raise NotImplementedError()

    def getCurrentDataPoints(self, tags):
        """Return latest data point for each tag"""
        raise NotImplementedError()

    def getInterpolatedPoints(self, tags, timestamps):
        """Return interpolated datapoints for each timestamp on each tag"""
        raise NotImplementedError()

    def getRawDataPoints(self, tags, start, end, maxpoints = 1000):
        """Return raw datapoints between start and end timestamp for each tag, up to maxpoints"""
        raise NotImplementedError()

    def getInterpolatedRange(self, tags, start, end, count):
        """Return count number of interpolated datapoints between start and end timestamp for each tag"""
        raise NotImplementedError()

    def getAggregates(self, tags, start, end, count, fields):
        """Returns min, max, avg, numgood, numnotgood, stddev and variance
        """
        raise NotImplementedError()

    def countPoints(self, tags, start, end):
        """Returns count of points in time range
        """
        raise NotImplementedError()

    def createDataTag(self, tag, units):
        """Creates a datatag with units"""
        raise NotImplementedError()

    def writeDataPoints(self, data):
        """Write datapoints to the Historian. data is a map of tag name
           to list of DataPoint.
        """
        raise NotImplementedError()

class JsonBridgeHistorian (Historian):
    """A Historian which talks the Eigen Historian Json Bridge protocol.
    """
    def __init__(self, baseurl):
       """This is a constructor. It takes in a URL like http://infra:8080/historian-servlet/jsonbridge/influxdb-dev1"""
       self.baseurl = baseurl

    def listDataTags(self, wildcards = None):
        args = {}
        if wildcards is not None:
            args['match'] = force_list(wildcards)

        response = self._doJsonRequest("list", args)
        return response

    def getMetaData(self, tags):
        ret = {}
        for tag in force_list(tags):
            args = {}
            args['tag'] = tag
            response = self._doJsonRequest("getmeta", args)
            ret[tag] = response

        return self._matchArgumentCardinality(tags, ret)


    def getCurrentDataPoints(self, tags):
        args = {}
        args['tag'] = force_list(tags)
        response = self._doJsonRequest("getmulticurrent", args)
        ret = {}
        items = response["items"]
        for tagname in items:
            point = items[tagname]
            ret[tagname] = self._makeDataPointFromJson(point)

        return self._matchArgumentCardinality(tags, ret)

    def getInterpolatedPoints(self, tags, timestamps):
        args = {}
        args['tag'] = force_list(tags)
        args['timestamp'] = force_list(timestamps)
        response = self._doJsonRequest("getmulti", args)
        items = response['items']
        ret = {}
        for tagname in items:
            ret[tagname] = []
            points = items[tagname]
            for point in points:
                ret[tagname].append(self._makeDataPointFromJson(point))


        return self._matchArgumentCardinality(tags, ret)

    def getRawDataPoints(self, tags, start, end, maxpoints = 1000):
        args = {}
        args['tag'] = force_list(tags)
        args['start'] = time_to_epoch_millis(start)
        args['end'] = time_to_epoch_millis(end)
        args['maxpoints'] = maxpoints
        response = self._doJsonRequest("getraw", args)

        ret = {}
        items = response["items"]
        for tagname in items:
            ret[tagname] = []
            points = items[tagname]
            for point in points:
                ret[tagname].append(self._makeDataPointFromJson(point))

        try:
            if response["truncated"]:
                raise DataPointLimitExceededException("Exceeded Data Limit", response)
        except KeyError:
            pass

        return self._matchArgumentCardinality(tags, ret)

    def getInterpolatedRange(self, tags, start, end, count):
        args = {}
        args['tag'] = force_list(tags)
        args['start'] = time_to_epoch_millis(start)
        args['end'] = time_to_epoch_millis(end)
        args['count'] = count
        response = self._doJsonRequest("getrange", args)

        ret = {}
        items = response['items']
        for tagname in items:
            ret[tagname] = []
            points = items[tagname]
            for point in points:
                ret[tagname].append(self._makeDataPointFromJson(point))

        return self._matchArgumentCardinality(tags, ret)

    def getAggregates(self, tags, start, end, count=1, fields=None):
        args = {}
        args['tag'] = force_list(tags)
        args['start'] = time_to_epoch_millis(start)
        args['end'] = time_to_epoch_millis(end)
        args['count'] = count
        args['aggfields'] = fields
        response = self._doJsonRequest("getagg", args)
        ret = {}
        for tagname in response:
            ret[tagname] = []
            sets = response[tagname]
            for agg in sets:
                ret[tagname].append(self._makeAggregateDataSetFromJson(agg))

        return self._matchArgumentCardinality(tags, ret)

    def getAggregateIntervals(self, tags, start, end, window=False, fields=None):

        epoch_ms_start = time_to_epoch_millis(start)
        epoch_ms_end = time_to_epoch_millis(end)

        if window:
            windowDuration = parse_duration(window)
            totalDuration = epoch_ms_end - epoch_ms_start

            count = math.floor(totalDuration/windowDuration)

            epoch_ms_end = epoch_ms_end - totalDuration%windowDuration
        else:
            count = 1

        args = {}
        args['tag'] = force_list(tags)
        args['start'] = epoch_ms_start
        args['end'] = epoch_ms_end
        args['count'] = count
        args['aggfields'] = fields
        response = self._doJsonRequest("getagg", args)
        ret = {}
        for tagname in response:
            ret[tagname] = []
            sets = response[tagname]
            for agg in sets:
                ret[tagname].append(self._makeAggregateDataSetFromJson(agg))

        return self._matchArgumentCardinality(tags, ret)

    def countPoints(self, tags, start, end):
        ret = {}
        aggs = self.getAggregates(force_list(tags), start, end, 1, "COUNT")
        for tag in list(aggs.keys()):
            ret[tag] = aggs[tag][0].getCount()

        return self._matchArgumentCardinality(tags, ret)

    def writeDataPoints(self, data):
        rawdata = {}
        for tag in list(data.keys()):
            rawdps = []
            for dp in force_list(data[tag]):
                rawdps.append([int(dp.getTimestamp()*1000), dp.getValue(), dp.getStatus()])
            rawdata[tag] = rawdps

        return self._doJsonRequest("write", {'write': json.dumps(rawdata)})

    def createDataTag(self, tag, units, description):
        args = {}
        args['tag'] = tag
        args['units'] = units
        args['description'] = description
        return self._doJsonRequest("create", args)

    def _doJsonRequest(self, cmd, params):
        url = self.baseurl + "?cmd=" + urlquote(cmd)
        return _do_eigen_json_request(url, **params)

    def _matchArgumentCardinality(self, proto, ret):
        """Takes in ret (a dict) and proto. If proto is a list, it returns
        ret. If proto is a single value, it extracts that key from ret and
        returns that instead.
        The intention is that:
            getTagThing("myTag") returns Thing for myTag
            getTagThing(["myTag", "myOtherTag"]) returns {'myTag': Thing, 'myOtherTag': OtherThing}
        and for clarification:
            getTagThing(["myTag"]) returns {'myTag': Thing}
        """
        try:
            badTags = []
            if is_list(proto):
                if ret != {}:
                    if len(ret) < len(proto):
                        for i in proto:
                            if i not in ret:
                                badTags.append(i)
                        logging.warning("One or more tags were not found: " + str(badTags))
                    return ret
                else:
                    raise KeyError
            else:
                return ret[proto]
        except KeyError:
            raise KeyError("Could not find tag(s): " + str(proto))

    def _makeDataPointFromJson(self, json):
        """Assumes the incoming timestamp in the jsonstring is in milliseconds, so converts to floating point seconds"""
        value = json["value"]
        timestampinmillis = json["timestamp"]
        timestamp = serverTimeToPythonTime(timestampinmillis)
        status = json["status"]
        return DataPoint(value, timestamp, status)


    def _makeAggregateDataSetFromJson(self, json):
        """Assumes the incoming start and end timestamps in the jsonstring are in milliseconds, so convert to floating point seconds"""
        start = serverTimeToPythonTime(json["start"])
        del json["start"]
        end = serverTimeToPythonTime(json["end"])
        del json["end"]
        return AggregateDataSet(start, end, json)


#Attempt to create a DataPoint Class


class DataPoint (object):
    """This class represents a data point which has a value and a python timestamp, and optionally a status of 'OK' or 'BAD'.
       Timestamp is stored in epochseconds. The constructor will convert datetime and tuples into floating point epoch seconds.
    """

    def __init__(self, value, timestamp, status = 'OK'):
       """This constructor takes in a value, a python timestamp (epoch floating point seconds or datetime or tuple)
       and an optional status.  Status is either "OK" or "BAD" and will default to "OK"
       """

       self.value = value

       if status is None:
           self.status = "OK"
       elif status == "OK":
           self.status = status
       elif status == "BAD" :
           self.status = status
       else:
            raise EigenException("Unrecognised Status")

       # Convert timestamp from python datetime or tuple into python floating point epoch seconds
       self.datetime = datetime.datetime.fromtimestamp(timestamp)
       self.timestamp = pythonTimeToFloatingSecs(timestamp)

    def __str__(self):
        """Return a nicely formatted version of the datapoint"""
        val = self.value
        if type(val) != str:
            val = str(number_to_string(val))
        else:
            val = val.ljust(12)
        return val + " @ " + get_timestamp_string(self.timestamp) + " - " + self.status

    def __repr__(self):
        return "DataPoint[" + str(self) + "]"

    def getValue(self):
        """Return the value of the datapoint"""
        return self.value

    def getTimestamp(self):
        """Return the timestamp of the datapoint in python floating point epoch seconds"""
        return self.timestamp

    def getTimestampMillis(self):
        """Return the timestamp of the datapoint in epochmillis"""
        return pythonTimeToServerTime(self.timestamp)

    def getTimestampAsDatetime(self):
        """Return the timestamp of the datapoint as Datetime"""
        return get_datetime(self.timestamp)

    def getTimestampAsTuple(self):
        """Return the timestamp of the datapoint as Tuple"""
        return get_time_tuple(self.timestamp)

    def getStatus(self):
        """Return the status of the datapoint - either 'OK' or 'BAD'"""
        return self.status

    def isBad(self):
        """Returns either True if status = "BAD" or false if status = "OK" """
        return self.status != "OK"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def getAsJson(self):
        """Return as a json map with the timestamp in milliseconds"""
        return "{" + "\"value\":" + str(self.value) + ",\"timestamp\":" + self.getTimestampMillis(self) + ",\"status\":\"" + self.status + "\"}"

def get_datapoint(dp):
    value = dp["value"]
    timestamp = dp["timestamp"]
    timestampinmillis = dp["timestamp"]
    timestamp = serverTimeToPythonTime(timestampinmillis)
    status = dp["status"]
    return DataPoint(value, timestamp, status)


class AggregateDataSet (object):
    """This class represents an aggregate data set which has a start and end (in floating point epoch seconds) and a set of aggregate fields.
       Double min
       Double max
       Double avg
       Double variance - defaults to 0.0
       Double stddev - defaults to 0.0
       long numGood
       long numNotGood
    """

    def __init__(self, start, end, aggfields = {}):
       """This constructor takes python start and end timestamps (epoch floating point seconds or datetime or tuple)
       and an dict of aggregate fields.
       """
       self.min = aggfields.get("min")
       self.max = aggfields.get("max")
       self.avg = aggfields.get("avg")
       self.var = aggfields.get("var",0.0)
       self.stddev = aggfields.get("stddev",0.0)
       self.numgood = aggfields.get("numgood")
       self.numnotgood = aggfields.get("numbad")
       self.count = aggfields.get("count")

       # Convert timestamp from python datetime or tuple into python floating point epoch seconds
       self.start = pythonTimeToFloatingSecs(start)
       self.end = pythonTimeToFloatingSecs(end)

    def __str__(self):
        """Return a nicely formatted version of the aggregate"""
        return " start:" + get_timestamp_string(self.start) + " end:" + get_timestamp_string(self.end) + " - " \
               + "min: " + str(number_to_string(self.min)) + "   " \
               + "max: " + str(number_to_string(self.max)) + "   " \
               + "avg: " + str(number_to_string(self.avg)) + "   " \
               + "var: " + str(number_to_string(self.var)) + "   " \
               + "stddev: " + str(number_to_string(self.stddev)) + "   " \
               + "numgood: " + str(number_to_string(self.numgood)) + "   " \
               + "numnotgood: " + str(number_to_string(self.numnotgood)) + "   "

    def __repr__(self):
        return "AggregateDataSet[" + str(self) + "]"

    def getCount(self):
        return self.count

    def getNumGood(self):
        """Return the number of good points."""
        return self.numgood

    def getNumBad(self):
        """Return the number of bad points."""
        return self.numnotgood

    def getMin(self):
        """Return the Minimum of the Aggregate DataSet"""
        return self.min

    def getStart(self):
        """Return the start of the aggregate data set in python floating point epoch seconds"""
        return self.start

    def getEnd(self):
        """Return the end of the aggregate data set in python floating point epoch seconds"""
        return self.end

    def getStartMillis(self):
        """Return the start date in epochmillis"""
        return pythonTimeToServerTime(self.start)

    def getEndMillis(self):
        """Return the end date in epochmillis"""
        return pythonTimeToServerTime(self.end)

    def getAsJson(self):
        """Return as a json map with the start and end in milliseconds"""
        return "{" + "\"start\":" + self.getStartMillis(self) + "," + "\"end\":" + self.getEndMillis(self) + "," \
               + "\"min\":" + self.min + "," \
               + "\"max\":" + self.max + "," \
               + "\"avg\":" + self.avg + "," \
               + "\"var\":" + self.var + "," \
               + "\"stddev\":" + self.stddev + "," \
               + "\"numgood\":" + self.numgood + "," \
               + "\"numnotgood\":" + self.numnotgood \
               + "\"}"

# def get_aggregate(agg):
#     start = serverTimeToPythonTime(agg["start"])
#     end = serverTimeToPythonTime(agg["end"])
#     aggfields = {}
#     aggfields["min"] = agg["min"]
#     return AggregateDataSet(start, end, aggfields)



class DataPointLimitExceededException (EigenException):

    def __init__(self, message, errors):

        items = []
        # Call the base class constructor with the parameters it needs
        super(EigenException, self).__init__(message)

        # Now for some custom code...
        self.errors = errors["truncated"]
        self.items = errors["items"]

    def getAllTags(self):
        allTags = list(self.items.keys()) + list(self.errors.keys())
        return allTags
    def getTruncatedTags(self):
        return list(self.errors.keys())
    def getUntruncatedTags(self):
        tags = list(self.items.keys()) 
        for tag in list(self.errors.keys()):
            tags.remove(tag)
        return tags
    def getEarliestTimestamp(self):
        for tagname in list(self.errors.keys()):
           thisTagEarliestTimestamp = serverTimeToPythonTime(self.errors[tagname]["earliesttimestamp"])
           if earliestTimestamp:
               if earliestTimestamp > thisTagEarliestTimestamp:
                      earliestTimestamp = thisTagEarliestTimestamp
           else:
               earliestTimestamp = thisTagEarliestTimestamp
        return earliestTimestamp
    def getEarliestTimestamp(self, tagname):
        earliestTimestamp = serverTimeToPythonTime(self.errors[tagname]["earliesttimestamp"])
        return earliestTimestamp
    def getLatestTimestamp(self):
        for tagname in list(self.errors.keys()):
           thisTagLatestTimestamp = serverTimeToPythonTime(self.errors[tagname]["latesttimestamp"])
           if latestTimestamp:
               if latestTimestamp < thisTagLatestTimestamp:
                      latestTimestamp = thisTagLatestTimestamp
           else:
               latestTimestamp = thisTagLatestTimestamp
        return latestTimestamp
    def getLatestTimestamp(self, tagname):
        latestTimestamp = serverTimeToPythonTime(self.errors[tagname]["latesttimestamp"])
        return latestTimestamp
    def getDataTag(self):
        raise NotImplementedError()
    def getNumPointsFound(self,tagname):
        numPoints = self.errors[tagname]["numberpointsfound"]
        return numPoints
    def getLimit(self,tagname):
        limit = self.errors[tagname]["limit"]
        return limit
    def getDataPoints(self):
        ret = {}
        for tagname in self.items:
            ret[tagname] = []
            points = self.items[tagname]
            for point in points:
                dp = get_datapoint(point) 
                ret[tagname].append(dp)
        return ret
    def getDataPoints(self,tagname):
        ret = []
        points = self.items[tagname]
        for point in points:
            dp = get_datapoint(point)
            ret.append(dp)
        return ret
    def getNextWindowStartTimestamp(self, tagname):
        latestTimestamp = serverTimeToPythonTime(self.errors[tagname]["latesttimestamp"])
        return latestTimestamp + 0.001 # 1ms later
    

def get_historian(instance = None, eigenserver = None):
    """Instantiate a historian object for the given instance
    """
    if eigenserver is None:
        eigenserver = get_default_server()
 
    if instance is not None and (instance.startswith("http:") or instance.startswith("https:")):
        return JsonBridgeHistorian(instance)

    if instance is None:
        instance = get_default_historian_name(eigenserver = eigenserver)
        if instance is None:
            raise EigenException ("No default historian instance found")

    return JsonBridgeHistorian(eigenserver.getAppUrl("historian-servlet") + "/jsonbridge/" + instance)

def list_historians(eigenserver = None):
    """List available historian instances."""
    if eigenserver is None:
        eigenserver = get_default_server()

    return eigenserver.listDataSources("historian")

def get_default_historian_name(eigenserver = None):
    """Returns the default historian"""
    if eigenserver is None:
        eigenserver = get_default_server()

    return eigenserver.getDefaultDataSource("historian") 


