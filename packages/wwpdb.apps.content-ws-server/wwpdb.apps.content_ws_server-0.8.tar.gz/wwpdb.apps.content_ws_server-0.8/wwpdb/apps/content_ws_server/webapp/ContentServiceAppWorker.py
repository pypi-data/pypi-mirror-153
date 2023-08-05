##
# File:  ContentServiceAppWorker.py
# Date:  8-Feb-2017  J.Westbrook
#
# Updates:
#   18-Feb-2017 jdw Change search approach for model file -
#   15-Mar-2017 ep  For model file, invoke DepUI to produce model
#   16-Mar-2017 jdw Change status tracking to avoid collisions
##
"""
Manage web request and response processing for miscellaneous annotation tasks.

This software was developed as part of the World Wide Protein Data Bank
Common Deposition and Annotation System Project

Copyright (c) wwPDB

This software is provided under a Creative Commons Attribution 3.0 Unported
License described at http://creativecommons.org/licenses/by/3.0/.

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.07"

import glob

import datetime
import json
import logging
import os
import signal
import time
from subprocess import Popen, PIPE
from wwpdb.io.file.DataExchange import DataExchange
from wwpdb.io.locator.PathInfo import PathInfo
from wwpdb.utils.config.ConfigInfo import getSiteId
from wwpdb.utils.config.ConfigInfoDataSet import ConfigInfoDataSet
from wwpdb.utils.message_queue.MessagePublisher import MessagePublisher
from wwpdb.utils.ws_utils.ServiceSessionState import ServiceSessionState
from wwpdb.utils.ws_utils.ServiceUploadUtils import ServiceUploadUtils
from wwpdb.utils.ws_utils.ServiceUtilsMisc import getMD5
from wwpdb.utils.ws_utils.ServiceWorkerBase import ServiceWorkerBase

from wwpdb.apps.content_ws_server.message_queue.MessageQueue import get_queue_name, get_routing_key, get_exchange_name

logger = logging.getLogger(__name__)


class ContentServiceAppWorker(ServiceWorkerBase):
    def __init__(self, reqObj=None, sessionDataPrefix=None):
        """
        Worker methods for annotation tasks.

        Performs URL - application mapping and application launching
        for annotation tasks module.

        """
        super(ContentServiceAppWorker, self).__init__(reqObj=reqObj, sessionDataPrefix=sessionDataPrefix)
        #
        #  URL to method mapping -----  the service names are case insensitive --
        #
        self.__appPathD = {
            "/contentws/dump": "_dumpOp",
            "/contentws/session": "_sessionOp",
            "/contentws/upload": "_uploadFileOp",
            "/contentws/input_file": "_uploadFileOp",
            "/contentws/sessioninfo": "_sessionInfoOp",
            "/contentws/session_status": "_sessionInfoOp",
            "/contentws/download": "_downloadOp",
            "/contentws/output_file": "_uploadFileOp",
            "/contentws/submit": "_submitReportOp",
            "/contentws/entry_content": "_submitContentRequestOp",
            "/contentws/summary_content": "_submitContentRequestOp",
            "/contentws/index": "_indexOp",
            "/contentws/session_index": "_indexOp",
            "/contentws/session_activity": "_activityOp",
            "/contentws/activity": "_activityOp",
        }
        self.addServices(self.__appPathD)
        #

    def run(self, reqPath=None):

        #
        inpRequestPath = reqPath if reqPath else self._reqObj.getRequestPath()
        #
        # First pull off the REST style URLS --
        #
        #  /contentws/report/X_XXXXXX
        #
        logger.debug("Request prefix %s", self._reqObj.getRequestPathPrefix())
        logger.debug("Request path   %s", self._reqObj.getRequestPath())
        logger.debug("Request inp path %s", inpRequestPath)
        #
        if inpRequestPath.startswith("/contentws/report/d_"):
            rFields = inpRequestPath.split("/")
            self._reqObj.setValue("idcode", rFields[4].upper())
            requestPath = "/review/report"
        else:
            requestPath = inpRequestPath
        #
        return self._run(requestPath)

    def _dumpOp(self):
        """Dump the request object dictionary ----"""
        logger.debug("Starting now")
        sst = ServiceSessionState()
        rD = self._reqObj.getDictionary()
        sst.setAppDataDict(rD, format="json")
        logger.debug("Completed")
        return sst

    def _sessionInfoOp(self):

        logger.debug("Starting now")
        sst = ServiceSessionState()
        #            join an existing session -
        ok = self._getSession(new=False, useContext=True, contextOverWrite=True)
        if not ok:
            sst.setServiceCompletionFlag(ok)
            sst.setServiceError(msg="Session acquire failed")
        else:
            sst.setServiceCompletionFlag(ok)
            sD = self._getSessionStoreDict()
            if "session_history" in sD:
                shL = sD["session_history"]
            else:
                shL = []
            if "status" in sD:
                status = sD["status"]
            else:
                status = "unknown"
            sst.setAppDataDict(
                {
                    "session_id": self._sessionId,
                    "status": status,
                    "session_history": shL,
                },
                format="json",
            )
        #
        logger.debug("Completed")
        return sst

    def _sessionOp(self):
        """Create a new session -

        :Returns: sst service session state object

        """
        logger.debug("Starting now")
        sst = ServiceSessionState()
        #            Create a new session -
        ok = self._getSession(new=True, useContext=True, contextOverWrite=True)
        if not ok:
            sst.setServiceCompletionFlag(ok)
            sst.setServiceError(msg="Session creation failed")
        else:
            self._trackServiceStatus("created")
            self._setSessionStoreValue("status", "newsession")
            sst.setServiceCompletionFlag(ok)
            sst.setAppDataDict({"session_id": self._sessionId}, format="json")
        #
        logger.debug("Completed")
        return sst

    def _uploadFileOp(self):
        """Upload callback method -- for model and experimental files -

        Copy input model and experimental data files to the current session directory and
        return file name and entry id details to the caller.

        """

        try:
            logger.debug("Starting now")
            sst = ServiceSessionState()
            #            join an existing session -
            ok = self._getSession(new=False, useContext=True, contextOverWrite=True)
            if not ok:
                sst.setServiceError(msg="Session acquire failed")
            else:
                suu = ServiceUploadUtils(reqObj=self._reqObj)
                if not suu.isFileUpload():
                    sst.setServiceError(msg="No input file in request ")
                else:
                    fileName = suu.copyToSession(fileTag="file")
                    if fileName:
                        sst.setServiceCompletionFlag(True)
                        sst.setServiceStatusText("Upload successful")
                        #
                        contentType = self._reqObj.getValue("content_type")
                        fileFormat = self._reqObj.getValue("file_format")
                        self._setSessionStoreValue(contentType, (fileName, fileFormat))
                        #
                        sD = self._getSessionStoreDict()
                        if "session_history" in sD:
                            shL = sD["session_history"]
                        else:
                            shL = []
                        sst.setAppDataDict(
                            {"session_id": self._sessionId, "session_history": shL},
                            format="json",
                        )
                        self._setSessionStoreValue("status", "uploading")
                        # self._trackServiceStatus('uploading', {'file': fileName})
                        self._trackServiceStatus("uploading", file=fileName)
                    else:
                        sst.setServiceError(msg="File upload failed")
        except Exception as e:
            logger.exception("FAILING")
            logger.exception(e)
            sst = ServiceSessionState()
            sst.setServiceError(msg="File upload failed")

        return sst

    def __fetchModelFile(self, siteId, entryId):
        """Fetch model file first from archive then from the deposit file source ..."""
        generateModel = True

        pdbxFilePath = None
        # Sanity check
        if len(entryId) > 30:
            return None
        try:
            logger.debug("siteId %r ", siteId)
            # note explict use of siteId here --
            dx = DataExchange(
                reqObj=self._reqObj,
                depDataSetId=entryId,
                fileSource="archive",
                siteId=siteId,
                verbose=True,
            )
            fl = dx.getContentTypeFileList(fileSource="archive", contentTypeList=["model"])
            if len(fl) > 0:
                pdbxFilePath = dx.fetch(contentType="model", formatType="pdbx", version="latest")
            elif generateModel:
                pdbxFilePath = self.__depuiGenerateModelFile(siteId, entryId)

            # Fallback on deposit directory
            if not pdbxFilePath:
                dx = DataExchange(
                    reqObj=self._reqObj,
                    depDataSetId=entryId,
                    fileSource="deposit",
                    siteId=siteId,
                    verbose=True,
                )
                pdbxFilePath = dx.fetch(contentType="model", formatType="pdbx", version="latest")

        except Exception as e:
            logger.exception("Fetch model failing %r", entryId)
            logger.exception(e)
        return pdbxFilePath

    def __depuiGenerateModelFile(self, siteId, entryId):
        """Uses code in the deposition system to generate a model file in the session directory.
        returns path to filename or None if it fails
        """
        logger.debug("generate %r from depui", entryId)
        sessDir = self._reqObj.getSessionObj().getPath()

        # Create script to run. Django will need WWPDB_SITE_ID set before invoking
        cmdPy = os.path.join(sessDir, "generate.py")
        fOut = open(cmdPy, "w")
        fOut.write("#!/usr/bin/env python\n")
        fOut.write("import os, sys\n")
        # Setup the Django environment
        fOut.write('os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wwpdb.apps.deposit.settings")\n')
        fOut.write("import django\n")
        fOut.write("django.setup()\n")
        fOut.write("from wwpdb.apps.deposit.depui.generate_model import generate_model\n")
        fOut.write('generate_model(depID="%s", sessionDir = "%s").write_out_cif_from_depui()' % (entryId, sessDir))
        fOut.close()
        cmdfile = os.path.join(sessDir, "generate.sh")
        fOut = open(cmdfile, "w")
        fOut.write("#!/bin/sh\n")
        fOut.write("export WWPDB_SITE_ID=%s\n" % siteId)
        fOut.write("export PYTHONPATH=$TOP_WWPDB_PYTHON_DIR/wwpdb/apps/deposit:$PYTHONPATH\n")
        fOut.write("python %s\n" % cmdPy)
        fOut.close()
        os.chmod(cmdfile, 0o777)

        logfile = os.path.join(sessDir, "generate.log")

        retCode = self.__runTimeout(cmdFile=cmdfile, logFile=logfile, timeout=30)

        logger.debug("response from depui %r", retCode)
        if retCode != 0:
            return None
        pI = PathInfo(siteId=self._siteId, sessionPath=sessDir, verbose=True)
        pdbxFilePath = pI.getModelPdbxFilePath(dataSetId=entryId, fileSource="session")
        # DepUI can generate file even if deposition non-existant!! Make sure minimal size....
        if os.access(pdbxFilePath, os.R_OK):
            statinfo = os.stat(pdbxFilePath)
            if statinfo.st_size > 100:
                return pdbxFilePath

        return None

    def _submitContentRequestOp(self):
        """Submit entry content service request  -"""
        logger.debug("Content request method starting now")
        sst = ServiceSessionState()
        #            Join an existing session -
        ok = self._getSession(new=False, useContext=True, contextOverWrite=True)
        if not ok:
            sst.setServiceCompletionFlag(ok)
            sst.setServiceError(msg="Session acquire failed")
        else:
            sD = self._getSessionStoreDict()
            ok = False
            pD = {}
            #
            #   Check for a test request
            #
            pD["worker_test_mode"] = self._reqObj.getValueOrDefault("worker_test_mode", default=False)
            pD["worker_test_duration"] = self._reqObj.getValueOrDefault("worker_test_duration", default=1)
            pD["exp_method"] = self._reqObj.getValueOrDefault("exp_method", default="unassigned")
            #
            pD["request_dataset_id"] = self._reqObj.getValueOrDefault("request_dataset_id", default="unassigned")
            pD["request_content_type"] = self._reqObj.getValueOrDefault("request_content_type", default="unassigned")
            pD["request_format_type"] = self._reqObj.getValueOrDefault("request_format_type", default="unassigned")
            #
            entryId = pD["request_dataset_id"]
            contentType = pD["request_content_type"]
            formatType = pD["request_format_type"]
            #
            # First check if we are handling this entry... If
            # config variable not set - will return ['None']
            siteCoverage = [x.strip() for x in str(self._cI.get("SITE_WS_CONTENT_SITE_COVERAGE")).split(",")]

            # Content type
            if entryId != "unassigned" and contentType.startswith("report-entry-"):
                ok = True
                fName = entryId + "_" + contentType + "." + formatType
                logger.debug("Entry content type %r format type %r and dataset id %r status %r", contentType, formatType, entryId, ok)

                cIDS = ConfigInfoDataSet()
                siteId = cIDS.getSiteId(entryId)

                # On development server
                if siteId == "UNASSIGNED":
                    siteId = self._siteId

                logger.debug("Entry siteid is %r", siteId)

                logger.debug("Entry %r my site %r cover %r", siteId, self._siteId, siteCoverage)
                if siteId != self._siteId and siteId not in siteCoverage:
                    logger.debug("Entry %r resides on another site %r", entryId, siteId)

                    # Simple lookup if we can redirect
                    siteMap = self._cI.get("PROJECT_CONTENTWS_SERVICE_DICTIONARY")
                    contentWsUrl = siteMap.get(siteId, None)
                    logger.debug("Alternate site to contact is %r", contentWsUrl)
                    if contentWsUrl:
                        pD["session_proxy_url"] = contentWsUrl
                    else:
                        ok = False
                else:
                    # Look up with siteId info for depositions
                    pdbxFilePath = self.__fetchModelFile(siteId, entryId)
                    if os.access(pdbxFilePath, os.R_OK):
                        pD["session_pdbx_file_path"] = str(pdbxFilePath)
                    else:
                        ok = False

            elif contentType.startswith("report-summary-"):
                ok = True
                fName = contentType + "." + formatType

                # Check if our site can handle...
                qs = self._reqObj.getValueOrDefault("query_site", default=None)

                # Check if request is for a separate site and if can access
                if qs and qs != self._siteId and qs not in siteCoverage:
                    logger.error("Request for %s but not in %s or %s", qs, self._siteId, siteCoverage)
                    ok = False

                pD["query_site"] = qs

                logger.debug("Summary content type %r format type %r site %s status %r", contentType, formatType, qs, ok)

            if ok:
                resultPath = os.path.join(self._sessionPath, fName)
                pD["report_file"] = fName
                pD["report_path"] = resultPath

                # Not really used in this example -
                dstPathList = [resultPath]
                pD["dst_file_path_list"] = dstPathList
                #
                pD["session_path"] = self._sessionPath
                pD["session_store_prefix"] = self._sdsPrefix
                pD["session_history_path"] = self._reqObj.getSessionUserPath()
                pD["session_id"] = self._sessionId
                #
                logger.debug("Request payload %r", pD)

                pStatus = sD["status"]
                try:
                    # preset the status as the request may be serviced immediately
                    self._setSessionStoreValue("status", "submitted")
                    self._trackServiceStatus("submitted")
                    ok = self.__publishRequest(pD)
                    logger.debug("Publish method return status %r", ok)
                except Exception as e:
                    logger.exception("Failed publish method %s", str(e))
                    ok = False

                if not ok:
                    # restore the prior status
                    self._setSessionStoreValue("status", pStatus)

            if "session_history" in sD:
                shL = sD["session_history"]
            else:
                shL = []
            #
            if ok:
                sst.setAppDataDict(
                    {"session_id": self._sessionId, "session_history": shL},
                    format="json",
                )
                sst.setServiceCompletionFlag(ok)
                sst.setServiceStatusText("Submit successful")

            else:
                sst.setServiceCompletionFlag(False)
                sst.setServiceError(msg="Submit operation failed")
        #
        logger.debug("Completed request method")
        return sst

    def __publishRequest(self, pD):
        ok = False
        logger.debug("Publishing request with payload %r", pD)
        try:
            siteID = getSiteId()
            msg = json.dumps(pD)
            mp = MessagePublisher()
            ok = mp.publish(
                msg,
                exchangeName=get_exchange_name(),
                queueName=get_queue_name(site_id=siteID),
                routingKey=get_routing_key(),
            )
        except Exception as e:
            logger.exception("Failing publish request %s", str(e))
        return ok

    ##
    def _indexOp(self):
        """Returns an index of service output files -"""
        sst = ServiceSessionState()
        #            join an existing session -
        ok = self._getSession(new=False, useContext=True, contextOverWrite=True)
        if not ok:
            sst.setServiceCompletionFlag(ok)
            sst.setServiceError(msg="Session acquire failed")
        else:
            try:
                sD = self._getSessionStoreDict()
                if "session_history" in sD:
                    shL = sD["session_history"]
                else:
                    shL = []
                dD = {"session_id": self._sessionId, "session_history": shL}
                #
                rD = {}
                fpList = glob.glob(self._sessionPath + "/*")
                for fp in fpList:
                    if os.access(fp, os.R_OK):
                        _pth, fName = os.path.split(fp)
                        (_fn, ft) = os.path.splitext(fName)
                        rD[fName] = (fName, ft[1:])
                dD["index"] = rD
                sst.setAppDataDict(dD, format="json")
                sst.setServiceCompletionFlag(True)
                sst.setServiceStatusText("Index length %d" % len(rD))
            except Exception as e:
                logger.exception("I updating session history %s", str(e))
                dD["index"] = rD
                sst.setAppDataDict(dD, format="json")
                sst.setServiceCompletionFlag(True)
                sst.setServiceError(msg="Index is empty")

        logger.debug("Completed index method")
        return sst

    ##
    def _downloadOp(self):
        """Download a file in the current session by type or by name -"""
        logger.debug("Starting now")
        sst = ServiceSessionState()
        try:
            #     - join an existing session -
            ok = self._getSession(new=False, useContext=True, contextOverWrite=True)
            if not ok:
                sst.setServiceCompletionFlag(ok)
                sst.setServiceError(msg="Session acquire failed")
            else:
                ct = self._reqObj.getValue("contenttype")
                sD = self._getSessionStoreDict()
                logger.debug("Session store keys %r ", sD.keys())
                logger.debug("Content type %r ", ct)
                #
                if ct in sD:
                    fn, _fmt = sD[ct]
                else:
                    fn = self._reqObj.getValue("filename")

                fp = os.path.join(self._sessionPath, fn)
                logger.debug("download target path %r", fp)
                md5Digest = getMD5(fp, block_size=4096, hr=True)
                sst.setDownload(fn, fp, contentType=None, md5Digest=md5Digest)
                # self._trackServiceStatus('downloading', {'file': fn})
                self._trackServiceStatus("downloading", file=fn)
        except Exception as e:
            logger.exception("FAILING %s", str(e))
            sst.setServiceCompletionFlag(False)
            sst.setServiceError(msg="File download failed")

        return sst

    def _activityOp(self):
        """Returns a summary of service activity  - for authenticated sessions -"""
        sst = ServiceSessionState()
        #            join an existing session -
        ok = self._getSession(new=False, useContext=True, contextOverWrite=True)
        if not ok:
            sst.setServiceCompletionFlag(ok)
            sst.setServiceError(msg="Session acquire failed")
        else:
            if self._reqObj.getValue("service_user_id") == "CONTENTWS_ANONYMOUS":
                dD = {
                    "session_id": self._sessionId,
                    "session_history": [],
                    "activity_summary": {},
                }
                sst.setAppDataDict(dD, format="json")
                sst.setServiceCompletionFlag(True)
                sst.setServiceError(msg="Activity history is not available")
            else:
                try:
                    sD = self._getSessionStoreDict()
                    if "session_history" in sD:
                        shL = sD["session_history"]
                    else:
                        shL = []
                    dD = {"session_id": self._sessionId, "session_history": shL}
                    #
                    dD["activity_summary"] = self._getServiceActivitySummary()
                    sst.setAppDataDict(dD, format="json")
                    sst.setServiceCompletionFlag(True)
                    sst.setServiceStatusText("Activity history length %d" % len(dD["activity_summary"]))
                except Exception as e:
                    logger.exception("Updating session store dict %s", str(e))
                    dD["activity_summary"] = {}
                    sst.setAppDataDict(dD, format="json")
                    sst.setServiceCompletionFlag(True)
                    sst.setServiceError(msg="Activity history is empty")

        logger.debug("Completed history summary method")
        return sst

    def __runTimeout(self, cmdFile=None, logFile=None, timeout=10):
        """Execute the command as a subprocess with a timeout."""
        logger.debug("STARTING with time out set at %d (seconds)", timeout)
        #
        start = datetime.datetime.now()
        try:
            process = Popen(  # pylint: disable=subprocess-popen-preexec-fn
                cmdFile,
                stdout=PIPE,
                stderr=PIPE,
                shell=False,
                close_fds=True,
                preexec_fn=os.setsid,
            )
            while process.poll() is None:
                time.sleep(0.1)
                now = datetime.datetime.now()
                if (now - start).seconds > timeout:
                    os.killpg(process.pid, signal.SIGKILL)
                    os.waitpid(-1, os.WNOHANG)
                    logger.debug("Execution terminated by timeout %d (seconds)", timeout)
                    if logFile is not None:
                        ofh = open(logFile, "a")
                        ofh.write("Execution terminated by timeout %d (seconds)\n" % timeout)
                        ofh.close()
                    #
                    return None
                #
                #
        except Exception as e:
            logger.error("Exception", exc_info=True)
            logger.error(e)
        #
        output = process.communicate()
        logger.debug("completed with stdout data %r", output[0])
        logger.debug("completed with stderr data %r", output[1])
        logger.debug("completed with return code %r", process.returncode)
        return process.returncode

    #
