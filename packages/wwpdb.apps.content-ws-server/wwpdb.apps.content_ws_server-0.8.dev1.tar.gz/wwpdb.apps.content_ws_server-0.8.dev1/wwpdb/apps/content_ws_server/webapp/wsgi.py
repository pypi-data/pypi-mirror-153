##
# File:     doServiceRequest.wsgi
# Created:  10-Feb-2017
# Updates:
#     17-Feb-2017  jdw add auth filtering on content request type ---
##
"""
This top-level responder for web service requests ...

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.07"

import datetime
import logging
from webob import Request
from wwpdb.utils.config.ConfigInfo import getSiteId
from wwpdb.utils.ws_utils.ServiceResponse import ServiceResponse
from wwpdb.utils.ws_utils.TokenUtils import JwtTokenReader

from wwpdb.apps.content_ws_server.webapp.WebServiceApp import WebServiceApp

USEKEY = True
# Create logger
FORMAT = "[%(levelname)s]-%(module)s.%(funcName)s: %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger()
#
# Note:  Don't add another handler as this will cause apache to duplicate log records --
# ch = logging.StreamHandler()
# formatter = logging.Formatter('[%(levelname)s]-%(module)s.%(funcName)s: %(message)s')
# ch.setFormatter(formatter)
# logger.addHandler(ch)
#
logger.setLevel(logging.DEBUG)


class MyRequestApp(object):
    """Process request and response from WSGI server using WebOb Request/Response objects."""

    def __init__(self, serviceName="ContentServiceApp", authVerifyFlag=True):
        """ """
        self.__serviceName = serviceName
        self.__authVerifyFlag = authVerifyFlag
        #

    def __dumpRequest(self, request):
        outL = []
        outL.append("%s" % ("-" * 80))
        outL.append("Web server request data content:")
        try:
            outL.append("Host:            %s" % request.host)
            outL.append("Remote host:     %s" % request.remote_addr)
            outL.append("Path:            %s" % request.path)
            outL.append("Method:          %s" % request.method)
            outL.append("wwpdb-api-token: %s" % request.headers.get("wwpdb-api-token"))
            outL.append("Headers:         %r" % sorted(request.headers.items()))
            # outL.append("Environ:         %r" % sorted(request.environ.items()))
            outL.append("Query string:    %s" % request.query_string)
            outL.append("Parameter List:")
            for name, value in request.params.items():
                outL.append("  ++  Request parameter:    %s:  %r\n" % (name, value))
        except Exception as e:
            logger.exception("FAILING for service %s", self.__serviceName)
            logger.exception(e)
        return outL

    def __isHeaderApiToken(self, request):
        try:
            tok = request.headers.get("wwpdb-api-token")
            if tok and len(tok) > 20:
                return True
        except Exception as e:
            logger.exception(e)

        return False

    def __authVerify(self, authHeader, siteId, serviceUserId):
        """Check the validity of the input API access token - check for user id consistency .

        Return: True for success or False otherwise
        """
        tD = {"errorCode": 401, "errorMessage": "Token processing error", "token": None, "errorFlag": True}

        try:
            jtu = JwtTokenReader(siteId=siteId)
            tD = jtu.parseAuth(authHeader)
            if tD["errorFlag"]:
                return tD
            tD = jtu.parseToken(tD["token"])
            logger.debug("authVerify tD %r", tD)
            #
            if (len(serviceUserId) > 0) and (serviceUserId != str(tD["sub"])):
                tD["errorMessage"] = "Token user mismatch"
                tD["errorFlag"] = True
                tD["errorCode"] = 401
            #

            return tD
        except Exception as e:
            logger.exception("Failed site %r auth header %r", siteId, authHeader)
            logger.exception(e)
            return tD

    def __call__(self, environment, responseApplication):
        """Request callable entry point"""
        #
        myRequest = Request(environment)
        logger.debug("%s", "\n ++ ".join(self.__dumpRequest(request=myRequest)))
        #
        myParameterDict = {"request_host": [""], "wwpdb_site_id": [getSiteId()], "service_user_id": [""], "remote_addr": [""]}
        #
        try:
            #
            # Injected from the web server environment
            if "WWPDB_SITE_ID" in environment:
                myParameterDict["wwpdb_site_id"] = [environment["WWPDB_SITE_ID"]]

            if "HTTP_HOST" in environment:
                myParameterDict["request_host"] = [environment["HTTP_HOST"]]

            myParameterDict["remote_addr"] = [myRequest.remote_addr]
            #
            # Injected from the incoming request payload
            #
            for name, value in myRequest.params.items():
                if name not in myParameterDict:
                    myParameterDict[name] = []
                myParameterDict[name].append(value)
            myParameterDict["request_path"] = [myRequest.path.lower()]

        except Exception as e:
            logger.exception("Exception processing %s request parameters", self.__serviceName)
            logger.exception(e)

        ###
        # At this point we have everything needed from the request !
        ###
        # logger.debug("%s" % ("\n ++ ".join(self.__dumpRequest(request=myRequest))))
        # logger.debug("Parameter dict:\n%s" % '\n'.join(["  ++  %s: %r" % (k, v) for k, v in myParameterDict.items()]))
        try:
            ok = True
            apiTokFlag = self.__isHeaderApiToken(myRequest)
            logger.debug("Request API token flag: %s", apiTokFlag)
            if self.__authVerifyFlag and apiTokFlag:
                #  Verify API token -
                authD = self.__authVerify(myRequest.headers.get("wwpdb-api-token"), myParameterDict["wwpdb_site_id"][0], myParameterDict["service_user_id"][0])
                logger.debug("Authorization error flag is %r", authD["errorFlag"])
                if authD["errorFlag"]:
                    ok = False
                else:
                    myParameterDict["jwt-sub"] = [str(authD["sub"])]
                    myParameterDict["jwt-exp"] = [authD["exp"]]
                    myParameterDict["jwt-iat"] = [authD["iat"]]
                    myParameterDict["jwt-exp-ts"] = [datetime.datetime.utcfromtimestamp(authD["exp"]).strftime("%Y-%b-%d %H:%M:%S")]
                    myParameterDict["jwt-iat-ts"] = [datetime.datetime.utcfromtimestamp(authD["iat"]).strftime("%Y-%b-%d %H:%M:%S")]
                    myParameterDict["service_user_id"] = myParameterDict["jwt-sub"]
            else:
                myParameterDict["service_user_id"] = ["CONTENTWS_ANONYMOUS"]

            #  If this is a content request then -
            if ok:
                try:
                    if "request_content_type" in myParameterDict:
                        rOk = False
                        sId = str(myParameterDict["service_user_id"][0]).upper()
                        ct = str(myParameterDict["request_content_type"][0]).lower()
                        logger.info("Checking auth for %s and %s", sId, ct)
                        if sId.startswith("SASBDBWS_") and "sasbdb" in ct:
                            rOk = True
                        elif sId.startswith("EMDBWS_") and "emdb" in ct:
                            rOk = True
                        elif sId.startswith("CONTENTWS_") or sId.startswith("WWPDBWS_"):
                            rOk = True
                    else:
                        rOk = True
                except Exception as e:
                    logger.exception("Content request auth failure")
                    logger.exception(e)
                    rOk = False

                ok = rOk

            if ok:
                #        Check for sufficent data to continue
                if len(myParameterDict["service_user_id"][0]) > 0 and len(myParameterDict["wwpdb_site_id"][0]) > 0:
                    logger.debug("Invoking web service application")
                    myApp = WebServiceApp(parameterDict=myParameterDict)
                    sR = myApp.run()
                    myResponse = sR.getResponse()
                else:
                    logger.debug("Failed to invoke web service application")
                    sR = ServiceResponse(returnFormat="json")
                    sR.setError(statusCode=400, msg="Request missing input data or access key information")
                    myResponse = sR.getResponse()
            else:
                logger.debug("Authorization failure returning error status")
                sR = ServiceResponse(returnFormat="json")
                sR.setError(statusCode=authD["errorCode"], msg=authD["errorMessage"])
                myResponse = sR.getResponse()
        except Exception as e:
            logger.exception("Service request processing exception")
            logger.exception(e)
        #
        #
        #
        logger.debug("Request processing completed for service %s\n\n", self.__serviceName)
        ###
        return myResponse(environment, responseApplication)


##
##
application = MyRequestApp(serviceName="ContentServiceApp", authVerifyFlag=USEKEY)
