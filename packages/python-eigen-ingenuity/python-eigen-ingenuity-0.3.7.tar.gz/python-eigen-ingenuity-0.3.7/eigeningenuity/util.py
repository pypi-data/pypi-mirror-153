
from __future__ import (absolute_import, division, print_function, unicode_literals)

import sys, os, json, time, datetime, ssl, re
from urllib.parse import quote as urlquote
from urllib.request import urlopen
from urllib.request import Request as UrlRequest
from urllib.error import HTTPError,URLError

from eigeningenuity.core.debug import _debug

DISABLESSLCHECK = os.getenv("EIGENDISABLESSLCHECK") != ""
def disableSslChecks():
    global DISABLESSLCHECK
    DISABLESSLCHECK = True

_JSONQUERYCACHE = {}
def _do_eigen_json_request(requesturl, _cachetime = 0, _disablessl = None, **params):
    if _disablessl is None:
        _disablessl = DISABLESSLCHECK

    now = time.time()

    # Cache housekeeping
    for k, e in list(_JSONQUERYCACHE.items()):
        if e[1] < now:
           del _JSONQUERYCACHE[k]

    if params:
        if "?" in requesturl:
            sep = "&"
        else:
            sep = "?"

        for k,v in params.items():
            if v is None:
               pass
            else:
               for e in force_list(v):
                  if not isinstance(e, str):
                      if isinstance(e, str):
                          e = e.encode("utf8")
                      else:
                          e = str(e)
                  requesturl += sep + urlquote(k) + "=" + urlquote(e.encode("UTF8"))

                  sep = "&"

    if _cachetime > 0:
       try:
          val, expiry = _JSONQUERYCACHE[requesturl]
          if expiry > now:
              return val
       except:
          pass

    _debug("DEBUG",requesturl)
    if 'DEBUG' in os.environ and os.environ['DEBUG']:
        print("DEBUG: [" + requesturl + "]", file=sys.stderr)

    req = UrlRequest(requesturl)
    req.add_header('X-EPM-Referer', os.path.basename(sys.argv[0]))

    try:
        ctx = ssl.create_default_context()
        if _disablessl:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

        try:
            try:
                c = urlopen(req, context=ctx)
            except URLError:
                raise URLError("Could not find an ingenuity instance at: " + requesturl.split("eigenpluscore")[0]
                               + ", no valid response from " + requesturl)
            data = ""
            for line in c.readlines():
                data += line.decode("UTF8")
        except (RuntimeError,HTTPError) as e:
            raise map_java_exception(e, requesturl)
    except (TypeError, AttributeError) as e: # Note: earlier Python has no SSL checking support
        try: 
            c = urlopen(req)
            data = "".join(map(lambda s: s.decode("UTF8"), c.readlines()))
        except (RuntimeError, HTTPError) as e:
            raise map_java_exception(e, requesturl)

    if data.startswith("ERROR:"):
        raise RemoteServerException(data[6 : ].split("\n")[1],requesturl)
    elif data.startswith("EXCEPT:"):
        raise RemoteServerException(requesturl, data[7 : ])
    else:
        try:
            ret = json.loads(data)
        except ValueError:
            ret = data

    if _cachetime > 0:
        _JSONQUERYCACHE[requesturl] = [ret, time.time() + _cachetime]

    return ret

def is_list(x):
    return type(x) in (list, tuple, set)

def force_list(x):
    if is_list(x):
        return x
    else:
        return [x]

def number_to_string(n):
    if type(n) == float:
        return format(n, '^12.5f')
    else:
        return n

def time_to_epoch_millis(t):
    if type(t) == datetime.datetime:
        epochmillis = time.mktime(t.timetuple()) * 1000
    elif type(t) == tuple:
        epochmillis = time.mktime(t) * 1000
    elif type(t) == int:
        epochmillis = t
    elif type(t) == float:
        epochmillis = int(t * 1000)
    elif type(t) == int:
        epochmillis = t
    else:
        raise EigenException("Unknown time format " + str(type(t)))
    return int(round(epochmillis))

