##
# File:    ConfigInfoSiteAccess.py
# Date:    6-Apr-2016
#
# Updates:
#         17-May-2016 jdw add getSiteDownTimeRange()
#         17-May-2016 jdw add  getCorrespondenceService()
#          1-Jun-2016 jdw add getForwardingService()
##
"""
Provides accessors for deposition site availability/unavailability information.

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import sys
import json
import datetime
import logging

try:
    from urllib.request import urlopen
    from urllib.error import HTTPError, URLError
except ImportError:  # pragma: no cover
    from urllib2 import urlopen, HTTPError, URLError
import ssl
import traceback
from wwpdb.utils.config.ConfigInfo import ConfigInfo
from wwpdb.utils.config.ConfigInfoApp import ConfigInfoAppDepUI

logger = logging.getLogger(__name__)


class ConfigInfoSiteAccess(object):
    """
    Provides accessors for service endpoints and deposition site availability/unavailability information.

    Configuration options -

    'SITE_ACCESS_INFO_FILE_PATH' points to file providing site unavailability schedule

    'PROJECT_DEPOSIT_SERVICE_DICTIONARY' option dictionary containing deposition site-to-service url mapping
    'PROJECT_CORRESPOND_SERVICE_DICTIONARY' option dictionary containing correspondence archiving site-to-service url mapping
    'PROJECT_FORWARDING_SERVICE_DICTIONARY' option dictionary containing message forwarding site-to-service url mapping

    """

    def __init__(self, verbose=False, log=sys.stderr):
        self.__verbose = verbose
        self.__lfh = log
        self.__debug = True
        self.__cI = ConfigInfo(siteId=None, verbose=self.__verbose)
        self.__cICommon = ConfigInfoAppDepUI()
        self.__serviceD = self.__cI.get("PROJECT_DEPOSIT_SERVICE_DICTIONARY")
        self.__siteAccessD = None

    def getCorrespondenceService(self, siteId):
        """Get the correspondence archiving service end point for the input site -

        Return the service URL or None

        """
        serviceD = self.__cI.get("PROJECT_CORRESPOND_SERVICE_DICTIONARY")
        if serviceD is None:
            return None

        if siteId in serviceD:
            return serviceD[siteId]
        else:
            return None

    def getForwardingService(self, siteId):
        """Get the message forwarding service end point for the input site -

        Return the service URL or None

        """
        serviceD = self.__cI.get("PROJECT_FORWARDING_SERVICE_DICTIONARY")
        if serviceD is None:
            return None

        if siteId in serviceD:
            return serviceD[siteId]
        else:
            return None

    def __getAccessDictionary(self):
        """Fetch the dictionary cotaining exceptional access information for each site
        expressed as the time interval when the site is not available.    Times are
        encoded as timestamps in UTC.

             Returns: d[<site_id>] = ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M")
                                           UTC begin        UTC end
        """
        fp = self.__cICommon.get_site_access_info_file_path()
        try:
            with open(fp, "r") as infile:
                return json.load(infile)
        except Exception as e:
            if self.__verbose:
                logger.error("failed reading json resource file %s %s", fp, str(e))
            if self.__debug:
                logger.exception("failed in parsing file %s", fp)
        return {}

    def isServiceReachable(self, siteId, timeout=2):
        # This restores the same behavior as before.
        context = ssl._create_unverified_context()  # pylint: disable=protected-access
        url = None
        if siteId in self.__serviceD:
            url = self.__serviceD[siteId]
        else:
            if self.__verbose:
                logger.info("no service url defined for site %s", siteId)
            return False
        #
        scode = -1
        try:
            scode = urlopen(url, context=context, timeout=timeout).getcode()
            if scode < 402:
                return True
        except HTTPError as e:
            if e.code < 402:
                return True
        except URLError as e:  # pragma: no cover
            if self.__verbose:
                logger.info("site %s url %s error %s", siteId, url, str(e.reason))
        except Exception as e:  # pragma: no cover
            if self.__verbose:
                logger.error("site %s scode %r url %s\n", siteId, scode, url)
            if self.__debug:
                logger.exception("Detecting service available %s", str(e))
                traceback.print_exc(file=self.__lfh)

        return False

    def isSiteAvailable(self, siteId):
        """Check if there is scheduled downtime for the input deposition site.

        Return True if deposition site is available (i.e. no scheduled downtime)

        """
        if self.__siteAccessD is None:
            self.__siteAccessD = self.__getAccessDictionary()

        if siteId in self.__siteAccessD:
            tBegin, tEnd = self.__siteAccessD[siteId]
            dtBegin = self.__getDateTimeUTC(tBegin)
            dtEnd = self.__getDateTimeUTC(tEnd)
            dtNow = datetime.datetime.utcnow()  # .replace(tzinfo=tz.tzutc())
            if self.__debug:
                logger.debug("site %s time begin %s  seconds %r", siteId, tBegin, dtBegin.strftime("%s"))
                logger.debug("site %s time end   %s  seconds %r", siteId, tBegin, dtBegin.strftime("%s"))
                logger.debug("current time   seconds %r\n", dtNow.strftime("%s"))
            if dtNow > dtBegin and dtNow < dtEnd:
                return False
        return True

    def getSiteDownTimeRange(self, siteId):
        """Get the scheduled down time range for the input site.

        Return tuple of timestamps (UTC) or (None,None)

        """
        if self.__siteAccessD is None:
            self.__siteAccessD = self.__getAccessDictionary()

        if siteId in self.__siteAccessD:
            tBegin, tEnd = self.__siteAccessD[siteId]
            if self.__debug:
                logger.debug("site %s time begin %s  time end %s\n", siteId, tBegin, tEnd)
            return (tBegin, tEnd)
        else:
            return (None, None)

    def __getDateTimeUTC(self, dateTimeStamp):
        # Converts datetie to UTC
        dt = datetime.datetime.strptime(dateTimeStamp, "%Y-%m-%d %H:%M:%S")
        return dt
