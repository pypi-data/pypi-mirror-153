##
# File:    ConfigInfoDataSet.py
# Date:    17-Mar-2016
#
# Updates:
#  06-Apr-2016  jdw  get default id ranges from ConfigInfoData -
#  07-Apr-2016  jdw  add resource data file to hold location exceptions.
#  15-Aug-2016  jdw  add support backup sites serving as surrogates for production sites.
#  19-Aug-2016  jdw  add getDefaultSiteId()
#  23-Aug-2016  jdw  add getDataSetLocations() and writeLocationList() and getDataSetLocationDict() and removeDataSets()
#  01-Jan-2018  ep   add getTestIdRange()
##
"""
Provides accessors for the correspondence between deposition data identifiers and
deposition and annotation sites (e.g. wwpdb_site_id).

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
from oslo_concurrency import lockutils

from wwpdb.utils.config.ConfigInfo import ConfigInfo, getSiteId
from wwpdb.utils.config.ConfigInfoApp import ConfigInfoAppDepUI

logger = logging.getLogger(__name__)


class ConfigInfoDataSet(object):
    """
    Provides accessors for the correspondence between deposition data identifiers and
    deposition and annotation sites (e.g. wwpdb_site_id).

    """

    def __init__(self, verbose=False, log=sys.stderr):  # pylint: disable=unused-argument
        self.__verbose = verbose
        self.__debug = True
        self.__cI = ConfigInfo(siteId=None, verbose=self.__verbose)
        self.__cIDepUI = ConfigInfoAppDepUI(siteId=getSiteId())
        # Default data set id range assignments
        self.__depIdAssignments = self.__cI.get("SITE_DATASET_ID_ASSIGNMENT_DICTIONARY")
        self.__depTestIdAssignments = self.__cI.get("SITE_DATASET_TEST_ID_ASSIGNMENT_DICTIONARY")
        self.__siteBackupD = self.__cI.get("SITE_BACKUP_DICT", default={})
        self.__dsLocD = None
        #
        self.__lockDirPath = self.__cI.get("SITE_SERVICE_REGISTRATION_LOCKDIR_PATH", "/tmp")
        lockutils.set_defaults(self.__lockDirPath)

    def getSiteId(self, depSetId):
        """Return siteId for the input depSetId subject to site backup details -

        siteBackupD[prodSite] = [backupSite1, backupSite2,...]
        """
        siteId = self.__getSiteId(depSetId)
        mySiteId = self.__cI.get("SITE_PREFIX", default=None)
        #
        if mySiteId and siteId:
            # is mySiteId a backup for siteId?
            if siteId in self.__siteBackupD and mySiteId in self.__siteBackupD[siteId]:
                if self.__debug:
                    logger.debug("using backup %s for %s", mySiteId, siteId)
                siteId = mySiteId

        return siteId

    def getDataSetLocationDict(self):
        d = {}
        try:
            d = self.__readLocationDictionary()
            return d
        except Exception as e:
            logger.error("failed reading data set location dictionary: %s", str(e))
            if self.__debug:
                logger.exception("failed reading data set location dictionary")
        return d

    def getDataSetLocations(self, siteId):
        dsL = []
        try:
            d = self.__readLocationDictionary()
            for ky in d:
                if d[ky] == siteId:
                    dsL.append(ky)
            return dsL
        except Exception as e:
            logger.info("failed reading data set locations for site %r - %s", siteId, str(e))
            if self.__debug:
                logger.exception("failed reading data set locations for site %r - %s", siteId, str(e))
        return []

    def removeDataSets(self, dataSetIdList):
        try:
            d = self.__readLocationDictionary()
            for dsId in dataSetIdList:
                if dsId in d:
                    del d[dsId]
            return self.__writeLocationDictionary(d)
        except Exception as e:
            logger.error("failed %s", str(e))
            if self.__debug:
                logger.exception("failed")
        return False

    def writeLocationList(self, siteId, dataSetIdList):
        try:
            d = self.__readLocationDictionary()
            for dsId in dataSetIdList:
                d[dsId] = siteId
            return self.__writeLocationDictionary(d)
        except Exception as e:
            logger.error("failed data set locations for site %r - %s", siteId, str(e))
            if self.__debug:
                logger.exception("failed data set locations for site %rs", siteId)
        return False

    def __readLocationDictionary(self):
        """Read the dictionary cotaining data set site location information.

        Returns: d[<data_set_id>] = <site_id> or a empty dictionary.
        """
        fp = self.__cIDepUI.get_site_dataset_siteloc_file_path()
        try:
            with open(fp, "r") as infile:
                return json.load(infile)
        except Exception as e:
            logger.error("failed reading json resource file %s - %s", fp, str(e))
            if self.__debug:
                logger.exception("failed reading json resource file %s", fp)
        return {}

    @lockutils.synchronized("configdataset.exceptionfile-lock", external=True)
    def __writeLocationDictionary(self, dsLocD, backup=True):
        """Write the input dictionary cotaining exceptional data set to site correspondences,

        Returns: True for success or False otherwise
        """
        fp = self.__cIDepUI.get_site_dataset_siteloc_file_path()

        try:
            if backup:
                bp = fp + datetime.datetime.now().strftime("-%Y-%m-%d-%H-%M-%S")
                d = self.__readLocationDictionary()
                with open(bp, "w") as outfile:
                    json.dump(d, outfile, indent=4)
            #
            with open(fp, "w") as outfile:
                json.dump(dsLocD, outfile, indent=4)
            return True
        except Exception as e:
            logger.error("failed writing json resource file %s - %s", fp, str(e))
            if self.__debug:
                logger.exception("failed writing json resource file %s", fp)
        return False

    def getDefaultIdRange(self, siteId):
        """Return the default upper and lower deposition data set identifier codes
        assigned to the input siteId.

        Any site lacking a default range will get the range assigned to the UNASSIGNED site.

        Returns:   (lower bound, upper bound) for data set identifiers (int)
        """
        if siteId in self.__depIdAssignments:
            DEPID_START, DEPID_STOP = self.__depIdAssignments[siteId]
        elif "UNASSIGNED" in self.__depIdAssignments:
            DEPID_START, DEPID_STOP = self.__depIdAssignments["UNASSIGNED"]
        else:
            DEPID_START, DEPID_STOP = (-1, -1)
        return (DEPID_START, DEPID_STOP)

    def getTestIdRange(self, siteId):
        """Return the upper and lower deposition data set identifier codes
        assigned to the input siteId.

        Any site lacking a default range will get the range (-1, -1)

        Returns:   (lower bound, upper bound) for data set identifiers (int)
        """
        if siteId in self.__depTestIdAssignments:
            DEPID_START, DEPID_STOP = self.__depTestIdAssignments[siteId]
        else:
            DEPID_START, DEPID_STOP = (-1, -1)
        return (DEPID_START, DEPID_STOP)

    def getDefaultSiteId(self, depSetId):
        """Get the default site assignment for the input data set id."""
        return self.__getSiteId(depSetId)

    def __getSiteId(self, depSetId):
        """Return the siteId to which the input depSetId is within the default
        code assignment range.

        Input may be either a string "D_xxxxxxxxxx" or an integer/string "xxxxxxxxxx".

        """
        # check for exceptional cases --
        try:
            if self.__dsLocD is None:
                self.__dsLocD = self.__readLocationDictionary()
            if str(depSetId)[:2] == "D_":
                if depSetId in self.__dsLocD:
                    return self.__dsLocD[depSetId]
            else:
                tId = "D_" + str("%010d" % int(depSetId))
                if tId in self.__dsLocD:
                    return self.__dsLocD[tId]
        except Exception as e:
            if self.__debug:
                logger.exception("failed checking for exception dictionary for %r - %s", depSetId, str(e))
        #
        # check default range assignment --
        try:
            if str(depSetId).startswith("D_"):
                idVal = int(str(depSetId)[2:])
            else:
                idVal = int(str(depSetId))
            for ky in self.__depIdAssignments.keys():
                idMin, idMax = self.__depIdAssignments[ky]
                if (idVal >= idMin) and (idVal <= idMax):
                    return ky
        except Exception as e:
            if self.__debug:
                logger.exception("failed checking deposition range for %r - %s", depSetId, str(e))
        return None
