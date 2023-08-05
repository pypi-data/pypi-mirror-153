##
# File:  WebServiceApp.py
# Date:  3-July-2016 Jdw
#
# Updates:
#    7-Feb-2017  jdw adapt for content provider service
#
##
"""
Manage web request and response processing for various web services.

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

import logging

#
from wwpdb.utils.config.ConfigInfo import ConfigInfo
from wwpdb.utils.ws_utils.ServiceRequest import ServiceRequest
from wwpdb.utils.ws_utils.ServiceResponse import ServiceResponse

#
from wwpdb.apps.content_ws_server.webapp.ContentServiceAppWorker import (
    ContentServiceAppWorker,
)

logger = logging.getLogger()


class WebServiceApp(object):
    """Handle request and response object processing for various web services."""

    def __init__(self, parameterDict=None):
        """
        Create an instance of the appropriate worker class to manage input service request.

         :param `parameterDict`: dictionary storing parameter information from the input request.

        """
        if parameterDict is None:
            parameterDict = {}
        self.__reqObj = ServiceRequest(parameterDict)
        siteId = self.__reqObj.getSiteId()
        #
        cI = ConfigInfo(siteId)
        self.__reqObj.setTopSessionPath(cI.get("SITE_WEB_APPS_TOP_SESSIONS_PATH"))
        self.__reqObj.setRequestPathPrefix(cI.get("SITE_WEB_SERVICE_PATH_PREFIX", default="/service"))
        self.__reqObj.setDefaultReturnFormat(return_format="json")
        #

    def run(self):
        """Execute request and package results in response dictionary.

        :Returns:
             A dictionary containing response data for the input request.
             Minimally, the content of this dictionary will include the
             keys: CONTENT_TYPE and REQUEST_STRING.
        """

        requestPath = self.__reqObj.getRequestPath()
        logger.debug("Processing requiest path : %s", requestPath)
        #
        if requestPath.startswith("/contentws"):
            swrk = ContentServiceAppWorker(reqObj=self.__reqObj)
        else:
            swrk = ContentServiceAppWorker(reqObj=self.__reqObj)
        #
        #  Each class implements a run() method that returns a ServiceSessionState object -
        #
        sst = swrk.run()
        logger.debug("Service response object for request path: %s\n   %r", requestPath, sst.getAppDataDict())
        sr = self.__buildResponse(sst)
        #
        # Return only the dictionary from the response object -
        #
        return sr

    def __buildResponse(self, sst):
        """Using the content from the input service state object, build a service response object."""
        rD = {}
        sr = ServiceResponse(returnFormat="json", injectStatus=False)
        #
        if sst.getServiceErrorFlag():
            rD["errorflag"] = True
            rD["statusmessage"] = sst.getServiceErrorMessage()
            sr.setData(rD)
        elif sst.getResponseFormat() in ["json"]:
            rD["errorflag"] = False
            sm = sst.getServiceStatusText()
            if sm and len(sm) > 0:
                rD["statusmessage"] = sm
            else:
                rD["statusmessage"] = "ok"
            #
            rD.update(sst.getAppDataDict())
            sr.setData(rD)
        elif sst.getResponseFormat() in ["files"]:
            sr.setReturnFormat("binary")
            fL = sst.getDownloadList()
            ok = False
            for f in fL[0:1]:
                # f = (fileName, filePath, contentType, md5Digest)
                ok = sr.setBinaryFile(f[1], attachmentFlag=False, serveCompressed=True, md5Digest=f[3])
            if not ok:
                sr.setReturnFormat("json")
                rD["errorflag"] = True
                rD["statusmessage"] = "Download file not found"
                sr.setData(rD)
        else:
            rD["errorflag"] = True
            rD["statusmessage"] = "Miscellaneous error"
            sr.setData(rD)
        #
        #
        return sr
