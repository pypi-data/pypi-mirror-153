#!/usr/bin/env python
##
# File:    ConfigInfoFileExec.py
# Author:  jdw
# Date:    5-Apr-2016
# Version: 0.001
#
# Updates:
#   6-Apr-2016  jdw   add fallback resources describing locations and sites -
#   7-Apr-2016  jdw   add directory existence checks
#  10-May-2016  jdw   add support for additional private configuration sections.
#  14-May-2016  jdw   add install section and cache update by location
#   4-Dec-2016  jdw   new CLI option for adding extra option section names added to common name space
#                     The defaults for common sections are 'database_services' and 'validation_module'.
#
#                     The defaults for private namespaces include 'os_environment', 'httpd_services',
#                     and 'install_environment'
#  12-Apr-2017  jdw   add missing site-common and common configuration paths in search for private configuration sections.
#  11-Oct-2017  jdw   add back_server_* private section
#  05-Oct-2018   ep   add options to inject a mock environment variable into config. Add support for a R/O source tree and R/W cache directory
"""
Execuction wrapper for configuration option and cache file management.

"""

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.001"

import sys
import os
import traceback
import logging
from optparse import OptionParser, SUPPRESS_HELP  # pylint: disable=deprecated-module

from wwpdb.utils.config.ConfigInfoFile import ConfigInfoFile

