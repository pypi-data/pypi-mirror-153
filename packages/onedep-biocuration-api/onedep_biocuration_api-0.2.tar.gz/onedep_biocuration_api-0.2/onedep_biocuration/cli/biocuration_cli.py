#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
biocuration_cli.py
^^^^^^^^^^^^^^^

Command line interface for wwPDB OneDep Biocuration webservice API.

:copyright: @wwPDB
:license: Apache 2.0, see LICENSE file for more details.

Updates:
    22-Sep-2016 jdw  adapt for onedep package
    24-Sep-2016 jdw  revise error handling
    28-Sep-2016 jdw  add exp_method argument
    30-Sep-2016 jdw  add additional path conditioning -
    01-Dec-2016 jdw  make api key functions for this cli controlled by env var ONEDEP_USE_API_KEY
    14-Feb-2017 jdw  adapt options for biocuration api
    31-May-2022 ep   add site request for reports

"""
from __future__ import print_function
from __future__ import unicode_literals

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"


import logging
import sys
import six
import os.path


try:
    from argparse import ArgumentParser as ArgParser
    from argparse import RawTextHelpFormatter
except ImportError:
    from optparse import OptionParser as ArgParser  # pylint: disable=deprecated-module

HERE = os.path.abspath(os.path.dirname(__file__))
#
try:
    from onedep_biocuration import __version__
except:  # noqa: E722 pylint: disable=bare-except
    sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
    from onedep_biocuration import __version__

from onedep_biocuration import __apiUrl__  # noqa: E402

from onedep_biocuration.api.ContentRequest import ContentRequest  # noqa: E402


log = logging.getLogger()


def print_(s):
    sys.stdout.write(s)


def version():
    """Print the version and exit"""
    raise SystemExit(__version__)


def readApiKey(filePath):
    apiKey = None
    try:
        fn = os.path.expanduser(filePath)
        with open(fn, "r") as fp:
            apiKey = fp.read()
    except:  # noqa: E722 pylint: disable=bare-except
        pass
    return apiKey


def writeSessionId(sessionId, filePath):
    try:
        fn = os.path.expanduser(filePath)
        with open(fn, "w") as fp:
            fp.write(sessionId)
        return True
    except:  # noqa: E722 pylint: disable=bare-except,raise-missing-from
        raise SystemExit("Error writing file %r" % filePath)


def readSessionId(filePath):
    sessionId = None
    try:
        fn = os.path.expanduser(filePath)
        log.debug("Getting session from %r", fn)
        with open(fn, "r") as fp:
            sessionId = fp.read()
    except:  # noqa: E722 pylint: disable=bare-except
        log.debug("failing for file path %r", filePath)

    return sessionId


def displayStatus(sD, exitFlag=False, exitOnError=True):

    if "onedep_error_flag" in sD and sD["onedep_error_flag"]:
        print_("OneDep error: %s\n" % sD["onedep_status_text"])
        if exitOnError:
            raise SystemExit()
    else:
        if "status" in sD:
            print_("OneDep status: %s\n" % sD["status"])
    if exitFlag:
        raise SystemExit()


def displayIndex(sD):
    #
    print_("\nOneDep Session File Index:\n")
    try:
        if "index" in sD and len(sD) > 0:
            print_("%50s\n" % ("Session File Name"))
            print_("%50s\n" % ("-----------------"))
            for ky in sD["index"]:
                _fn, fmt = sD["index"][ky]
                if fmt in ["json"]:
                    print_("%50s\n" % (ky))
        else:
            print_("No session content\n")
    except:  # noqa: E722 pylint: disable=bare-except
        print_("Error processing session index")


def filterPath(inpPath):
    try:
        return os.path.expanduser(inpPath)
    except:  # noqa: E722 pylint: disable=bare-except
        return inpPath


def run():
    """Command line interface for OneDep Biocuration API"""

    description = """
    Command line interface for OneDep biocuration API:

    Step 1:  Request a new session on the biocuration server.

        onedep_biocuration --new_session

            By default, session information will be stored in your home directory
            in file ~/.onedep_current_session

    Step 2:  Submit a request for data content in the current session

            onedep_biocuration --request_entry_content  <entry_content_type>  --request_entry_id <data_set_id>

            onedep_biocuration --request_summary_content  <summary_content_type>

    Step 4:  Check the status of the content service request

            onedep_biocuration --status

    Step 5: When the request is completed, recover the content report.


            onedep_biocuration --output_file status.json --output_content_type request-status-xxxx

    """

    #
    try:
        parser = ArgParser(description=description, formatter_class=RawTextHelpFormatter)
    except:  # noqa: E722 pylint: disable=bare-except
        parser = ArgParser(description="Command line interface for OneDep biocuration API")

    # For optparse.OptionParser add an `add_argument` method for compatibility with argparse.ArgumentParser
    try:
        parser.add_argument = parser.add_option
    except AttributeError:
        pass

    ###
    parser.add_argument(
        "--session_file",
        dest="sessionFile",
        type=six.text_type,
        default=filterPath("~/.onedep_biocuration_current_session"),
        help="File containing current session information (default: %(default)s)",
    )
    ##
    parser.add_argument("--new_session", dest="newSessionOp", action="store_true", default=False, help="Start a new session")
    ##
    parser.add_argument("--entry_id", dest="dataSetId", type=six.text_type, default=None, help="Entry identifier [D_0000000000]")

    parser.add_argument("--entry_content_type", dest="requestEntryContentType", type=six.text_type, default=None, help="Entry content type")

    parser.add_argument("--summary_content_type", dest="requestSummaryContentType", type=six.text_type, default=None, help="Summary content type")

    parser.add_argument("--query_site", dest="requestSummaryQuerySite", type=six.text_type, default=None, help="For summary content types, option site id")
    #
    # Output options -
    parser.add_argument("--output_file", dest="outputFile", type=six.text_type, default=None, help="Output file path")

    parser.add_argument("--output_format_type", dest="outputFormatType", type=six.text_type, default="json", help="Output file format type")

    parser.add_argument("--output_type", dest="outputType", type=six.text_type, default=None, help="Target content type to output")
    ##
    #   Operational and status options for the service  --
    parser.add_argument("--status", dest="statusOp", action="store_true", default=False, help="Get the status of the current session")
    #
    parser.add_argument(
        "--test_complete", dest="completeOp", action="store_true", default=False, help="Return competion status for the current session [1 for done or 0 otherwise]"
    )
    #
    parser.add_argument("--index", dest="indexOp", action="store_true", default=False, help="Request index of the data files in the current session")
    #
    parser.add_argument("--version", action="store_true", help="Show the version number and exit")
    ##
    parser.add_argument("--verbose", action="store_true", help="Set verbose logging")
    parser.add_argument("--debug", action="store_true", help="Set debug logging")
    parser.add_argument("--test_mode", dest="testMode", action="store_true", help="Set service in test mode")
    parser.add_argument("--test_duration", dest="testModeDuration", type=int, default=10, help="Mock service duration in test mode (seconds, default=10)")
    parser.add_argument("--log_file", dest="logFile", type=six.text_type, default=None, help="Local log file path")

    parser.add_argument("--api_url", dest="apiUrl", type=six.text_type, default=__apiUrl__, help="API base URL")
    #
    parser.add_argument(
        "--api_key_file",
        dest="apiKeyFile",
        type=six.text_type,
        default=filterPath("~/.onedep_biocuration_apikey.jwt"),
        help="File containing a OneDep API key (default: %(default)s)",
    )
    #
    #
    options = parser.parse_args()
    if isinstance(options, tuple):
        args = options[0]
    else:
        args = options
    del options

    # Print the version and exit
    if args.version:
        version()
    #
    # Configure logging -
    logging.captureWarnings(True)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
    logging.basicConfig(format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
    if args.logFile:
        handler = logging.FileHandler(args.logFile)
        handler.setFormatter(formatter)
        log.addHandler(handler)
    #
    if args.debug:
        log.setLevel(logging.DEBUG)
        log.debug("debug logging activated")
    elif args.verbose:
        log.setLevel(logging.INFO)
        log.debug("info logging activated")
    else:
        log.setLevel(logging.ERROR)

    #
    apiUrl = args.apiUrl
    apiKey = None
    #

    #
    # Read API key file -
    if args.apiKeyFile:
        apiKey = readApiKey(args.apiKeyFile)
        if not apiKey:
            parser.print_usage()
            raise SystemExit("\nError reading Api key file %s" % filterPath(args.apiKeyFile))

    # Create a new session or recover cached session data -
    sessionId = None
    if args.newSessionOp:
        cr = ContentRequest(apiKey=apiKey, apiUrl=apiUrl)
        rD = cr.createSession()
        displayStatus(rD)
        sessionId = rD["session_id"]
        writeSessionId(sessionId, args.sessionFile)
    else:
        sessionId = readSessionId(args.sessionFile)
        if not sessionId:
            parser.print_usage()
            raise SystemExit("\nError reading session file %s" % filterPath(args.sessionFile))

    # Submit content service request -
    if (args.requestEntryContentType and args.dataSetId) or args.requestSummaryContentType:
        pD = {}
        cr = ContentRequest(apiKey=apiKey, apiUrl=apiUrl)
        cr.setSession(sessionId)
        # optional test mode configuration
        if args.testMode:
            pD["worker_test_mode"] = True
        if args.testModeDuration:
            pD["worker_test_duration"] = args.testModeDuration
        else:
            pD["worker_test_duration"] = 10
        # option query site
        if args.requestSummaryContentType and args.requestSummaryQuerySite:
            pD["query_site"] = args.requestSummaryQuerySite
        #
        #
        rD = {}
        if args.requestEntryContentType and args.dataSetId:
            rD = cr.requestEntryContent(args.dataSetId, args.requestEntryContentType, args.outputFormatType, **pD)
        elif args.requestSummaryContentType:
            rD = cr.requestSummaryContent(args.requestSummaryContentType, args.outputFormatType, **pD)

        displayStatus(rD)

    # Output files -
    if args.outputFile and args.outputType:
        cr = ContentRequest(apiKey=apiKey, apiUrl=apiUrl)
        cr.setSession(sessionId)
        rD = cr.getOutputByType(filePath=filterPath(args.outputFile), contentType=args.outputType)
        displayStatus(rD)

    # Get index of session file content -
    if args.indexOp:
        cr = ContentRequest(apiKey=apiKey, apiUrl=apiUrl)
        cr.setSession(sessionId)
        rD = cr.getIndex()
        displayStatus(rD)
        displayIndex(rD)

    # Get session service status details -
    if args.statusOp:
        cr = ContentRequest(apiKey=apiKey, apiUrl=apiUrl)
        cr.setSession(sessionId)
        rD = cr.getStatus()
        displayStatus(rD)

    if args.completeOp:
        cr = ContentRequest(apiKey=apiKey, apiUrl=apiUrl)
        cr.setSession(sessionId)
        rD = cr.getStatus()
        #
        if "status" in rD and rD["status"] in ["completed", "failed"]:
            iRet = 1
            print_("%d" % iRet)
        else:
            iRet = 0
            print_("%d" % iRet)


if __name__ == "__main__":
    run()
