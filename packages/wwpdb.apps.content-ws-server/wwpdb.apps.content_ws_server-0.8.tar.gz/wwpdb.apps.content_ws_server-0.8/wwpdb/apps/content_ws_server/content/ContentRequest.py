##
# File:  ContentRequest.py
# Date:  14-Feb-2017  J. Westbrook
#
# Update:
#   16-Feb-2017 jdw add summary content request support --
#   14-Mar-2017 jdw remove some unused code and uncecessary file checks
##
"""
Manage invoking content request for web service -

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.07"

import copy
import os.path

import json
import logging
import os
import time

#
from wwpdb.utils.config.ConfigInfo import ConfigInfo, getSiteId
from wwpdb.utils.ws_utils.ServiceDataStore import ServiceDataStore
from wwpdb.utils.ws_utils.ServiceHistory import ServiceHistory

from wwpdb.apps.content_ws_server.content.ContentRequestPolicyFilter import ContentRequestPolicyFilter
from wwpdb.apps.content_ws_server.content.ContentRequestProxyReportPdbx import ContentRequestProxyReportPdbx
from wwpdb.apps.content_ws_server.content.ContentRequestReportDb import ContentRequestReportDb

#
from wwpdb.apps.content_ws_server.content.ContentRequestReportPdbx import ContentRequestReportPdbx

#
logger = logging.getLogger()


class ContentRequest(object):
    """
    Manage various request for entry and summary level content.

    """

    def __init__(self):

        self.__siteId = getSiteId(defaultSiteId=None)
        self.__cI = ConfigInfo(self.__siteId)
        logger.info("Starting with siteId %r", self.__siteId)
        self.__topSessionPath = self.__cI.get("SITE_WEB_APPS_TOP_SESSIONS_PATH")
        logger.info("Starting with session path %r", self.__topSessionPath)
        self.__sessionPath = None
        self.__sdsPrefix = None
        self.__sds = None
        self.__debugPayload = False
        #
        self.__pD = {}

    def setup(self, pD):
        logger.debug("Content request input payload %r", pD)
        try:
            self.__sessionPath = pD["session_path"]
            self.__sdsPrefix = pD["session_store_prefix"]
            self.__sds = ServiceDataStore(sessionPath=self.__sessionPath, prefix=self.__sdsPrefix)
            self.__sds.set("status", "running")
            #
            #  JDW not used
            # self.__sD = self.__sds.getDictionary()
            # logger.info("Session dictionary %r", self.__sD)
            #
            # logger.info("Preparing copy of dictionary")
            self.__pD = copy.deepcopy(pD)
            #
            if self.__debugPayload:
                logger.debug("Parameter dictionary copy %r", self.__pD)
            return True
        except Exception as e:
            logger.exception("Failing %s", str(e))

        return False

    def run(self):
        """Service execution method"""
        iD = {}
        #
        testMode = self.__pD.get("worker_test_mode", False)
        successFlag = False
        #
        if testMode:
            try:
                wSecs = int(self.__pD.get("worker_test_duration", 10))
                logger.info("Running in test mode with duration %d seconds", wSecs)
                time.sleep(wSecs)
            except Exception as e:
                logger.exception(e)

            try:
                ct = self.__pD["request_content_type"]
                fp = self.__pD["report_path"]
                fn = self.__pD["report_file"]
                with open(fp, "w") as ofh:
                    ofh.write("DUMMY")
                iD[ct] = (fn, "data")
                successFlag = True
            except Exception as e:
                logger.exception("Mock execution file update failing %s", str(e))
            #
            logger.info("Test mode service completed")
        else:
            #
            successFlag = self.__run(self.__pD)
            # Add the output files to the session store -
            ct = self.__pD["request_content_type"]
            fp = self.__pD["report_path"]
            fn = self.__pD["report_file"]
            #
            # JDW  - Move down
            # if os.access(fp, os.R_OK):
            #    iD[ct] = (fn, 'data')
            #
            # Add an additional existence tests for key report files -
            #
            if successFlag:
                fp = self.__pD["report_path"]
                if not os.access(fp, os.R_OK):
                    successFlag = False
                else:
                    successFlag = True
                    iD[ct] = (fn, "data")
        #
        if successFlag:
            iD["status"] = "completed"
        else:
            iD["status"] = "failed"
        #
        try:
            #
            # Update service activity tracking
            sH = ServiceHistory(historyPath=self.__pD["session_history_path"])
            sH.add(sessionId=self.__pD["session_id"], statusOp=iD["status"])
            logger.info("Updated service history store with %r", iD["status"])
            #
        except Exception as e:
            logger.exception("Failed to update session tracking history status %r", iD)
            logger.exception(e)

        try:
            #  Update session store -
            logger.info("Updated session store with %r", iD)
            self.__sds.updateAll(iD)
            #
            tStatus = self.__sds.get("status")
            logger.info("Read session store status as  %r", tStatus)
        except Exception as e:
            logger.exception("Failed to update session status %r", iD)
            logger.exception(e)
        #
        logger.info("Updated session store with: %r", iD)
        return True

    def __run(self, pD):
        """Create entry level and summary content reports  --"""
        ok = False
        try:
            #
            sessionPath = pD["session_path"]
            cI = ConfigInfo()
            siteId = cI.get("SITE_PREFIX")
            #
            dataSetId = pD["request_dataset_id"]
            contentType = pD["request_content_type"]
            reportFile = pD["report_file"]
            reportPath = pD["report_path"]
            proxyReportUrl = pD.get("session_proxy_url")

            if proxyReportUrl and contentType.startswith("report-entry-"):
                logger.debug("Forwarding request to another server for an entry")
                logger.debug("pD is %r", pD)
                formatType = pD.get("request_format_type")

                cr = ContentRequestProxyReportPdbx()
                # Need to test for rejection - id not found and forward back errors
                status = cr.retrieveProxyReport(dataSetId, proxyReportUrl, contentType, formatType, reportPath)

                ok = status

            elif contentType.startswith("report-entry-"):
                cr = ContentRequestReportPdbx()
                ctypeL = cr.getContentTypes()
                if contentType in ctypeL:
                    logger.debug("Processing content definition %r", contentType)
                    logFilePath = os.path.join(self.__sessionPath, dataSetId + " -parser.log")
                    pdbxFilePath = pD["session_pdbx_file_path"]
                    #
                    rD = cr.extractContent(pdbxFilePath, logFilePath, contentType)
                    cF = ContentRequestPolicyFilter()
                    # Filter content based on contentType policies
                    rD = cF.filterContent(contentType, rD)
                    if self.__debugPayload:
                        logger.debug("File content %r", rD)
                    ss = json.dumps(rD)
                    if self.__debugPayload:
                        logger.info("JSON serialized result %r", ss)
                    with open(reportPath, "w") as ofh:
                        ofh.write(ss)
                    ok = True
            elif contentType.startswith("report-summary-"):
                site = self.__siteId
                qs = pD["query_site"]
                if qs is not None:
                    site = qs
                cr = ContentRequestReportDb(siteId=site)
                ctL = cr.getContentTypes()
                if contentType in ctL:
                    rD = cr.extractContent(contentType)
                    logger.info("Database content length %r", len(rD))
                    ss = json.dumps(rD)
                    logger.info("JSON serialized result length %r", len(ss))
                    with open(reportPath, "w") as ofh:
                        ofh.write(ss)
                    ok = True
            else:
                ok = False
            #
            logger.info(" - Site Id: %r", siteId)
            logger.info(" - Session path: %r", sessionPath)
            logger.info(" - Dataset Id:   %r", dataSetId)
            logger.info(" - Content Type: %r", contentType)
            logger.info(" - Report file: %r", reportFile)
            logger.info(" - Report path: %r", reportPath)
            logger.info(" - Return status: %r", ok)

            return ok
        except Exception as e:
            logger.exception("Failing content request runner method %s", str(e))

        return False
        #
