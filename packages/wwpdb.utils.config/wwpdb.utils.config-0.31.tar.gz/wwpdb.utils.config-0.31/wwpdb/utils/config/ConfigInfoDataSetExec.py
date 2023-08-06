#!/usr/bin/env python
##
# File:    ConfigInfoDataSetExec.py
# Author:  jdw
# Date:    23-Aug-2016
# Version: 0.001
#
# Updates:
##
"""
Execuction wrapper for data set site alternate location mapping cache.
"""

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.001"

import sys
import traceback
from optparse import OptionParser  # pylint: disable=deprecated-module
import logging

from wwpdb.utils.config.ConfigInfoDataSet import ConfigInfoDataSet

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ConfigInfoDataSetExec(object):
    """
    Execuction wrapper for data set site alternate location mapping cache.

    """

    def __init__(self, verbose=True, log=sys.stderr):
        self.__lfh = log
        self.__verbose = verbose
        #

    def checkConfig(self):
        """Perform read check for the data set configuration file."""
        try:
            cfds = ConfigInfoDataSet(self.__verbose, self.__lfh)
            d = cfds.getDataSetLocationDict()
            self.__lfh.write("Alternate site location dictionary length = %d\n" % len(d))
            sD = {}
            for ky in d:
                if d[ky] not in sD:
                    sD[d[ky]] = 0
                sD[d[ky]] += 1
            #
            for ky in sD:
                self.__lfh.write("  Site %-40r   count %8d\n" % (ky, sD[ky]))
        except Exception as e:
            self.__lfh.write("checkConfig failing %r\n" % str(e))
            traceback.print_exc(file=self.__lfh)

    def printConfig(self, siteId):
        """Print the configuration options for the input site."""
        try:
            cfds = ConfigInfoDataSet(self.__verbose, self.__lfh)
            (lId, uId) = cfds.getDefaultIdRange(siteId=siteId)
            self.__lfh.write(" Default data set range for site %-30s lower %-12d upper %-12d \n" % (siteId, lId, uId))
            #
            dataSetIdL = cfds.getDataSetLocations(siteId)
            nDataSets = len(dataSetIdL)
            for ii, dataSetId in enumerate(sorted(dataSetIdL)):
                self.__lfh.write("    %-8d - %12s\n" % (ii, dataSetId))
            self.__lfh.write("  Total alternate data set locations = %d" % nDataSets)
        except Exception as e:
            self.__lfh.write("printConfig failing for site %r - %r\n" % (siteId, str(e)))
            traceback.print_exc(file=self.__lfh)

    def setLocations(self, siteId, dataSetIdList):
        """Set the site location for the input data list."""
        try:
            cfds = ConfigInfoDataSet(self.__verbose, self.__lfh)
            return cfds.writeLocationList(siteId, dataSetIdList)
        except Exception as e:
            self.__lfh.write("setLocations failing for site %r - %r\n" % (siteId, str(e)))
            traceback.print_exc(file=self.__lfh)

    def removeDataSets(self, dataSetIdList):
        try:
            cfds = ConfigInfoDataSet(self.__verbose, self.__lfh)
            return cfds.removeDataSets(dataSetIdList)
        except Exception as e:
            self.__lfh.write("removeDataSets failing %s\n" % str(e))
            traceback.print_exc(file=self.__lfh)


def main():  # pragma: no cover
    usage = """usage: %prog [options]

    Examples:

     Read check the data set location configuration file:

       python %prog --check

     Print the data set configuration for a site (requires --siteid):

       python %prog --print --siteid=WWPDB_DEPLOY_TEST_RU

     Set alternative location for data set(s) to site (requires --siteid):

       python %prog --set --siteid=WWPDB_DEPLOY_TEST_RU --dataset D_0000000000
       python %prog --set --siteid=WWPDB_DEPLOY_TEST_RU --dataset_file  <datsetid_file>

     Remove data set from alternate location configuration file:

       python %prog --remove --siteid=WWPDB_DEPLOY_TEST_RU --dataset D_0000000000
       python %prog --remove --siteid=WWPDB_DEPLOY_TEST_RU --dataset_file  <datsetid_file>


    """
    parser = OptionParser(usage)

    parser.add_option("--check", dest="checkConfig", action="store_true", default=False, help="Check data set configuration file")
    parser.add_option("--print", dest="printConfig", action="store_true", default=False, help="Print the data set configuration for a site (--siteid)")
    parser.add_option("--siteid", dest="siteId", default=None, help="wwPDB site ID (e.g. WWPDB_DEPLOY_TEST_RU)")

    parser.add_option("--set", dest="setOp", action="store_true", default=False, help="Set alternative data set location")
    parser.add_option("--remove", dest="removeOp", action="store_true", default=False, help="Remove data set alternative location")

    parser.add_option("--dataset", dest="dataSetId", default=None, help="Data set identifier (e.g. D_0000000000)")
    parser.add_option("--dataset_file", dest="dataSetIdFile", default=None, help="File containing a list of data sets one per line")
    parser.add_option("-v", "--verbose", default=True, action="store_true", dest="verbose")

    (options, args) = parser.parse_args()  # pylint: disable=unused-variable

    #
    # Fetch any input data set list  ---
    #
    dsL = []
    if options.dataSetIdFile:
        try:
            with open(options.dataSetIdFile, "r") as ifh:
                for line in ifh:
                    dsL.append(str(line[:-1]).strip())
        except Exception as e:
            sys.stderr.write("main() read failed for %r %r\n" % (options.dataSetIdFile, str(e)))
    elif options.dataSetId:
        dsL = [options.dataSetId]

    ciEx = ConfigInfoDataSetExec(verbose=options.verbose, log=sys.stderr)
    #
    if options.checkConfig:
        ciEx.checkConfig()

    if options.printConfig and options.siteId:
        ciEx.printConfig(siteId=options.siteId)

    if len(dsL) > 0:
        if options.setOp and options.siteId:
            ciEx.setLocations(options.siteId, dsL)
        elif options.removeOp:
            ciEx.removeDataSets(dsL)


if __name__ == "__main__":
    main()
