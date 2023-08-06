#!/usr/bin/env python
##
# File:    ConfigInfoShellExec.py
# Author:  jdw
# Date:    8-May-2016
# Version: 0.001
#
# Updates:
#      14-May-2016 jdw add support for installation environment
#      16-May-2016 jdw add bootstrap support for reading flat config files directly --
#       4-Dec-2016 jdw add support for extra common configuration sections
#       5-Dec-2016 jdw add export for validation and database services -
##
"""
Execuction wrapper for shell configuration using project configuration files.

"""

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.001"

import sys
import os
import traceback

if sys.version_info[0] > 2:
    import importlib
else:
    import imp  # pylint: disable=deprecated-module
import ast

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser
from optparse import OptionParser  # pylint: disable=deprecated-module


class ConfigInfoShellExec(object):
    """
    Execuction wrapper for shell configuration using project configuration files.

    Shell configuration:

    + by host as argument (fqdn)

        expects  <TOP_WWPDB_SITE_CONFIG_DIR>/common/common.cfg  containing mapping data

    + by site using explicit arguments for siteLoc and siteId -

    both require: TOP_WWPDB_SITE_CONFIG_DIR in the environment or as argument


    """

    def __init__(self, topConfigPath=None, hostName=None, siteLoc=None, siteId=None, cacheFlag=True, verbose=True, log=sys.stdout):  # pylint: disable=unused-argument
        self.__lfh = log
        self.__debug = False
        self.__siteId = None
        self.__siteLoc = None
        self.__topConfigPath = None
        self.__cD = {}
        #
        # Complete list of sections maintained as private namespaces
        self.__privateSectionNameList = ["os_environment", "httpd_services", "install_environment", "database_services", "validation_services"]
        #
        # additional configuration sections added to the common namespace
        self.__extraCommonSectionNameList = ["database_services", "validation_services"]

        #
        if topConfigPath is None:
            topConfigPath = os.getenv("TOP_WWPDB_SITE_CONFIG_DIR", default=None)
        ok = self.__testConfigPath(topConfigPath)
        if ok:
            self.__topConfigPath = topConfigPath
            self.__siteLoc, self.__siteId = self.__setup(topConfigPath, hostName, siteLoc, siteId)

            if cacheFlag:
                self.__cD = self.__getConfigD(self.__topConfigPath, self.__siteLoc, self.__siteId)
            else:
                self.__cD = self.__getSiteConfigRaw(self.__topConfigPath, self.__siteLoc, self.__siteId)

    def __setup(self, topConfigPath, inpHostName, inpSiteLoc, inpSiteId):
        """ """
        siteLoc = None
        siteId = None
        #
        if topConfigPath is None:
            self.__lfh.write("FAILING - missing configuration file path\n")
        elif inpSiteLoc is not None and inpSiteId is not None:
            #
            # load site configuration data cache -
            siteLoc = inpSiteLoc
            siteId = inpSiteId
        elif inpHostName is not None:
            # read host mapping data
            fp = self.__getCommonConfigPath(topConfigPath)
            cD = self.__readConfigTextFile(fp)
            if "HOST_SITE_DEFAULTS" in cD:
                hnU = str(inpHostName).upper()
                if hnU in cD["HOST_SITE_DEFAULTS"]:
                    tL = cD["HOST_SITE_DEFAULTS"][hnU].split(",")
                    siteLoc = tL[0]
                    siteId = tL[1]
        else:
            self.__lfh.write("FAILING configuration could not be resolved\n")
        #
        if self.__debug:
            self.__lfh.write("_setup returns siteLoc %r siteId %r\n" % (siteLoc, siteId))
        return siteLoc, siteId

    def __getPrivateSectionNames(self):
        return self.__privateSectionNameList

    def __getExtraCommonSectionNames(self):
        return self.__extraCommonSectionNameList

    def __getConfigD(self, topConfigPath, siteLoc, siteId):
        """Load the current python cache configuration data for the input location/site
        and return a dictionary of this data.
        """
        #
        tD = {}
        try:
            fp = self.__getSitePythonCachePath(topConfigPath, siteLoc, siteId)
            if sys.version_info[0] > 2:
                # Assumes > python 3.4 - import.machinery.SourceFileLoader
                # would be needed
                spec = importlib.util.spec_from_file_location("ConfigInfoFileCache", fp)
                oD = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(oD)
                cD = oD.ConfigInfoFileCache._configD  # pylint: disable=protected-access
            else:
                oD = imp.load_source("ConfigInfoFileCache", fp)
                cD = oD.ConfigInfoFileCache._configD  # pylint: disable=protected-access
            tD = cD[siteId]
        except Exception as e:
            self.__lfh.write("failing %s\n" % str(e))
            if self.__debug:
                traceback.print_exc(file=self.__lfh)
        return tD

    def __testConfigPath(self, topConfigPath, accessType="read"):
        #
        ok = True
        try:
            if topConfigPath is None:
                ok = False
                self.__lfh.write("WARNING - TOP_WWPDB_SITE_CONFIG_DIR is not set in the environment.\n")
            elif accessType == "write" and not os.access(topConfigPath, os.W_OK):
                ok = False
                self.__lfh.write("WARNING - %s lacks write access\n" % topConfigPath)
            elif accessType == "read" and not os.access(topConfigPath, os.R_OK):
                ok = False
                self.__lfh.write("WARNING - %s lacks read access\n" % topConfigPath)
        except Exception as e:
            self.__lfh.write("__testConfigPath failing %r\n" % str(e))
            traceback.print_exc(file=self.__lfh)
            ok = False

        return ok

    def __getCommonConfigPath(self, topConfigPath, sectionName="common", context="common"):
        cfPath = os.path.join(topConfigPath, "common", "common.cfg")
        return cfPath, sectionName, context

    def __getSiteCommonConfigPath(self, topConfigPath, siteLoc, sectionName="site_common", context="common"):
        cfPath = os.path.join(topConfigPath, siteLoc.lower(), "site_common", "common.cfg")
        return cfPath, sectionName, context

    def __getSiteConfigPath(self, topConfigPath, siteLoc, siteId, sectionName, context="common"):
        cfPath = os.path.join(topConfigPath, siteLoc.lower(), siteId.lower(), "site.cfg")
        return cfPath, sectionName, context

    def __getSitePythonCachePath(self, topConfigPath, siteLoc, siteId):
        cfPath = os.path.join(topConfigPath, siteLoc.lower(), siteId.lower(), "ConfigInfoFileCache.py")
        return cfPath

    # def __getSiteJsonCachePath(self, topConfigPath, siteLoc, siteId):
    #     cfPath = os.path.join(topConfigPath, siteLoc.lower(), siteId.lower(), "ConfigInfoFileCache.json")
    #     return cfPath

    def __readConfigTextFile(self, configFilePath):
        """Read the input configuration file and return a dictionary of configuration items
        where all configuration keys are converted to upper case.  The returned dictionary is
        organized in configuration sections (e.g. retD[sectionN.upper()]={k1:v1,k2:v2,...})

        """
        retD = {}
        try:
            if sys.version_info[0] > 2:
                # Python 3.2 deprecates SafeConfigParser()
                config = ConfigParser.ConfigParser()
            else:
                config = ConfigParser.SafeConfigParser()
            # print configFilePath
            config.read(configFilePath)
            sectionL = config.sections()
            # print sectionL
            for section in sectionL:
                kvTupL = config.items(section)
                sKyU = section.upper()
                d = {}
                for (k, v) in kvTupL:
                    d[k.upper()] = v
                retD[sKyU] = d
        except Exception as e:
            self.__lfh.write("FAILED reading %s - %s\n" % (configFilePath, str(e)))
            if self.__debug:
                traceback.print_exc(file=self.__lfh)

        return retD

    def __getConfigPathSectionList(self, topConfigPath, siteLoc, siteId, extraCommonSectionNameList, privateSectionNameList):
        """Returns the search path of sections and configuration file paths for the input location and site.
        The site specific configuration file path is always included.   The site-common or project common
        configuration files are included only if these exist.

        Any section names in extraCommonSectionNameList are added to path list for each configuration file -

        Returns: [(configPath,sectionName,context), (configPath,sectionName),context), ...]
        """
        cfPathSectionList = []
        if self.__topConfigPath is not None and siteId is not None and siteLoc is not None:
            (p, s, c) = self.__getSiteConfigPath(topConfigPath=topConfigPath, siteLoc=siteLoc, siteId=siteId, sectionName=siteId.lower())
            if p is not None and os.access(p, os.R_OK):
                cfPathSectionList.append((p, s, c))
                for cSec in extraCommonSectionNameList:
                    cfPathSectionList.append((p, cSec, "common"))
            (p, s, c) = self.__getSiteCommonConfigPath(topConfigPath=topConfigPath, siteLoc=siteLoc, sectionName="site_common")
            if p is not None and os.access(p, os.R_OK):
                cfPathSectionList.append((p, s, c))
                for cSec in extraCommonSectionNameList:
                    cfPathSectionList.append((p, cSec, "common"))
            (p, s, c) = self.__getCommonConfigPath(topConfigPath=topConfigPath, sectionName="common")
            if p is not None and os.access(p, os.R_OK):
                cfPathSectionList.append((p, s, c))
                for cSec in extraCommonSectionNameList:
                    cfPathSectionList.append((p, cSec, "common"))
            #
            # Additional context specific (private) configuration sections - stored in the site specific path
            #
            for sectionName in privateSectionNameList:
                (p, s, c) = self.__getSiteConfigPath(topConfigPath=topConfigPath, siteLoc=siteLoc, siteId=siteId, sectionName=sectionName, context="private")
                if p is not None and os.access(p, os.R_OK):
                    cfPathSectionList.append((p, s, c))

        return cfPathSectionList

    def __getSiteConfigRaw(self, topConfigPath, siteLoc, siteId, deserialize=True):
        """Return the complete site of configuration options for the input location and site."""
        cD = {}
        try:
            privateSectionNameList = self.__getPrivateSectionNames()
            extraCommonSectionNameList = self.__getExtraCommonSectionNames()
            pathSectList = self.__getConfigPathSectionList(topConfigPath, siteLoc, siteId, extraCommonSectionNameList, privateSectionNameList)
            if self.__debug:
                self.__lfh.write("__getSiteConfigRaw location %r site %r path list %r \n" % (siteLoc, siteId, pathSectList))
            cD = self.__readConfigFileList(configPathSectionList=pathSectList)
            if deserialize:
                #
                cD = self.__deserializeConfig(cD, optionD=cD)
                for sectionName in privateSectionNameList:
                    sU = sectionName.upper()
                    if sU in cD:
                        cD[sU] = self.__deserializeConfig(cD[sU], optionD=cD[sU])
        except Exception as e:
            self.__lfh.write("__getSiteConfigRaw failing for location %r site %r - %s\n" % (siteLoc, siteId, str(e)))
            traceback.print_exc(file=self.__lfh)
        return cD

    def __readConfigFileList(self, configPathSectionList=None):
        """Read the input list of configuration file paths/section names   [(configPath,sectionName,context), (configPath,sectionName,context),].
        Preceding files in this list may supply substition values for subsequent files through string interpolation
        such as %(replace_me)s.  The first instance of any option/value encountered in the path list is treated as authoritative.

        The ConfigParser class processes all configuration option values as strings.  Section names are searched in lower case.

        Returns configuration options from all sections in a dictionary with option keys in upper case.

        """
        retD = {}
        try:
            defaultD = {}
            saveD = {}
            # For each configuration file in turn -- accumulated content provides default value substition values for subsequent files -
            #
            # Template substitution performed explicitly here using any preceding content in the 'common' namespace --
            if configPathSectionList is not None:
                for configFilePath, sectionName, context in configPathSectionList:
                    config = ConfigParser.RawConfigParser(allow_no_value=True)
                    config.read(configFilePath)
                    sectionL = config.sections()
                    if sectionName in sectionL:
                        kvTupL = config.items(sectionName.lower())
                        # for k, v in kvTupL:
                        #    defaultD[k] = v
                        if self.__debug:
                            self.__lfh.write("__readConfigFileList fetching section %s length %d\n" % (sectionName, len(kvTupL)))
                        if context in ["common"]:
                            for (k, v) in kvTupL:
                                # Respect existing values in the order of config files -
                                if k not in saveD:
                                    try:
                                        saveD[k] = v % defaultD
                                    except BaseException as e:
                                        self.__lfh.write("substitution failed for %r %r %r\n" % (k, v, str(e)))
                                        continue
                                    # update substitution defaults ...
                                    defaultD[k] = saveD[k]
                        elif context in ["private"]:
                            pD = {}
                            pDU = {}
                            for (k, v) in kvTupL:
                                if k not in pD:
                                    try:
                                        pD[k] = v % defaultD
                                    except BaseException as e:
                                        self.__lfh.write("substitution failed for %r %r %r\n" % (k, v, str(e)))
                                        continue
                                    # update substitution defaults ...
                                    defaultD[k] = pD[k]
                                    pDU[k.upper()] = pD[k]
                            saveD[sectionName.upper()] = pDU
                        for k, v in saveD.items():
                            defaultD[k] = v

            # Copy the accumulated saved items for return with upper-cased keys --
            for k, v in saveD.items():
                retD[k.upper()] = v
        except Exception as e:
            self.__lfh.write("failed reading configuration file list %r %r\n" % (configPathSectionList, str(e)))
            if self.__debug:
                traceback.print_exc(file=self.__lfh)

        return retD

    def __deserializeConfig(self, configD, optionD=None):
        """Apply an adhoc set of filters on the input configuration dictionary.
        Input option values are assumed to be the string values returned by the configuration file parser.

        The following inline options are used as filter selectors:

        config_as_object - "option, option, option"
                           convert string to object. For instance, create tuple, list or dict from
                           string (e.g __repr__) represenation. This also handles "None" -> None

        config_csv_as_list - "option, option, option"
                              convert comma separated values to a list of strings

        config_csv_as_int_list - "option, option, option"
                               convert comma separated values to a list of integers

        config_as_int|float  - "option, option, option"
                              convert string to int|float

        all values are tested for the literal 'None' string which is converted to a None value.

        All input option keys (optionD) are processed with leading and trailing whitespace stripped and
        in upper case.

        Returns an updated dictionary of configuration options with values cast according filter conditions.

        """
        retD = {}
        objD = {}
        lstD = {}
        intD = {}
        fltD = {}
        iLstD = {}
        try:
            if optionD is not None:
                optD = dict((k.lower(), v) for k, v in optionD.items())
                if "config_as_object" in optD:
                    objD = dict.fromkeys([t.strip().upper() for t in optD["config_as_object"].split(",") if len(t.strip()) > 0])
                if "config_csv_as_list" in optD:
                    lstD = dict.fromkeys([t.strip().upper() for t in optD["config_csv_as_list"].split(",") if len(t.strip()) > 0])
                if "config_as_int" in optD:
                    intD = dict.fromkeys([t.strip().upper() for t in optD["config_as_int"].split(",") if len(t.strip()) > 0])
                if "config_as_float" in optD:
                    fltD = dict.fromkeys([t.strip().upper() for t in optD["config_as_float"].split(",") if len(t.strip()) > 0])
                if "config_csv_as_int_list" in optD:
                    iLstD = dict.fromkeys([t.strip().upper() for t in optD["config_csv_as_int_list"].split(",") if len(t.strip()) > 0])
            #
            # if self.__debug:
            #   print "Filter as object", objD
            #
            for (k, v) in configD.items():
                retD[k] = v
                if v == "None":
                    retD[k] = None

                if k in intD:
                    retD[k] = int(v)

                if k in fltD:
                    retD[k] = float(v)

                try:
                    if k in lstD:
                        retD[k] = [t.strip() for t in v.split(",")]
                    if k in iLstD:
                        retD[k] = [int(t.strip()) for t in v.split(",")]
                except Exception as e:
                    self.__lfh.write("failed csv list filter %r %r %r\n" % (k, v, str(e)))
                #
                try:
                    if k in objD:
                        retD[k] = ast.literal_eval(v)
                except Exception as e:
                    self.__lfh.write("failed eval filter %r %r %r\n" % (k, v, str(e)))
        except Exception as e:
            self.__lfh.write("failed configuration filter %r\n" % str(e))
            if self.__debug:
                traceback.print_exc(file=self.__lfh)

        return retD

    def printConfig(self):
        return self.__printConfig(self.__siteLoc, self.__siteId, self.__cD)

    def __printConfig(self, siteLoc, siteId, cD):
        """Print the configuration options for the input location and site."""
        try:
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
            self.__lfh.write("failing for location %r site %r %r\n" % (siteLoc, siteId, str(e)))
            if self.__debug:
                traceback.print_exc(file=self.__lfh)

    def shellConfig(self, shellType="bash"):
        return self.__exportConfig(self.__siteLoc, self.__siteId, self.__cD, expKey="OS_ENVIRONMENT", shellType=shellType)

    def httpdConfig(self, shellType="bash"):
        return self.__exportConfig(self.__siteLoc, self.__siteId, self.__cD, expKey="HTTPD_SERVICES", shellType=shellType)

    def installConfig(self, shellType="bash"):
        return self.__exportConfig(self.__siteLoc, self.__siteId, self.__cD, expKey="INSTALL_ENVIRONMENT", shellType=shellType)

    def validationConfig(self, shellType="bash"):
        return self.__exportConfig(self.__siteLoc, self.__siteId, self.__cD, expKey="VALIDATION_SERVICES", shellType=shellType)

    def databaseConfig(self, shellType="bash"):
        return self.__exportConfig(self.__siteLoc, self.__siteId, self.__cD, expKey="DATABASE_SERVICES", shellType=shellType)

    def __exportConfig(self, siteLoc, siteId, cD, expKey="OS_ENVIRONMENT", shellType="bash"):
        """Print the configuration options for the input location and site."""
        try:
            if expKey in cD:
                dd = cD[expKey]
                for k in sorted(dd.keys()):
                    v = dd[k]
                    if shellType in ["bash", "sh"]:
                        self.__lfh.write('export %s="%s"\n' % (k, v))
                    elif shellType in ["csh", "tcsh"]:
                        self.__lfh.write('setenv %s "%s"\n' % (k, v))
        except Exception as e:
            if self.__debug:
                self.__lfh.write("__exportConfig failing for location %r site %r - %r\n" % (siteLoc, siteId, str(e)))
                traceback.print_exc(file=self.__lfh)


