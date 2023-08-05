##
# File:  ContentRequestReportIo.py
# Date:  14-Feb-2017  J. Westbrook
#
# Update:
#
##
"""
     Manage fetching and storing  content type definitions.

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.07"

import datetime
import logging

from wwpdb.apps.content_ws_server.content_definitions.ContentDefintions import get_content_definition_file_path

try:
    import json
except ImportError:
    import simplejson as json
#
from oslo_concurrency import lockutils
from wwpdb.utils.config.ConfigInfo import ConfigInfo, getSiteId

#
logger = logging.getLogger()


class ContentRequestReportIo(object):
    """
    Manage fetching and storing content type definitions.

    """

    def __init__(self):
        self.__siteId = getSiteId(defaultSiteId=None)
        self.__cI = ConfigInfo(self.__siteId)
        logger.info("Starting with siteId %r", self.__siteId)
        self.__D = None
        #
        self.__lockDirPath = self.__cI.get("SITE_SERVICE_REGISTRATION_LOCKDIR_PATH", ".")
        lockutils.set_defaults(self.__lockDirPath)

    def __setup(self):
        if self.__D is None:
            self.__D = self.__readContentDefinitionDictionary()

    def getContentDefinition(self, contentType):
        self.__setup()
        if contentType and contentType in self.__D:
            return self.__D[contentType]
        else:
            return {}

    def getContentTypes(self):
        """Return a list of defined content types -"""
        self.__setup()
        if self.__D is not None:
            return self.__D.keys()
        else:
            return []

    def __get_content_definition_file(self):
        """
        helper method for getting path to content definition file
        :return:
        """
        # return self.__cI.get('SITE_WS_CONTENT_TYPE_DEFINITION_FILE_PATH')
        return get_content_definition_file_path()

    def __readContentDefinitionDictionary(self):
        """Read the dictionary containing web service content type definitions.

        Returns: d[<content_type>] = {categoryName: [at1,at2,...], ...}  or a empty dictionary.
        """
        fp = self.__get_content_definition_file()
        try:
            with open(fp, "r") as infile:
                return json.load(infile)
        except Exception as e:
            logger.info("Failed reading json resource file %s", fp)
            logger.exception(e)

        return {}

    @lockutils.synchronized("wscontenttypedef.exceptionfile-lock", external=True)
    def writeContentDefinitionDictionary(self, contentDefD, backup=True):
        """Write the dictionary containing web service content type definitions.

        Returns: True for success or False otherwise
        """
        fp = self.__get_content_definition_file()

        try:
            if backup:
                bp = fp + datetime.datetime.now().strftime("-%Y-%m-%d-%H-%M-%S")
                d = self.__readContentDefinitionDictionary()
                with open(bp, "w") as outfile:
                    json.dump(d, outfile, indent=4)
            #
            with open(fp, "w") as outfile:
                json.dump(contentDefD, outfile, indent=4)
            return True
        except Exception as e:
            logger.exception("Failed writing json resource file %s -- %s", fp, str(e))

        return False
