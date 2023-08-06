##
# File:    ConfigInfoFile.py
# Date:    16-Mar-2016
#
# Updates:
#      2-Apr-2016  jdw add serializer/deserializer filters -
#      4-Apr-2016  jdw add methods for json serialized cache files
#      4-Apr-2016  jdw split off fallback methods in separate class ConfigInfoFallBack()
#     10-May-2016  jdw revised the template substitution to support additional configuration sections
#     24-May-2016  jdw simplified the import of off-site json files -
#      4-Dec-2016  jdw process additional list of section names for each configuration file.
#     11-Oct-2017  jdw add support for private section names including wildcard chars.
#     10-Oct-2017  jdw Preliminary support for Py2->Py3
# -
"""
Provides access to site-specific configuration information stored in flat files and cache files.

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"


import os
import sys
import datetime
import shutil

import ast
import json
from fnmatch import fnmatchcase
import logging

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser

logger = logging.getLogger(__name__)


class ConfigInfoFile(object):
    """
    Provides access to site-specific configuration information stored in flat files and cache files.
    """

    def __init__(self, verbose=False, log=sys.stderr, mockTopPath=None):  # pylint: disable=unused-argument
        self.__debug = True
        if mockTopPath:
            self.__mockdefaults = {"test_mockpath_env": mockTopPath}
        else:
            self.__mockdefaults = {}
        #

    def readSiteConfig(self, siteId, configFilePath):
        """Read the input configuration file and return a configuration dictionary for
        the input site.  This corresponds to the items and values within the configuration
        section identified by the input site identifier.   All configuration sections and
        option keys are converted to upper case in the returned dictionary.

        """
        d = self.readConfig(configFilePath)
        if siteId in d:
            return d[siteId]
        else:
            return {}

    def readConfig(self, configFilePath):
        """Read the input configuration file and return a dictionary of configuration items
        where all configuration keys are converted to upper case.  The returned dictionary is
        organized in configuration sections (e.g. retD[sectionN.upper()]={k1:v1,k2:v2,...})

        """
        retD = {}
        try:
            if sys.version_info[0] > 2:
                # Python 3.2 deprecated
                config = ConfigParser.ConfigParser(defaults=self.__mockdefaults)
            else:
                config = ConfigParser.SafeConfigParser(defaults=self.__mockdefaults)
            config.read(configFilePath)
            sectionL = config.sections()
            for section in sectionL:
                kvTupL = config.items(section)
                sKyU = section.upper()
                d = {}
                for (k, v) in kvTupL:
                    d[k.upper()] = v
                retD[sKyU] = d
        except Exception as e:
            logger.error("failed reading %s", configFilePath)
            if self.__debug:
                logger.exception("failed reading %s - %s", configFilePath, str(e))

        return retD

    def readConfigFileList(self, configPathSectionList=None):
        """Read the input list of configuration file paths/section names   [(configPath,sectionName,context), (configPath,sectionName,context),].
        Preceding files in this list may supply substition values for subsequent files through string interpolation
        such as %(replace_me)s.  The first instance of any option/value encountered in the path list is treated as authoritative.

        The ConfigParser class processes all configuration option values as strings.  Section names are searched in lower case.

        Target section names may contain wildcard characters supported by fnmatch()

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
                    config = ConfigParser.RawConfigParser(defaults=self.__mockdefaults, allow_no_value=True)
                    config.read(configFilePath)
                    sectionL = config.sections()
                    for tsn in sectionL:
                        if tsn == sectionName or fnmatchcase(tsn, sectionName):
                            kvTupL = config.items(tsn.lower())
                            # for k, v in kvTupL:
                            #    defaultD[k] = v
                            if self.__debug:
                                logger.info("fetching section %s length %d", tsn, len(kvTupL))
                            if context in ["common"]:
                                for (k, v) in kvTupL:
                                    # Respect existing values in the order of config files -
                                    if k not in saveD:
                                        try:
                                            saveD[k] = v % defaultD
                                        except BaseException as e:
                                            logger.error("substitution failed for %r %r %r", k, v, str(e))
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
                                            logger.error("substitution failed for %r %r %r", k, v, str(e))
                                            continue
                                        # update substitution defaults ...
                                        defaultD[k] = pD[k]
                                        pDU[k.upper()] = pD[k]
                                saveD[tsn.upper()] = pDU
                            for k, v in saveD.items():
                                defaultD[k] = v

            # Copy the accumulated saved items for return with upper-cased keys --
            for k, v in saveD.items():
                retD[k.upper()] = v
        except Exception as e:  # noqa: E722
            logger.error("failed reading configuration file list %r", configPathSectionList)
            if self.__debug:
                logger.exception("failed reading file - error %s", str(e))

        return retD

    def writeConfig(self, configFilePath, sectionL, sectionD, requireBackup=True, sortKeys=True):
        """Write configuration file for the key-value options in the input section dictionary.

        Section names and option keys are converted to lower case.   Option values are
        not modified.

        sectionL [sectionName,sectionName,...]  oder of
        sectionD [sectionName] stores a dictionary of options, opD  where opD[k] = v
        """
        try:
            config = ConfigParser.RawConfigParser(defaults=self.__mockdefaults)
            for sectionKey in sectionL:
                opD = sectionD[sectionKey]
                sectionName = str(sectionKey).lower()
                config.add_section(sectionName)
                #
                if sortKeys:
                    for ky in sorted(opD.keys()):
                        v = opD[ky]
                        kyDsp = str(ky).lower()
                        config.set(sectionName, kyDsp, v)
                else:
                    for ky, v in opD.items():
                        kyDsp = str(ky).lower()
                        config.set(sectionName, kyDsp, v)
                #
                #
            ok = self.__copyWithTimeStamp(configFilePath)
            if not ok and requireBackup:
                logger.error("failed writing backup config file for %s", configFilePath)
                return False
            with open(configFilePath, "w") as configfile:
                config.write(configfile)
            return True
        except Exception as e:
            logger.info("failing")
            if self.__debug:
                logger.exception("failing %s", str(e))
        return False

    def deserializeConfig(self, configD, optionD=None):
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
                    logger.error("failed csv filter %r %r - %s", k, v, str(e))
                #
                try:
                    if k in objD:
                        retD[k] = ast.literal_eval(v)
                except Exception as e:
                    logger.error("failed eval filter %r %r - %s", k, v, str(e))
        except Exception as e:
            logger.info("failed configuration filter")
            if self.__debug:
                logger.exception("failed configuration filter %s", str(e))

        return retD

    def serializeConfig(self, configD, optionD=None):
        """Apply an adhoc set of filters on the input configuration dictionary.
        Input option values are assumed to be python objects to be converted to strings for output
        by the configuration file writer

        The following inline options are used as filter selectors:

        config_as_object - "option, option, option"
                           convert object to string. For instance,  tuple, list or dict are
                           stringified (e.g __repr__) represenation. This also handles None -> "None"

        config_csv_as_list - "option, option, option"
                             convert list to comma separated values

        config_csv_as_int_list - "option, option, option"
                               convert list of integers to comma separated values

        config_as_int|float  - "option, option, option"
                              convert int|float to string  (default behavior)

        all values are tested for the literal None value and converted to string 'None'

        Returns an updated dictionary of configuration options with values cast according filter conditions.

        """
        retD = {}
        objD = {}
        lstD = {}
        iLstD = {}
        try:
            if optionD is not None:
                optD = dict((k.lower(), v) for k, v in optionD.items())
                if "config_as_object" in optD:
                    objD = dict.fromkeys([t.strip().upper() for t in optD["config_as_object"].split(",")])
                if "config_csv_as_list" in optD:
                    lstD = dict.fromkeys([t.strip().upper() for t in optD["config_csv_as_list"].split(",")])
                if "config_csv_as_int_list" in optD:
                    iLstD = dict.fromkeys([t.strip().upper() for t in optD["config_csv_as_int_list"].split(",")])
            #
            for (k, v) in configD.items():
                retD[k] = v
                if v is None:
                    retD[k] = "None"
                try:
                    if k in lstD or k in iLstD:
                        if isinstance(v, list):
                            retD[k] = ",".join(str(x) for x in v)
                except Exception as e:
                    logger.error("failed list join %r %r - %s", k, v, str(e))
                #
                try:
                    if k in objD:
                        retD[k] = "%r" % v
                except Exception as e:
                    logger.error("failed __repr__ %r %r - %s", k, v, str(e))
        except Exception as e:
            logger.info("failed configuration filter\n")
            if self.__debug:
                logger.exception("failed configuration filter %s", str(e))

        return retD

    def __copyWithTimeStamp(self, filePath):
        try:
            bckupPath = filePath + datetime.datetime.now().strftime("-%Y-%m-%d-%H-%M-%S")
            shutil.copyfile(filePath, bckupPath)
            return True
        except Exception as e:
            logger.info("Could not write backup file %s - %s", bckupPath, str(e))

        return False

    def writePythonConfigCache(self, cacheD, cacheFilePath, withBackup=True):
        """Write a Python cache file containing configuration option data in the input cache dictionary.
        This cache file wraps the configuration dictionary with a class in a module that can be imported.

        """
        template = """
import os
import sys
import json
import traceback


class ConfigInfoFileCache(object):
    _configD=%r

    @classmethod
    def getConfigDictionary(cls, siteId):
        try:
            return cls._configD[siteId]
        except:
            return cls.getJsonConfigDictionary(siteId)

    @classmethod
    def getJsonConfigDictionary(cls, siteId):
        try:
            p = os.getenv("TOP_WWPDB_SITE_CONFIG_DIR")
            for l in ["rcsb-east", "rcsb-west", "pdbj", "pdbe", "pdbc"]:
                jsonPath = os.path.join(p,l,siteId.lower(),"ConfigInfoFileCache.json")
                if os.access(jsonPath, os.R_OK):
                    with open(jsonPath, "r") as infile:
                        cD = json.load(infile)
                    return cD[siteId]
        except:
            pass
            # traceback.print_exc(file=sys.stderr)

        return {}

    @classmethod
    def getJsonConfigDictionaryPrev(cls, siteId):
        try:
            id = os.getenv("WWPDB_SITE_ID")
            if siteId != id:
                p = os.getenv("TOP_WWPDB_SITE_CONFIG_DIR")
                l = str(os.getenv("WWPDB_SITE_LOC")).lower()
                jsonPath = os.path.join(p,l,siteId.lower(),"ConfigInfoFileCache.json")
                with open(jsonPath, "r") as infile:
                    cD = json.load(infile)
                return cD[siteId]
        except:
            pass
            # traceback.print_exc(file=sys.stderr)

        return {}

        """
        try:
            if os.access(cacheFilePath, os.R_OK):
                if withBackup:
                    ok = self.__copyWithTimeStamp(cacheFilePath)
                    if not ok:
                        logger.error("failed writing backup cache file for %s", cacheFilePath)
                        return False
            with open(cacheFilePath, "wb") as cacheFile:
                if sys.version_info[0] > 2:
                    cacheFile.write((template % cacheD).encode())
                else:
                    cacheFile.write(template % cacheD)
            return True
        except Exception as e:  # noqa: E722
            logger.info("failed writing %s - %s", cacheFilePath, str(e))
            if self.__debug:
                logger.exception("failed writing %s", cacheFilePath)
        return False

    def writeJsonConfigCache(self, cacheD, cacheFilePath, withBackup=True):
        """Write a JSON cache file containing configuration option data in the input cache dictionary."""
        try:
            if os.access(cacheFilePath, os.R_OK):
                if withBackup:
                    ok = self.__copyWithTimeStamp(cacheFilePath)
                    if not ok:
                        logger.error("failed writing backup cache file for %s", cacheFilePath)
                        return False
            with open(cacheFilePath, "w") as outfile:
                json.dump(cacheD, outfile, indent=4)
            return True
        except Exception as e:
            logger.info("failed writing %s - %s", cacheFilePath, str(e))
            if self.__debug:
                logger.exception("failed writing %s - %s", cacheFilePath, str(e))
        return False

    def readJsonConfigCache(self, cacheFilePath):
        """Read a JSON cache file and return a dictionary containing configuration option data."""
        try:
            with open(cacheFilePath, "r") as infile:
                return json.load(infile)
        except Exception as e:
            logger.info("failed reading %s - %s", cacheFilePath, str(e))
            if self.__debug:
                logger.exception("failed reading file %s", cacheFilePath)
        return {}
