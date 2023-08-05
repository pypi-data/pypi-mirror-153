##
# File:  ContentRequestReportDb.py
# Date:  15-Feb-2017  J. Westbrook
#
# Update:
#
##
"""
Fetch content and prepare report from PDBx content -

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.07"

import datetime
import logging
import sys
import time

#
#  -- supporting queries against only DA_INTERNAL in this service --
from wwpdb.utils.db.DaInternalSchemaDef import DaInternalSchemaDef
from wwpdb.utils.db.MyConnectionBase import MyConnectionBase
from wwpdb.utils.db.MyDbSqlGen import MyDbQuerySqlGen, MyDbConditionSqlGen
from wwpdb.utils.db.MyDbUtil import MyDbQuery
from wwpdb.utils.db.WorkflowSchemaDef import WorkflowSchemaDef

from wwpdb.apps.content_ws_server.content.ContentRequestReportIo import ContentRequestReportIo

#
logger = logging.getLogger()


class ContentRequestReportDb(MyConnectionBase):
    """
    Fetch content and prepare report from PDBx content -

    """

    def __init__(self, siteId, verbose=True, log=sys.stderr):
        super(ContentRequestReportDb, self).__init__(siteId=siteId, verbose=verbose, log=log)
        self.__verbose = verbose
        logger.info("Starting with siteId %r", siteId)
        self.__lfh = log
        #
        self.__crio = ContentRequestReportIo()

    def getContentTypeDef(self, contentType):
        return self.__crio.getContentDefinition(contentType)

    def getContentTypes(self):
        return self.__crio.getContentTypes()

    def extractContent(self, requestContentType):
        """Apply the input 'requestContentType' to the current database state -


        Example -
            {'req-emdb-summary-status-report': {'content': {'tablename': ['colname1','colname2','colname3'], },
                                               'type': 'rdbms',
                                               'resource': {'tablename': ('da_internal', 'da_internal_combine')},
                                               'conditions': {'tablename': {'colname': ('val', 'char', 'like')}
                                                          },
                                                }
             }
        """
        rD = {}
        try:
            cDef = self.getContentTypeDef(requestContentType)
            logger.debug("Content definition %r", cDef.items())
            logger.debug("Content keys definition %r", cDef["content"].keys())
            logger.debug("Content resource %r", cDef["resource"])
            #
            #  -- Note the str() filter here --
            myCategoryList = [str(c) for c in cDef["content"].keys()]
            myConditionList = [str(c) for c in cDef["conditions"].keys()]

            #
            if len(cDef) < 1:
                logger.error("Undefined/empty content definition")
                return rD

            #
            logger.debug("Category list in definition %r", myCategoryList)
            #
            for catName in myCategoryList:
                rD[catName] = []
                sList = cDef["content"][catName]
                myResource, myDatabase = cDef["resource"][catName]
                logger.debug("Resource %r database %r", myResource, myDatabase)
                if myResource.upper() in ["DA_INTERNAL", "STATUS"]:
                    if myDatabase in ["da_internal", "da_internal_prod", "da_internal_combine"]:
                        sDef = DaInternalSchemaDef(verbose=self.__verbose, log=sys.stderr, databaseName=myDatabase)
                    elif myDatabase in ["status"]:
                        sDef = WorkflowSchemaDef(verbose=self.__verbose, log=sys.stderr)
                    else:
                        sDef = {}
                else:
                    logger.error("Undefined resource %r database %r", myResource, myDatabase)
                    continue

                # tableIdList = sd.getTableIdList()
                # aIdList = sd.getAttributeIdList(tableId)
                sqlGen = MyDbQuerySqlGen(schemaDefObj=sDef, verbose=self.__verbose, log=sys.stderr)
                sTableIdList = []

                sTableIdList.append(catName.upper())
                for s in sList:
                    sqlGen.addSelectAttributeId(attributeTuple=(catName.upper(), s.upper()))

                if catName in myConditionList:
                    # {'entity_poly': {'entity_id': ('1', 'char', 'eq')},
                    sqlCondition = MyDbConditionSqlGen(schemaDefObj=sDef, verbose=self.__verbose, log=sys.stderr)
                    cndD = cDef["conditions"][catName]
                    cList = []
                    for k, v in cndD.items():
                        cList.append(((catName.upper(), k.upper()), v[2].upper(), (v[0].upper(), v[1].upper())))
                    for cTup in cList:
                        sqlCondition.addValueCondition(cTup[0], cTup[1], cTup[2])

                    sqlCondition.addTables(sTableIdList)
                    sqlGen.setCondition(sqlCondition)
                    #
                sqlS = sqlGen.getSql()
                logger.debug("SQL string\n %s\n\n", sqlS)
                sqlGen.clear()
                #
                rL = self.__processQuery(myResource, sList, sqlS)
                rD[catName] = rL
        except Exception as e:
            logger.exception("Database extraction failing for content type %r", requestContentType)
            logger.exception(e)
        #
        return rD

    def __processQuery(self, resourceName, sList, sqlS):
        """Process query  -"""
        startTime = time.time()
        #
        # config the db auth info
        self.setResource(resourceName=resourceName.upper())

        rL = []
        #
        try:
            self.openConnection()
            myQ = MyDbQuery(dbcon=self._dbCon, verbose=self.__verbose, log=self.__lfh)
            rowList = myQ.selectRows(queryString=sqlS)
            #
            if self.__verbose:
                logger.debug("Result length %d", len(rowList))
                # logger.debug("Row list %r" % rowList)
                #
            for row in rowList:
                d = {}
                for ii, s in enumerate(sList):
                    tt = row[ii]
                    try:
                        if isinstance(tt, datetime.datetime) or isinstance(tt, datetime.date):
                            tt = tt.isoformat()
                    except Exception as e:
                        logger.exception("Failing %r", tt)
                        logger.exception(e)
                    d[s] = tt
                rL.append(d)
            #
            self.closeConnection()
        except Exception as e:
            logger.exception("Failing for resource %r and query %r", resourceName, sqlS)
            logger.exception(e)

        endTime = time.time()
        logger.debug("Completed in (%.2f seconds)", endTime - startTime)
        return rL

    #
    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
            serial = obj.isoformat()
            return serial
        raise TypeError("Type not serializable")
