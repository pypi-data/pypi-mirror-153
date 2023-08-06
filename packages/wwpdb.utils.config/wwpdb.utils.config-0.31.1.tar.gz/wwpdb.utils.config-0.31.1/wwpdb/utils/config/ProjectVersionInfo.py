##
# File:    ProjectVersionInfo.py
# Author:  jdw
# Date:    23-Oct-2017
# Version: 0.001
#
# Updates:
#
##
"""
Accessor for project version information ...

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"
__version__ = "V0.01"

import os.path

import json
import logging
import os

from wwpdb.utils.config.ConfigInfoApp import ConfigInfoAppCommon

logger = logging.getLogger(__name__)


class ProjectVersionInfo(object):
    def __init__(self, siteId=None):
        self.__cICommon = ConfigInfoAppCommon(siteId)
        self.__top_webapps_path = self.__cICommon.get_site_web_apps_top_path()

    def getVersionFile(self):
        """
        returns the version json file path
        :return str: version json file path
        """
        return os.path.join(self.__top_webapps_path, "version.json")

    def getVersion(self):
        """Returns version number of system or "unknown" """

        try:
            file_name = self.getVersionFile()
            if os.path.exists(file_name):
                with open(file_name, "r") as fp:
                    version_dict = json.load(fp)
                return version_dict["Version"]
            else:
                return "unknown"
        except Exception as e:
            logger.exception(e)
            return "unknown"