def main():  # pragma: no cover
    usage = """
    %prog [options]

    Examples:

     Export shell configuration options  (requires both --locid & --siteid):

       python %prog --shell --configpath=/wwpdb_da/site-config --siteid=WWPDB_DEPLOY_TEST_RU --locid=rcsb-east

     Export shell configuration options for the default host site assignment:

       python %prog --shell --configpath=/wwpdb_da/site-config --hostname=myhost.wwpdb.org --shellType='bash'

     Print the all configuration options  (requires both --locid & --siteid or --hostname):

       python %prog --print --configpath=/wwpdb_da/site-config --siteid=WWPDB_DEPLOY_TEST_RU --locid=rcsb-east

    """
    parser = OptionParser(usage)
    parser.add_option("--print", dest="printConfig", action="store_true", default=False, help="Print the configuration options for site (--siteid) at location (--locid)")
    parser.add_option("--hostname", dest="hostName", default=None, help="Fully qualified host name")
    parser.add_option("--siteid", dest="siteId", default=None, help="wwPDB site ID (e.g. WWPDB_DEPLOY_TEST_RU)")
    parser.add_option("--locid", dest="siteLoc", default=None, help="wwPDB location ID (e.g. pdbe, pdbj, rcsb-east, ... )")
    parser.add_option("--configpath", dest="topConfigPath", default=None, help="Configuration path (e.g. /wwpdb_da/site-config)")

    parser.add_option("--shell", dest="shellConfig", action="store_true", default=False, help="Export shell environment for (--siteid) at location (--locid) or host")
    parser.add_option("--shelltype", dest="shellType", default="bash", help="Export shell type ('bash', 'csh')")
    parser.add_option("--httpd", dest="httpdConfig", action="store_true", default=False, help="Export httpd environment for (--siteid) at location (--locid) or host")
    parser.add_option("--install", dest="installConfig", action="store_true", default=False, help="Export installation environment for (--siteid) at location (--locid) or host")
    parser.add_option(
        "--validation", dest="validationConfig", action="store_true", default=False, help="Export validation service environment for (--siteid) at location (--locid) or host"
    )
    parser.add_option(
        "--database", dest="databaseConfig", action="store_true", default=False, help="Export database services environment for (--siteid) at location (--locid) or host"
    )
    parser.add_option("-v", "--verbose", default=True, action="store_true", dest="verbose")
    parser.add_option("--nocache", default=False, action="store_true", dest="nocacheFlag")

    (options, args) = parser.parse_args()  # pylint: disable=unused-variable

    if options.topConfigPath is None:
        print("Configuration path must be specified (--configpath)")
        parser.print_help()
        exit(-1)

    if options.hostName is None and (options.siteLoc is None or options.siteId is None):
        print("Either hostname or the combination of siteLoc and siteId must be specified")
        parser.print_help()
        exit(-1)

        parser.error(usage)

    cI = ConfigInfoShellExec(
        topConfigPath=options.topConfigPath,
        hostName=options.hostName,
        siteLoc=options.siteLoc,
        siteId=options.siteId,
        cacheFlag=not options.nocacheFlag,
        verbose=options.verbose,
        log=sys.stdout,
    )

    if options.printConfig:
        cI.printConfig()

    if options.shellConfig:
        cI.shellConfig(shellType=options.shellType)

    if options.httpdConfig:
        cI.httpdConfig(shellType=options.shellType)

    if options.installConfig:
        cI.installConfig(shellType=options.shellType)

    if options.validationConfig:
        cI.validationConfig(shellType=options.shellType)

    if options.databaseConfig:
        cI.databaseConfig(shellType=options.shellType)


if __name__ == "__main__":
    main()