def get_time_tuple(floatingpointepochsecs):
    time_tuple = time.gmtime(floatingpointepochsecs)
    return time_tuple

def get_timestamp_string(t):
    pattern = '%Y-%m-%d %H:%M:%S UTC'
    s = datetime.datetime.fromtimestamp(t).strftime(pattern)
    return s

def get_timestamp(t):
    if type(t) == str or type(t) == str:
        try:
            pattern = '%Y-%m-%d %H:%M:%S.%f'
            epochmillis = time.mktime(time.strptime(t, pattern))
        except ValueError:
            try:
                pattern = '%Y-%m-%d %H:%M:%S'
                epochmillis = time.mktime(time.strptime(t, pattern))
            except ValueError:
                try:
                    pattern = '%Y-%m-%d'
                    epochmillis = time.mktime(time.strptime(t, pattern))
                except ValueError:
                    try:
                        epochmillis = int(t)
                    except ValueError:
                        raise EigenException("Unknown time format " + str(type(t)))

    else:
        epochmillis = time_to_epoch_millis(t)
    return epochmillis


def get_datetime(t):
    timestamp = get_timestamp(t)
    return datetime.datetime.fromtimestamp(timestamp)

def pythonTimeToServerTime(ts):
# where ts may be supplied as time tuple, datetime or floating point seconds, and server time is (obviously) millis.
    if type(ts) == datetime.datetime:
        epochmillis = time.mktime(ts.timetuple()) * 1000
    elif type(ts) == tuple:
        epochmillis = time.mktime(ts) * 1000
    elif type(ts) == float:
        epochmillis = int(ts * 1000)
    else:
        raise EigenException("Unknown python time format " + str(type(ts)))
    return int(round(epochmillis))


def serverTimeToPythonTime(ts):
# where ts is millis and the returned value is consistently whatever we're using internally in the python library (i.e. floating secs)
    return ts / 1000.0

def pythonTimeToFloatingSecs(ts):
# where ts may be supplied as time tuple, datetime or floating point seconds
    if type(ts) == datetime.datetime:
        return time.mktime(ts.timetuple())
    elif type(ts) == tuple:
        return time.mktime(ts)
    elif type(ts) == float:
        return ts
    else:
        raise EigenException("Unknown python time format " + str(type(ts)))

def pythonTimeToTuple(ts):
# where ts may be supplied as time tuple, datetime or floating point seconds
    if type(ts) == datetime.datetime:
        return ts.timetuple()
    elif type(ts) == tuple:
        return ts
    elif type(ts) == float:
        return ts
    else:
        raise EigenException("Unknown python time format " + str(type(ts)))

def pythonTimeToDateTime(ts):
# where ts may be supplied as time tuple, datetime or floating point seconds
    if type(ts) == datetime.datetime:
        return ts
    elif type(ts) == tuple:
        epochmillis = time.mktime(ts) * 1000
        return datetime.datetime.fromtimestamp(epochmillis)
    elif type(ts) == float:
        return time.gmtime(ts)
    else:
        raise EigenException("Unknown python time format " + str(type(ts)))

def map_java_exception(myExceptionName, params):
    if myExceptionName == "urllib2.HTTPError":
         return RemoteServerException(params)
#    elif: ...
    else:
        return EigenException(myExceptionName)

def parse_duration(timeWindow):
    unit = timeWindow[-1:]
    value = timeWindow[:-1]

    def seconds():
        int(value)

    def minutes():
        return int(value) * 60

    def hours():
        return int(value) * 3600

    def days():
        return int(value) * 3600 * 24

    def months():
        return int(value) * 3600 * 24 * 30

    def years(): int(value) * 3600 * 24 * 365

    options = {"s" : seconds,
               "m" : minutes,
               "h" : hours,
               "d" : days,
               "M" : months,
               "y" : years,
    }

    duration = options[unit]()

    return duration * 1000


class EigenException (Exception): pass
class RemoteServerException (EigenException): pass
