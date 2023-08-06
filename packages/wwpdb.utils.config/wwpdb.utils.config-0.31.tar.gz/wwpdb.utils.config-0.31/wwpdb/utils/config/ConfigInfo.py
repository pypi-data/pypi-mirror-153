##
# File:    ConfigInfo.py
# Date:    28-Mar-2010
#
# Updates:
#
# 27-Apr-2010 jdw Allow site Id to be set in the constructor.
# 29-Jun-2011 jdw Print configuration error if site id is neither provided in the constructor
#                 or provided in the environment
# 18-Jun-2012 jdw add function to set site id from the environment
# 25-Feb-2013 jdw correct typo in diagnostic message
# 11-Jul-2016 jdw add optional default return value for get()
#
##
"""
Provides access to shared and site-specific configuration information for the common deposition and annotation
system.

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import os
import sys

from wwpdb.utils.config.ConfigInfoData import ConfigInfoData


def getSiteId(defaultSiteId=None):
    """Obtain the site information from the environment or failover to the development site id."""
    siteId = str(os.getenv("WWPDB_SITE_ID", defaultSiteId))
    if siteId is None:
        siteId = "WWPDB_DEPLOY"
    return siteId


class ConfigInfo(object):
    """Provides access to site-specific configuration information for the common
    deposition and annotation system.

    Configuration data is stored in a dictionary of key value pairs.

    Configuration data is defined in class ConfigInfoData().

    SiteId provided in the constructor overrides any value in the environment.

    """

    def __init__(self, siteId=None, verbose=True, log=sys.stderr):
        self.__siteId = siteId
        self.__verbose = verbose
        self.__lfh = log

        if self.__siteId is None:
            self.__siteId = str(os.getenv("WWPDB_SITE_ID", None)).upper()
            """The site identification is obtained from the environmental variable `WWPDB_SITE_ID`
            """
        if self.__siteId is None:
            self.__lfh.write("++ERROR - ConfigInfo()  no site identifier in constructor or WWPDB_SITE_ID in environment.\n")

        self.__sI = ConfigInfoData(siteId=self.__siteId, verbose=self.__verbose)
        self.__D = self.__sI.getConfigDictionary()

    def get(self, keyWord, default=None):
        """Returns the site-specific value assigned to the input keyword or the default value -"""
        if keyWord is not None and keyWord in self.__D:
            return self.__D[keyWord]
        else:
            return default

    def dump(self, ofh):
        """Print the current configuration dictionary ."""
        for ky in sorted(self.__D.keys()):
            ofh.write("+ConfigInfo.dump() key: %-40s   value: %s\n" % (ky, self.__D[ky]))
