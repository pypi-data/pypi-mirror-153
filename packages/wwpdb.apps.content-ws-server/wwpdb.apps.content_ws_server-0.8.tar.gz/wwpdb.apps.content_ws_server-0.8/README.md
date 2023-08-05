# py-wwpdb_apps_content_ws_server
OneDep Content Service

This package provides API end points for 
access to data stored in the OneDep database
and content with the mmCIF model files.

## Components

This package comprises a server front end and a consumer backend

## Installation

### Requirements

Communication between the front end and back end is via a RabbitMQ server
set by the variable SITE_RBMQ_SERVER_HOST in site-config

The front end and back end must share the same filesystem
They require SITE_WEB_APPS_TOP_SESSIONS_PATH to be set in OneDep site-config
The consumer requires access to the OneDep database and archive folder.

### server

pip install wwpdb.apps.content-ws-server[server]

### consumer

pip install wwpdb.apps.content-ws-server


## Running

### Server

WSGI scripts are provided for both use with an apache or Gunicorn

####Apache

WSGIScriptAlias /service/contentws wwpdb/apps/content_ws_server/webapp/doServiceRequest.wsgi

or

WSGIScriptAlias /service/contentws ${SITE_WEB_APPS_TOP_PATH}/wsgi/doServiceRequest_content.wsgi

####Gunicorn 

To run localhost with port 10005

pip install gunicorn
gunicorn wwpdb.apps.content_ws_server.webapp.wsgi --bind 0.0.0.0:10005

### Consumer

The following command runs a single consumer as a detached process

python -m wwpdb.apps.content_ws_server.service.ContentRequestServiceHandler --start

or for more options

python -m wwpdb.apps.content_ws_server.service.ContentRequestServiceHandler --help

## Configuring new API calls

Definitions are stored in a JSON file in wwpdb.apps.content_ws_server.content_definitions. 
The JSON is made by running a unit test 

python -m wwpdb.apps.tests-contentws.ContentRequestReportIoTests

This outputs a JSON file in the current working directory which can be copied to 
wwpdb.apps.content_ws_server.content_definitions and checked in.

## Registering for access to the API

Access to the API is controlled by a JWT key.
To generate a new key

python -m wwpdb.apps.content_ws_server.register.Register

This will output a key which is needed to access the service

to find more options

python -m wwpdb.apps.content_ws_server.register.Register --help

## Accessing the API

Access to the API is through the onedep-biocuration-api

pip install onedep-biocuration-api

Example usage

    #!/bin/bash
    #
    # File:  request-entry-report.sh
    # Date:  14-Feb-2017  Jdw
    #
    #
    TS=`/bin/date "+%Y%m%d%H%M%S"`_$$
    export ONEDEP_BIOCURATION_API_KEY_PATH="onedep_biocuration_apikey.jwt"
    CONTENT_TYPE="report-entry-example-sasbdb"
    #CONTENT_TYPE="report-summary-example-test"
    CONTENT_TYPE="report-entry-wwpdb-status"
    ONEDEP_BIOCURATION_TEST_ENTRY_ID="D_800002"
    X_ARGS=" --session_file ./.onedep_biocuration_session_${TS} --api_key_file  ${ONEDEP_BIOCURATION_API_KEY_PATH} "
    #X_ARGS=" --api_key_file  ${ONEDEP_BIOCURATION_API_KEY_PATH} "
    #
    #export ONEDEP_BIOCURATION_API_URL='http://localhost:10005/service/contentws/'
    export ONEDEP_BIOCURATION_API_URL='http://pdbe-onedep-staging:12000/service/contentws/'
    #
    # New session  -
    
    echo $X_ARGS
    #
    onedep_request --new_session ${X_ARGS}
    #
    # Submit request to run service
    #
    #onedep_request --entry_id ${ONEDEP_BIOCURATION_TEST_ENTRY_ID} --summary_content_type ${CONTENT_TYPE}  ${X_ARGS}#
    onedep_request --summary_content_type ${CONTENT_TYPE}  ${X_ARGS}
    #
    # Poll for completion status
    #
    STEP=0
    SLEEP=1
    while :
    do
       STEP=$((STEP + 1))
       PAUSE=$((STEP * STEP * SLEEP))
       echo "[${STEP}] Pausing for ${PAUSE} seconds.   Press CTRL+C to stop..."
       sleep ${PAUSE}
       ST=$(onedep_request --test_complete ${X_ARGS})
       #
       if [ "${ST}" == "1" ]
       then
            break #Abandon the loop.
       fi
    done
    #
    #  Optionally, check the completion status
    onedep_request --status ${X_ARGS}
    #
    #  Optionally, get an index of output report files
    onedep_request --index  ${X_ARGS}
    #
    #  Download report (by file type)
    onedep_request --output_file ${ONEDEP_BIOCURATION_TEST_ENTRY_ID}-${CONTENT_TYPE}-${TS}.json  --output_type ${CONTENT_TYPE} ${X_ARGS}
    #
    #

