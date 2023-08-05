##
# File:  ContentRequestProxyReportPdbx.py
# Date:  02-Jun-2017  E. Peisach. Westbrook
#
# Update:
##
"""
Fetch content and prepare report from PDBx content -

"""
__docformat__ = "restructuredtext en"
__author__ = "Ezra Peisach"
__email__ = "peisach@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.07"

import logging
import time

from onedep_biocuration.api.ContentRequest import ContentRequest
from wwpdb.utils.config.ConfigInfo import ConfigInfo, getSiteId

logger = logging.getLogger()


class ContentRequestProxyReportPdbx(object):
    """
    Fetch content and prepare report from PDBx content from a remote service using
    biocuration api.

    """

    def __init__(self, verbose=True):  # pylint: disable=unused-argument
        # self.__verbose = verbose
        self.__siteId = getSiteId(defaultSiteId=None)
        self.__cI = ConfigInfo(self.__siteId)
        # Max time to get a response
        self.__maxWait = 60
        logger.info("Starting with siteId %r", self.__siteId)
        #

    def __readApiKey(self, filePath):
        """Reads API key from file"""
        api_key = None
        try:
            with open(filePath, "r") as fp:
                api_key = fp.read()
        except Exception as e:
            logger.exception(e)

        return api_key

    def retrieveProxyReport(self, dataSetId, apiUrl, contentType, formatType, reportPath):
        """Retrieve a report from a remote server"""
        logger.debug("dataSetId %r apiUrl %r contentType %r reportPath %r", dataSetId, apiUrl, contentType, reportPath)

        apiKeyFileName = self.__cI.get("SITE_WS_CONTENT_WWPDB_KEY")
        apiKey = self.__readApiKey(apiKeyFileName)
        if not apiKey:
            logger.error("Could not read apiKeyFile %r", apiKeyFileName)
            return False

        cr = ContentRequest(apiKey=apiKey, apiUrl=apiUrl)

        # Need a session....
        rD = cr.createSession()
        if not rD or rD["onedep_error_flag"]:
            logger.error("Response from create session %r", rD)
            return False

        sessionId = rD["session_id"]
        logger.debug("sessionId %r", sessionId)

        rD = cr.requestEntryContent(dataSetId, contentType, formatType)
        if rD["onedep_error_flag"]:
            logger.error("Submitted content service failed request %r", rD)
            return False

        logger.debug("Submitted remote content reuqest")

        #
        #   Poll for service completion -
        #
        total = 0
        it = 0
        sl = 2
        while True:
            #    Pause -
            it += 1
            pause = it * it * sl
            time.sleep(pause)
            rD = cr.getStatus()
            if rD["status"] in ["completed", "failed"]:
                break
            logger.debug("[%4d] Pausing for %4d (seconds)", it, pause)
            total += pause
            # Timeout?
            if pause > self.__maxWait:
                logger.error("No response from remote service in %r", total)
                return False
        #
        logger.debug("Received response from remote %r", rD)

        if rD["status"] == "failed" or rD["onedep_error_flag"]:
            logger.error("Remote service request failed %r", rD)
            return False

        rD = cr.getOutputByType(reportPath, contentType, formatType=formatType)
        if rD["onedep_error_flag"]:
            logger.debug("getOutputByType failed %r", rD)
            return False

        # We have succeeded!!!!
        return True
