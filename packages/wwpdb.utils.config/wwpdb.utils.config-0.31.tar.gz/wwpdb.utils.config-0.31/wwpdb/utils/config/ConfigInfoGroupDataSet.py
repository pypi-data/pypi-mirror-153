##
# File:    ConfigInfoGroupDataSet.py
# Date:    23-Oct-2016
#
# Updates:
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
import logging

from wwpdb.utils.config.ConfigInfo import ConfigInfo

logger = logging.getLogger(__name__)


class ConfigInfoGroupDataSet(object):
    """
    Provides accessors for the correspondence between group deposition data identifiers and
    deposition and annotation sites (e.g. wwpdb_site_id).

    """

    def __init__(self, verbose=False, log=sys.stderr):  # pylint: disable=unused-argument
        self.__verbose = verbose
        self.__debug = True
        self.__cI = ConfigInfo(siteId=None, verbose=self.__verbose)
        self.__groupIdAssignments = self.__cI.get("SITE_GROUP_DATASET_ID_ASSIGNMENT_DICTIONARY")

    def getDefaultGroupIdRange(self, siteId):
        """Return the default upper and lower group deposition data set identifier codes
        assigned to the input siteId.

        Any site lacking a default range will get return tuple (-1,-1)

        Returns:   (lower bound, upper bound) for data set identifiers (int)
        """
        if siteId in self.__groupIdAssignments:
            GID_START, GID_STOP = self.__groupIdAssignments[siteId]
        # elif 'UNASSIGNED' in self.__groupIdAssignments:
        #    GID_START, GID_STOP = self.__groupIdAssignments['UNASSIGNED']
        else:
            GID_START, GID_STOP = (-1, -1)
        return (GID_START, GID_STOP)

    def getDefaultSiteId(self, groupId):
        """Get the default site assignment for the input group data set id."""
        return self.__getSiteIdForGroup(groupId)

    def __getSiteIdForGroup(self, groupId):
        """Return the siteId to which the input groupId is within the default
        code assignment range.

        Input may be either a string "G_xxxxxxx" or an integer/string "xxxxxx".

        """
        # check default group range assignment --
        try:
            if str(groupId).startswith("G_"):
                idVal = int(str(groupId)[2:])
            else:
                idVal = int(str(groupId))
            #
            for ky in self.__groupIdAssignments.keys():
                idMin, idMax = self.__groupIdAssignments[ky]
                if (idVal >= idMin) and (idVal <= idMax):
                    return ky
        except Exception as e:
            if self.__debug:
                logger.exception("failed checking group range for %r with %s", groupId, str(e))

        return None