or as a python file

    # -*- coding: utf-8 -*-
    """
    request-entry-report.py <entry_id> <request_content_type> <output_file>
    
    request-entry-report.py D_800002 report-entry-example-sasbdb D_800002_report-entry-example-sasbdb.json
    
    ^^^^^^^^^^
    
    Example of wwPDB OneDep Biocuration API entry content service -
    
    :copyright: @wwPDB
    :license: Apache 2.0
    """
    from __future__ import absolute_import
    
    import argparse
    import logging
    import os
    import sys
    import time
    
    logger = logging.getLogger()
    
    HERE = os.path.abspath(os.path.dirname(__file__))
    
    try:
        from onedep_biocuration import __apiUrl__
    except:
        sys.path.insert(0, os.path.dirname(HERE))
        from onedep_biocuration import __apiUrl__
    
    from onedep_biocuration.api.ContentRequest import ContentRequest
    
    
    def readApiKey(filePath):
        apiKey = None
        try:
            fn = os.path.expanduser(filePath)
            with open(fn, 'r') as fp:
                apiKey = fp.read()
        except:
            pass
        return apiKey
    
    
    def displayStatus(sD, exitOnError=True):
        if 'onedep_error_flag' in sD and sD['onedep_error_flag']:
            logging.info("OneDep error: %s" % sD['onedep_status_text'])
            if exitOnError:
                raise SystemExit()
        else:
            if 'status' in sD:
                logging.info("OneDep status: %s" % sD['status'])
    
    
    def displayIndex(sD):
        #
        logging.info("Session File Index:")
        try:
            if 'index' in sD and len(sD) > 0:
                logging.info("%50s " % (" File name  "))
                logging.info("%50s " % ("------------"))
                for ky in sD['index']:
                    fn, fmt = sD['index'][ky]
                    if fmt in ['json']:
                        logging.info("%50s " % (fn))
            else:
                logging.info("No index content")
        except:
            logging.info("Error processing session index")
    
    
    def requestEntryContent(requestEntryId, requestContentType, requestFormatType, resultFilePath,
                            keyFilePath, apiUrl):
        """ Example of OneDep API content request.
    
            :param string requestEntryId :   the entry deposition data set identifier (D_0000000000)
            :param string requestContentType : the request content type
            :param string requestFormatType :  the request format type
            :param string resultFilePaht :  result file path for the requested content
    
        """
        #
        logging.info("Example content request service for:  +entry   %s +content type %s" % (
            requestEntryId, requestContentType))
        #
        # Flag for mock service for testing -
        mockService = True if os.getenv("ONEDEP_API_MOCK_SERVICE") == "Y" else False
        #
        # Check for alternative URL and KEY settings in the environment -
        #
        apiKey = readApiKey(keyFilePath)
        cr = ContentRequest(apiKey=apiKey, apiUrl=apiUrl)
    
        #
        # Create a new service session -
        #
        logging.info("Creating new session for content request example")
        rD = cr.newSession()
        displayStatus(rD)
        #
        #
        logging.info("Request entry identifier %s content type %s" % (requestEntryId, requestContentType))
        #
        # Submit service request
        if mockService:
            pD = {}
            pD['worker_test_mode'] = True
            pD['worker_test_duration'] = int(os.getenv("ONEDEP_API_MOCK_DURATION"))
            logging.info("Using mock service setup %r" % pD)
            rD = cr.requestEntryContent(requestEntryId, requestContentType, requestFormatType, **pD)
        else:
            logging.info("Submitted content service request")
            rD = cr.requestEntryContent(requestEntryId, requestContentType, requestFormatType)
        displayStatus(rD)
        #
        #   Poll for service completion -
        #
        it = 0
        sl = 2
        while (True):
            #    Pause -
            it += 1
            pause = it * it * sl
            time.sleep(pause)
            rD = cr.getStatus()
            if rD['status'] in ['completed', 'failed']:
                break
            logging.info("[%4d] Pausing for %4d (seconds)" % (it, pause))
            #
        #
        logging.info("Storing content type %s  in result file %s" % (requestContentType, resultFilePath))
        rD = cr.getOutputByType(resultFilePath, requestContentType, formatType=requestFormatType)
        displayStatus(rD)
        #
        iD = cr.getIndex()
        displayIndex(iD)
        #
        logging.info("Completed")
    
    
    def example():
        requestEntryContent(requestEntryId=None,
                            requestContentType="report-entry-wwpdb-status",
                            requestFormatType='json',
                            resultFilePath="summary.json",
                            keyFilePath="onedep_biocuration_apikey_staging.jwt",
                            apiUrl="http://pdbe-onedep-staging:12000/service/contentws/")
    
    def main():
        parser = argparse.ArgumentParser()
        parser.add_argument('-d', '--debug', help='debugging', action='store_const', dest='loglevel', const=logging.DEBUG,
                            default=logging.INFO)
        parser.add_argument('--requestEntryId', help='entry id', type=str)
        parser.add_argument('--requestContentType', help='content type', type=str, required=True)
        parser.add_argument('--resultFileName', help='output filename', type=str, required=True)
        parser.add_argument('--apiUrl', help='api url', type=str, default=__apiUrl__)
        parser.add_argument('--key_path', help='key_path', type=str, required=True)
    
        args = parser.parse_args()
        logger.setLevel(args.loglevel)
    
        requestEntryContent(requestEntryId=args.requestEntryId,
                            requestContentType=args.requestContentType,
                            requestFormatType='json',
                            resultFilePath=args.resultFileName,
                            keyFilePath=args.key_path,
                            apiUrl=args.apiUrl)
    
    
    if __name__ == '__main__':
        main()
        #example()


with the following command to call this file (request-entry-report.py)

   request-entry-report.py --requestContentType report-summary-wwpdb-status --resultFileName test.json --apiUrl http://localhost:10005 --key_path onedep_biocuration_apikey.jwt --requestEntryId D_00001
