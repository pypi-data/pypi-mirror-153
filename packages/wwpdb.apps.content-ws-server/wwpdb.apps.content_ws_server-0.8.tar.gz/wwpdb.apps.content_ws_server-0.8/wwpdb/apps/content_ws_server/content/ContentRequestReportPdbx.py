##
# File:  ContentRequestReportPdbx.py
# Date:  14-Feb-2017  J. Westbrook
#
# Update:
#     16-Feb-2017  jdw add limited condition filters -
##
"""
Fetch content and prepare report from PDBx content -

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.07"

import logging
import sys
import time
from mmcif.io.IoAdapterCore import IoAdapterCore

from wwpdb.apps.content_ws_server.content.ContentRequestReportIo import ContentRequestReportIo

#
logger = logging.getLogger()


class ContentRequestReportPdbx(object):
    """
    Fetch content and prepare report from PDBx content -

    """

    def __init__(self, verbose=True):
        self.__verbose = verbose
        #
        self.__crio = ContentRequestReportIo()
        logger.info("Starting ContentRequestReportPdbx")

    def getContentTypeDef(self, contentType):
        return self.__crio.getContentDefinition(contentType)

    def getContentTypes(self):
        return self.__crio.getContentTypes()

    def readFilePdbx(self, filePath, logFilePath, catNameList=None):
        """Read selected categories from PDBx file"""
        startTime = time.time()
        containerList = []
        try:
            io = IoAdapterCore(verbose=self.__verbose, log=sys.stderr)
            if catNameList and len(catNameList) > 0:
                containerList = io.readFile(str(filePath), selectList=catNameList, logFilePath=str(logFilePath))
            else:
                containerList = io.readFile(str(filePath), logFilePath=str(logFilePath))
            #
            logger.info("Read %d data blocks from %r", len(containerList), filePath)

        except Exception as e:
            logger.exception("Read failing for %r", filePath)
            logger.exception(e)

        endTime = time.time()
        logger.info("Completed in (%.2f seconds)", endTime - startTime)
        return containerList

    def __cmpfunc(self, v, target, myType, myOp):
        """Internal function to compare simple types -"""
        if myType in ["string", "char"]:
            vv = str(v)
        elif myType == "int":
            vv = int(str(v))
        elif myType in ["float", "double"]:
            vv = float(str(v))
        else:
            vv = str(v)
        #
        if type in ["string", "char", "float", "double", "int"]:
            if myOp in ["eq"]:
                return vv == target
            elif myOp in ["gt"]:
                return vv > target
            elif myOp in ["ge"]:
                return vv >= target
            elif myOp in ["lt"]:
                return vv < target
            elif myOp in ["le"]:
                return vv <= target
            else:
                return False
        #
        return False

    def extractContent(self, pdbxFilePath, logFilePath, requestContentType):
        """Apply the input 'requestContentType' to the content of the input PDBx data file -"""
        rD = {}
        try:
            cDef = self.getContentTypeDef(requestContentType)
            logger.info("Content definition %r", cDef.items())
            logger.info("Content keys definition %r", cDef["content"].keys())
            # Note the str() filter here -
            myCategoryList = [str(c) for c in cDef["content"].keys()]
            myConditionList = [str(c) for c in cDef["conditions"].keys()]
            #
            if len(cDef) < 1:
                return rD
            logger.info("Category list in definition %r", myCategoryList)
            myContainerList = self.readFilePdbx(pdbxFilePath, logFilePath, myCategoryList)
            for container in myContainerList:
                catNameList = container.getObjNameList()
                for catName in myCategoryList:
                    if catName in catNameList:
                        rD[catName] = []
                        catSel = cDef["content"][catName]
                        if catName in myConditionList:
                            cndD = cDef["conditions"][catName]
                        else:
                            cndD = {}
                        cObj = container.getObj(catName)
                        for ii in range(0, cObj.getRowCount()):
                            od = {}
                            dd = cObj.getRowAttributeDict(ii)
                            for k, v in dd.items():
                                # Check for a condition -
                                if k in cndD:
                                    fD = cndD[k]
                                    ok = self.__cmpfunc(v, fD[0], fD[1], fD[2])
                                    if not ok:
                                        continue
                                #
                                if k in catSel:
                                    od[k] = v
                            rD[catName].append(od)
        except Exception as e:
            logger.exception("Extraction processing failing for %r content type %r", pdbxFilePath, requestContentType)
            logger.exception(e)
        #
        return rD