logging.basicConfig(level=logging.INFO, format="[%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ConfigInfoFileExec(object):
    """
    Execuction wrapper for configuration option and cache file management.

    """

    def __init__(self, mockTopPath=None, sourceDirPath=None, verbose=True, log=sys.stderr):
        self.__lfh = log
        self.__verbose = verbose
        self.__debug = False
        self.__mockTopPath = mockTopPath
        #
        self.__topConfigPath = os.getenv("TOP_WWPDB_SITE_CONFIG_DIR", default=None)
        #
        if sourceDirPath:
            self.__sourceDirPath = sourceDirPath
        else:
            self.__sourceDirPath = self.__topConfigPath

        # Complete list of sections maintained as private namespaces
        self.__privateSectionNameList = []
        # additional configuration sections added to the common namespace
        self.__extraCommonSectionNameList = []

    def setPrivateSectionNames(self, sectionNameList):
        self.__privateSectionNameList = sectionNameList

    def __getPrivateSectionNames(self):
        return self.__privateSectionNameList

    def addCommonSectionNames(self, sectionNameList):
        self.__extraCommonSectionNameList = sectionNameList

    def __getExtraCommonSectionNames(self):
        return self.__extraCommonSectionNameList

    def testConfigPath(self, accessType="read"):
        #
        ok = True
        try:
            if self.__topConfigPath is None:
                ok = False
                self.__lfh.write("WARNING - TOP_WWPDB_SITE_CONFIG_DIR is not set in the environment.\n")
            elif accessType == "write" and not os.access(self.__topConfigPath, os.W_OK):
                ok = False
                self.__lfh.write("WARNING - %s lacks write access.\n" % self.__topConfigPath)
            elif accessType == "read" and not os.access(self.__topConfigPath, os.R_OK):
                ok = False
                self.__lfh.write("WARNING - %s lacks read access.\n" % self.__topConfigPath)
        except Exception as e:
            self.__lfh.write("testConfigPath failing %r\n" % str(e))
            traceback.print_exc(file=self.__lfh)
            ok = False

        return ok

    def __getCommonConfigPath(self, sectionName="common", context="common"):
        cfPath = os.path.join(self.__sourceDirPath, "common", "common.cfg")
        return cfPath, sectionName, context

    def __getSiteCommonConfigPath(self, siteLoc, sectionName="site_common", context="common"):
        cfPath = os.path.join(self.__sourceDirPath, siteLoc.lower(), "site_common", "common.cfg")
        return cfPath, sectionName, context

    def __getSiteConfigPath(self, siteLoc, siteId, sectionName, context="common"):
        cfPath = os.path.join(self.__sourceDirPath, siteLoc.lower(), siteId.lower(), "site.cfg")
        return cfPath, sectionName, context

    def __getSitePythonCachePath(self, siteLoc, siteId):
        cfPath = os.path.join(self.__topConfigPath, siteLoc.lower(), siteId.lower(), "ConfigInfoFileCache.py")
        return cfPath

    def __getSiteJsonCachePath(self, siteLoc, siteId):
        cfPath = os.path.join(self.__topConfigPath, siteLoc.lower(), siteId.lower(), "ConfigInfoFileCache.json")
        return cfPath

    def __getCommonConfig(self):
        """Return the project common configuration options as a dictionary.

        Really depends on config_as_object setting to deserialize dictionary ...
        """
        cD = {}
        try:
            cfPath, sectionName, context = self.__getCommonConfigPath(sectionName="common", context="common")  # pylint: disable=unused-variable
            cf = ConfigInfoFile(mockTopPath=self.__mockTopPath, verbose=self.__verbose, log=self.__lfh)
            tD = cf.readConfig(configFilePath=cfPath)
            if sectionName.upper() in tD:
                cD = cf.deserializeConfig(tD[sectionName.upper()], optionD=tD[sectionName.upper()])
        except Exception as e:
            self.__lfh.write("__getCommonConfig failing %r\n" % str(e))
            traceback.print_exc(file=self.__lfh)

        return cD

    def __getConfigPathSectionList(self, siteLoc, siteId, extraCommonSectionNameList, privateSectionNameList):
        """Returns the search path of sections and configuration file paths for the input location and site.
        The site specific configuration file path is always included.   The site-common or project common
        configuration files are included only if these exist.

        Any section names in extraCommonSectionNameList are added to path list for each configuration file -

        Returns: [(configPath,sectionName,context), (configPath,sectionName),context), ...]
        """
        cfPathSectionList = []
        if self.__topConfigPath is not None and siteId is not None and siteLoc is not None:
            (p, s, c) = self.__getSiteConfigPath(siteLoc=siteLoc, siteId=siteId, sectionName=siteId.lower())
            if p is not None and os.access(p, os.R_OK):
                cfPathSectionList.append((p, s, c))
                for cSec in extraCommonSectionNameList:
                    cfPathSectionList.append((p, cSec, "common"))
            (p, s, c) = self.__getSiteCommonConfigPath(siteLoc=siteLoc, sectionName="site_common")
            if p is not None and os.access(p, os.R_OK):
                cfPathSectionList.append((p, s, c))
                for cSec in extraCommonSectionNameList:
                    cfPathSectionList.append((p, cSec, "common"))
            (p, s, c) = self.__getCommonConfigPath(sectionName="common")
            if p is not None and os.access(p, os.R_OK):
                cfPathSectionList.append((p, s, c))
                for cSec in extraCommonSectionNameList:
                    cfPathSectionList.append((p, cSec, "common"))
            #
            # Additional context specific (private) configuration sections - stored in the site, site-common and common config paths
            #
            for sectionName in privateSectionNameList:
                (p, s, c) = self.__getSiteConfigPath(siteLoc=siteLoc, siteId=siteId, sectionName=sectionName, context="private")
                if p is not None and os.access(p, os.R_OK):
                    cfPathSectionList.append((p, s, c))
                #
                (p, s, c) = self.__getSiteCommonConfigPath(siteLoc=siteLoc, sectionName=sectionName, context="private")
                if p is not None and os.access(p, os.R_OK):
                    cfPathSectionList.append((p, s, c))

                (p, s, c) = self.__getCommonConfigPath(sectionName=sectionName, context="private")
                if p is not None and os.access(p, os.R_OK):
                    cfPathSectionList.append((p, s, c))

        return cfPathSectionList

    def __getSiteConfig(self, siteLoc, siteId, deserialize=True):
        """Return the complete site of configuration options for the input location and site."""
        cD = {}
        try:
            privateSectionNameList = self.__getPrivateSectionNames()
            extraCommonSectionNameList = self.__getExtraCommonSectionNames()
            pathSectList = self.__getConfigPathSectionList(siteLoc, siteId, extraCommonSectionNameList, privateSectionNameList)
            if self.__debug:
                self.__lfh.write("__getSiteConfig Path list for location %r site %r\n" % (siteLoc, siteId))
                for pTup in pathSectList:
                    self.__lfh.write("__getSiteConfig %r\n" % pTup)
            cf = ConfigInfoFile(mockTopPath=self.__mockTopPath, verbose=self.__verbose, log=self.__lfh)
            cD = cf.readConfigFileList(configPathSectionList=pathSectList)
            if deserialize:
                #
                cD = cf.deserializeConfig(cD, optionD=cD)
                # Deserialize any subsections -  avoid checking for private section name with wildcards.
                if True:  # pylint: disable=using-constant-test
                    #
                    for k, v in cD.items():
                        if isinstance(v, dict):
                            cD[k] = cf.deserializeConfig(cD[k], optionD=cD)
                else:
                    for sectionName in privateSectionNameList:
                        sU = sectionName.upper()
                        if sU in cD:
                            cD[sU] = cf.deserializeConfig(cD[sU], optionD=cD[sU])
        except Exception as e:
            self.__lfh.write("__getSiteConfig failing for location %r site %r - %r\n" % (siteLoc, siteId, str(e)))
            traceback.print_exc(file=self.__lfh)
        return cD

    def checkConfig(self, siteLoc, siteId, deserialize=True):
        """Perform sanity checks for the configuration options for the input location and site."""
        try:
            cD = self.__getSiteConfig(siteLoc, siteId, deserialize=deserialize)
            self.__lfh.write("read %d options for location %r site %r\n" % (len(cD), siteLoc, siteId))
            #
            #  - path check -
            deployPath = cD["SITE_DEPLOY_PATH"]
            for k in sorted(cD.keys()):
                v = cD[k]
                if v is None:
                    self.__lfh.write("location %s siteId %s option %s is None\n" % (siteLoc, siteId, k))
                elif not isinstance(v, str):
                    self.__lfh.write("location %s siteId %s option %s is %s\n" % (siteLoc, siteId, k, type(v)))
                elif len(v) < 1:
                    self.__lfh.write("location %s siteId %s option %s is blank\n" % (siteLoc, siteId, k))
                elif v.startswith(deployPath) and not os.access(v, os.R_OK):
                    self.__lfh.write("location %s siteId %s path access error %s\n" % (siteLoc, siteId, v))

        except Exception as e:
            self.__lfh.write("checkConfig for location %r site %r - %r\n" % (siteLoc, siteId, str(e)))
            traceback.print_exc(file=self.__lfh)

    def printConfig(self, siteLoc, siteId, deserialize=True):
        """Print the configuration options for the input location and site."""
        try:
            cD = self.__getSiteConfig(siteLoc, siteId, deserialize=deserialize)
            self.__lfh.write("read %d options for location %r site %r\n" % (len(cD), siteLoc, siteId))
            for k in sorted(cD.keys()):
                v = cD[k]
                if type(v) in [dict]:
                    self.__lfh.write(" +++ %-45s  %r\n" % (k, "private context"))
                    for k1 in sorted(v.keys()):
                        self.__lfh.write(" ---  --- +++ %-45s  %r\n" % (k1, v[k1]))
                else:
                    self.__lfh.write(" +++ %-45s  %r\n" % (k, v))
        except Exception as e:
            self.__lfh.write("printConfig failing for location %r site %r - %r\n" % (siteLoc, siteId, str(e)))
            traceback.print_exc(file=self.__lfh)

    def writeConfigCache(self, siteLoc, siteId, skipEmpty=True):
        """Write Python and JSON format cache files using the configuration options for input location and site."""
        self.__lfh.write("Starting writeConfigCache\n")
        try:
            cD = self.__getSiteConfig(siteLoc, siteId, deserialize=True)
            #
            if ((cD is None) or (len(cD) < 1)) and skipEmpty:
                self.__lfh.write("SKIPPING update of empty cache files for location %r site %r\n" % (siteLoc, siteId))
                return False
            cf = ConfigInfoFile(mockTopPath=self.__mockTopPath, verbose=self.__verbose, log=self.__lfh)
            cfCachePath = self.__getSitePythonCachePath(siteLoc, siteId)
            cf.writePythonConfigCache(cacheD={siteId.upper(): cD}, cacheFilePath=cfCachePath)
            #
            cfCachePath = self.__getSiteJsonCachePath(siteLoc, siteId)
            cf.writeJsonConfigCache(cacheD={siteId.upper(): cD}, cacheFilePath=cfCachePath)
            self.__lfh.write("updating cache files with %d options for location %r site %r\n" % (len(cD), siteLoc, siteId))
            return True
        except Exception as e:
            self.__lfh.write("writeConfigCache failing for location %r site %r - %r\n" % (siteLoc, siteId, str(e)))
            traceback.print_exc(file=self.__lfh)

        return False

    def writeLocationConfigCache(self, siteLoc, skipEmpty=True):
        """Write Python and JSON format cache files using the configuration options for input location and site."""
        self.__lfh.write("Starting writeLocationConfigCache\n")
        try:
            siteD = self.__getLocSiteD()
            siteIdList = []
            if siteLoc.upper() in siteD:
                siteIdList = siteD[siteLoc.upper()]
            #
            for siteId in siteIdList:
                cD = self.__getSiteConfig(siteLoc, siteId, deserialize=True)
                #
                if ((cD is None) or (len(cD) < 1)) and skipEmpty:
                    self.__lfh.write("SKIPPING update of empty cache files for location %r site %r\n" % (siteLoc, siteId))
                    continue
                cf = ConfigInfoFile(mockTopPath=self.__mockTopPath, verbose=self.__verbose, log=self.__lfh)
                cfPath = self.__getSiteConfigPath(siteLoc, siteId, "none")[0]
                if os.path.exists(cfPath):
                    cfCachePath = self.__getSitePythonCachePath(siteLoc, siteId)
                    cf.writePythonConfigCache(cacheD={siteId.upper(): cD}, cacheFilePath=cfCachePath)
                    #
                    cfCachePath = self.__getSiteJsonCachePath(siteLoc, siteId)
                    cf.writeJsonConfigCache(cacheD={siteId.upper(): cD}, cacheFilePath=cfCachePath)
                    self.__lfh.write("updating cache files with %d options for location %r site %r\n" % (len(cD), siteLoc, siteId))
                else:
                    self.__lfh.write("skipping cache files with for location %r site %r as site.cfg missing %s \n" % (siteLoc, siteId, cfPath))
            return True
        except Exception as e:
            self.__lfh.write("writeLocationConfigCache failing for location %r site %r - %r\n" % (siteLoc, siteId, str(e)))
            traceback.print_exc(file=self.__lfh)

        return False

    def __getLocSiteD(self):
        # Fetch custom location site details from the global common configuration file -
        comD = self.__getCommonConfig()
        siteD = {}
        if "SITE_LOCATION_SITE_DICT" in comD:
            siteD = comD["SITE_LOCATION_SITE_DICT"]
        else:
            # fallback resources --
            siteD = {
                "RCSB-WEST": ["WWPDB_DEPLOY_PRODUCTION_UCSD"],
                "PDBJ": ["WWPDB_DEPLOY_INTERNAL_PDBJ", "WWPDB_DEPLOY_PRODUCTION_PDBJ"],
                "RCSB-EAST": [
                    "WWPDB_DEPLOY_PRODUCTION_RU",
                    "WWPDB_DEPLOY_VALSRV_RU",
                    "WWPDB_DEPLOY_TEST_RU",
                    "WWPDB_DEPLOY_STAGING_RU",
                    "WWPDB_DEPLOY_ALPHA_RU",
                    "WWPDB_DEPLOY_BETA_RU",
                    "WWPDB_DEPLOY_NEXT_RU",
                    "WWPDB_DEPLOY_INTERNAL_RU",
                    "WWPDB_DEPLOY_DEVEL_RU",
                    "WWPDB_DEPLOY_MACOSX",
                    "WWPDB_DEPLOY_DEVEL_RU",
                    "WWPDB_DEPLOY_DEVEL2_RU",
                    "WWPDB_DEPLOY_DEVEL3_RU",
                    "WWPDB_DEPLOY_DEVEL4_RU",
                    "WWPDB_DEPLOY_DEPGRP1_RU",
                    "WWPDB_DEPLOY_DEPGRP2_RU",
                ],
                "PDBE": ["PDBE_PROD", "PDBE_DEV", "PDBE_LOCAL", "PDBE_HAPPY"],
            }
        return siteD


def main():  # pragma: no cover
    usage = """usage: %prog [options]

    Examples:

     Check a site configuration options file (requires both --locid & --siteid):

       python %prog --check --siteid=WWPDB_DEPLOY_TEST_RU --locid=rcsb-east

     Print the options in the specified site configuration file (requires both --locid & --siteid):

       python %prog --print --siteid=WWPDB_DEPLOY_TEST_RU --locid=rcsb-east

     Write/update the Python and JSON cache files for the specified site (requires --locid or both --locid & --siteid).

       python %prog --writecache --siteid=WWPDB_DEPLOY_TEST_RU --locid=rcsb-east

     Include additional locally scoped configuration sections using --sections="sec1,sec2,..." that
     will be stored in embedded dictionaries using section name keys (default=os_environment,httpd_services)

    """
    parser = OptionParser(usage)

    parser.add_option("--check", dest="checkConfig", action="store_true", default=False, help="Check configuration file for a site (--siteid) within a location (--locid)")
    parser.add_option("--print", dest="printConfig", action="store_true", default=False, help="Print the configuration options a site (--siteid) within a location (--locid)")
    parser.add_option(
        "--writecache", dest="writeCache", action="store_true", default=False, help="Write configuration cache file for a site (--siteid) within a location (--locid)"
    )

    parser.add_option("--siteid", dest="siteId", default=None, help="wwPDB site ID (e.g. WWPDB_DEPLOY_TEST_RU)")
    parser.add_option("--locid", dest="locId", default=None, help="wwPDB location ID (e.g. pdbe, pdbj, rcsb-east, ... )")

    parser.add_option(
        "--sections", dest="privateSectionNames", default=None, help="Comma separated list of private section names (stored as dictionaries under their section name)"
    )
    parser.add_option(
        "--add_common_sections", dest="commonSectionNames", default=None, help="Comma separated list of additional option section names added to the common namespace"
    )
    parser.add_option("-v", "--verbose", default=True, action="store_true", dest="verbose")

    # Test setup configuration
    # mockdir path
    parser.add_option("--mockdir", default=None, help=SUPPRESS_HELP)
    # source dir - specifies a read only source tree to use for finding configuration files
    parser.add_option("--sourcedir", default=None, help=SUPPRESS_HELP)

    (options, args) = parser.parse_args()  # pylint: disable=unused-variable

    cI = ConfigInfoFileExec(mockTopPath=options.mockdir, sourceDirPath=options.sourcedir, verbose=options.verbose, log=sys.stderr)
    #
    if options.privateSectionNames is not None:
        privateSectionNameList = [str(x).strip() for x in options.privateSectionNames.split(",")]
    else:
        privateSectionNameList = [
            "os_environment",
            "httpd_services",
            "install_environment",
            "database_services",
            "validation_services",
            "host_site_defaults",
            "test_setup_*",
            "backup_server_*",
        ]
    cI.setPrivateSectionNames(sectionNameList=privateSectionNameList)

    if options.commonSectionNames is not None:
        commonSectionNameList = [str(x).strip() for x in options.commonSectionNames.split(",")]
    else:
        commonSectionNameList = ["database_services", "validation_services"]
    cI.addCommonSectionNames(sectionNameList=commonSectionNameList)

    if options.checkConfig and options.siteId is not None and options.locId is not None and cI.testConfigPath(accessType="read"):
        cI.checkConfig(siteLoc=options.locId, siteId=options.siteId)

    if options.printConfig and options.siteId is not None and options.locId is not None and cI.testConfigPath(accessType="read"):
        cI.printConfig(siteLoc=options.locId, siteId=options.siteId)

    if options.writeCache and options.siteId is not None and options.locId is not None and cI.testConfigPath(accessType="write"):
        cI.writeConfigCache(siteLoc=options.locId, siteId=options.siteId)
    elif options.writeCache and options.siteId is None and options.locId is not None and cI.testConfigPath(accessType="write"):
        cI.writeLocationConfigCache(siteLoc=options.locId)


if __name__ == "__main__":
    main()
