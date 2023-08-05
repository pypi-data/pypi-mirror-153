# -*- coding: utf-8 -*-
"""
ApiBase.py
^^^^^^^^^^

Core methods supporting the wwPDB OneDep webservice API.

:copyright: @wwPDB
:license: Apache 2.0, see LICENSE file for more details.


Updates:
     3-Aug-2016 jdw  add Authorization header
    20-Sep-2016 jdw  refactor for standard packaging
    21-Sep-2016 jdw  add download by name and type.
    21-Sep-2016 jdw  make parameters optional in all prototypes
    25-Sep-2016 jdw  revise exception handling
    14-Feb-2017 jdw  add download() method which bypasses content/format checks.
"""


from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"

import logging
import sys
import os
import copy
import hashlib

# import warnings

import requests
import six

try:
    import json
except ImportError:
    import simplejson as json

from onedep_biocuration import __version__
from requests.packages.urllib3.exceptions import InsecureRequestWarning  # pylint: disable=E0401

log = logging.getLogger(__name__)


class ApiBase(object):
    def __init__(self, apiKey=None, userAgent=None, apiName=None, apiUrl=None, verify=True):
        """
        Core methods supporting the OneDep web client API.

        :param string apiKey: (Optional) security token.
        :param string userAgent: (Optional) alternative identifier for calling application.
        :param string apiName: (Optional) API service name
        :param string apiUrl: (Optional) API service base URL.
        :param string verify:  (Optional) verify SSL certificate

        """
        log.debug("Service initializing")
        self.__chunkSize = 2048
        #
        self._apiUrl = apiUrl if apiUrl else "https://localhost"
        self._apiKey = apiKey if apiKey else "anonymous"
        self._apiName = apiName if apiName else "onedep"
        #
        self.__myreq = requests.session()
        self.__myreq.headers["User-Agent"] = userAgent if userAgent else "OneDepApiClient/%s Python/%s " % (__version__, sys.version.split()[0])
        self.__myreq.headers["wwpdb-api-token"] = "%s %s" % ("Bearer", self._apiKey)
        #
        self._returnApiErrorFlagKey = "onedep_error_flag"
        self._returnApiStatusTextKey = "onedep_status_text"
        #
        self._sessionId = None
        #
        self._verify = verify
        self._reservedContentTypes = {}
        if not verify:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # pylint: disable=no-member

    def createSession(self):
        """Create and maintain a session context in all subsequent API requests.

        :rtype: json service response converted to dictionary (with mininal keys: api_error_flag, api_status_text, session_id)
        """
        # create a new session context
        pD = {}
        rD = self.post("session", **pD)
        self._sessionId = rD.get("session_id", None)
        return rD

    def setSession(self, sessionId):
        """Set the identifier for the current session context."""
        self._sessionId = sessionId

    def getSession(self):
        return self._sessionId

    def __addSessionContext(self, pD, auto=False):
        """Internal method to add the current session context to the input parameter dictionary."""
        if not self._sessionId and auto:
            self.createSession()
        #
        if "session_id" not in pD:
            pD["session_id"] = self.getSession()

    def setApiReturnStatusKeys(self, errorFlagKey, statusTextKey):
        self._returnApiErrorFlagKey = errorFlagKey
        self._returnApiStatusTextKey = statusTextKey

    def setContentTypes(self, contentTypeDict):
        try:
            self._reservedContentTypes = copy.deepcopy(contentTypeDict)
            return True
        except:  # noqa: E722 pylint: disable=bare-except
            return False

    def getContentTypes(self):
        try:
            return self._reservedContentTypes.keys()
        except:  # noqa: E722 pylint: disable=bare-except
            return []

    def getContentFormatList(self, contentType):
        if contentType in self._reservedContentTypes:
            return self._reservedContentTypes[contentType]
        else:
            return []

    def getContentFormatDefault(self, contentType):
        try:
            if contentType in self._reservedContentTypes:
                return self._reservedContentTypes[contentType][0]
            else:
                return None
        except:  # noqa: E722 pylint: disable=bare-except
            return None

    def downloadByName(self, dstPath, fileName, endPoint="download", **params):
        """Construct GET request to download the target fileName to dstPath.

        :param string fileName: file name target for download
        :param string dstPath: full local path to file for download
        :param string endPoint:  API endPoint  - valws.
        :param params: (Optional) Parameters as keyword arguments.

        :rtype: json response converted to dictionary

        """
        _params = {}
        for p in params:
            _params[p] = params[p]

        _params["filename"] = fileName
        return self.__download(dstPath, endPoint, **_params)

    def downloadByType(self, dstPath, contentType, endPoint="download", **params):
        """Construct GET request to download the target data object type to dstPath.

        :param string contentType: data object content type target download
        :param string dstPath: full local path to file for download
        :param string endPoint:  API endPoint  - valws.
        :param params: (Optional) Parameters as keyword arguments.

        :rtype: json response converted to dictionary

        """
        rD = {}
        if contentType not in self._reservedContentTypes:
            rD[self._returnApiErrorFlagKey] = True
            rD[self._returnApiStatusTextKey] = "Unrecognized content type"
            return rD

        _params = {}
        for p in params:
            _params[p] = params[p]
        _params["contenttype"] = contentType
        _params["formattype"] = self.getContentFormatDefault(contentType)

        #
        return self.__download(dstPath, endPoint=endPoint, **_params)

    def download(self, dstPath, contentType, formatType, endPoint="download", **params):
        """Construct GET request to download the target data object type to dstPath.

        :param string contentType: data object content type target download
        :param string formatType: data object format type target download
        :param string dstPath: full local path to file for download
        :param string endPoint:  API endPoint  - valws.
        :param params: (Optional) Parameters as keyword arguments.

        :rtype: json response converted to dictionary

        """
        _params = {}
        for p in params:
            _params[p] = params[p]
        _params["contenttype"] = contentType
        _params["formattype"] = formatType
        #
        return self.__download(dstPath, endPoint=endPoint, **_params)

    def __download(self, dstPath, endPoint="download", **params):
        """Internal method to construct GET request to download the content/format type to dstPath.

        :param string dstPath: full path to file for download
        :param string endPoint:  API endPoint  - valws.
        :param params: Parameters as keyword arguments including file type/format specification and session details.

        :rtype: json response converted to dictionary

        """
        _params = {}
        for p in params:
            _params[p] = params[p]
        #
        self.__addSessionContext(_params)
        log.debug(" DOWNLOAD BEGINS for : %s %r", dstPath, _params)
        #
        rD = {}
        rD[self._returnApiErrorFlagKey] = True
        rD[self._returnApiStatusTextKey] = "Miscellaneous api failure"
        #
        url = self.__encodeUrl(self._apiUrl, self._apiName, endPoint, **_params)
        #
        log.debug("Request: URL: %r", url)
        #
        try:
            response = self.__myreq.get(url, data=_params, verify=self._verify, stream=True)
            if response.status_code == 200:
                with open(dstPath, "wb") as f:
                    for chunk in response.iter_content(self.__chunkSize):
                        f.write(chunk)
            rD[self._returnApiErrorFlagKey] = False
            rD[self._returnApiStatusTextKey] = "ok"
            log.debug("download request headers %r", response.request.headers)
            log.debug("download response headers %r", response.headers)
        except Exception as e:
            return self.__filterExceptions(e, msgDefault="Download request processing exception")

        errFlag, errD = self.__filterErrors(response)
        if errFlag:
            return errD

        try:
            myDigest = self.getMD5(dstPath)
            theDigest = response.headers["checksum_md5"]
            if myDigest != theDigest:
                rD[self._returnApiErrorFlagKey] = True
                rD[self._returnApiStatusTextKey] = "Checksum failure"
            else:
                log.debug("checksum comparison success")
        except:  # noqa: E722 pylint: disable=bare-except
            rD[self._returnApiErrorFlagKey] = True
            rD[self._returnApiStatusTextKey] = "Download checksum processing error %r " % dstPath
            # log.exception("Local file processing error %r" % dstPath)

        return rD

    def upload(self, filePath, contentType, fileFormat, endPoint="upload", **params):
        """Construct POST request to perform multipart/ file upload and return the JSON response.

        :param string filepath: full path to file for upload
        :param string contentType: type ['model', 'structure-factors', 'nmr-chemical-shifts', 'nmr-restraints', 'em-volume']
        :param string fileFormat:  (pdbx)
        :param string endPoint:  API endPoint  - valws.
        :param params: (Optional) Parameters as keyword arguments.

        :rtype: json response converted to dictionary


        >>> url = 'http://httpbin.org/post'
        >>> files = {'file': ('report.xls', open('report.xls', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}
        >>> r = requests.post(url, files=files)

        """
        log.debug("upload request: %s %s %s", filePath, contentType, fileFormat)
        rD = {}
        rD[self._returnApiErrorFlagKey] = True
        rD[self._returnApiStatusTextKey] = "Miscellaneous api failure"
        #
        if contentType not in self._reservedContentTypes:
            rD[self._returnApiErrorFlagKey] = True
            rD[self._returnApiStatusTextKey] = "Unrecognized file type"
            return rD
        if fileFormat not in self._reservedContentTypes[contentType]:
            rD[self._returnApiErrorFlagKey] = True
            rD[self._returnApiStatusTextKey] = "Unrecognized file format"
            return rD
        #
        log.debug(" A params %r", params)
        _params = {}
        for p in params:
            _params[p] = params[p]
        log.debug(" B _params %r", _params)
        self.__addSessionContext(_params)
        log.debug(" C _params %r", _params)
        #
        try:
            md5 = self.getMD5(filePath)
            _params["checksum_md5"] = md5
            _, fn = os.path.split(filePath)
            fobj = open(filePath, "rb")
            fD = {"file": (fn, fobj)}
            _params["content_type"] = contentType
            _params["file_format"] = fileFormat
        except:  # noqa: E722 pylint: disable=bare-except
            rD[self._returnApiErrorFlagKey] = True
            rD[self._returnApiStatusTextKey] = "Input file access or processing error "
            # log.exception("Local file processing error ")
            return rD
        #
        url = "%s/service/%s/%s" % (self._apiUrl, self._apiName, endPoint)
        #
        log.debug("Request: URL: %s PARAMS: %r", url, _params)
        #
        try:
            response = self.__myreq.post(url, files=fD, data=_params, verify=self._verify)
            log.debug("post headers %r", response.request.headers)
        except Exception as e:
            return self.__filterExceptions(e, msgDefault="Upload request processing exception")

        #
        errFlag, errD = self.__filterErrors(response)
        if errFlag:
            return errD

        try:
            rD.update(json.loads(response.text))
            rD[self._returnApiErrorFlagKey] = rD["errorflag"]
            rD[self._returnApiStatusTextKey] = rD["statusmessage"]
        except Exception as e:
            rD[self._returnApiErrorFlagKey] = True
            rD[self._returnApiStatusTextKey] = "Upload response processing error %s" % str(e)
            # log.exception("Local upload response processing error ")

        return rD

    def __filterExceptions(self, exception, msgDefault="OneDep API service failure"):
        """Handle typical exceptions and map these to response dictionary -

        :param exception: target exception object

        :rtype dictionary:  response dictionary (with mininal keys: api_error_flag, api_status_text)

        """
        errorFlag = True
        msg = msgDefault
        try:
            msg = str(exception)
        except:  # noqa: E722 pylint: disable=bare-except
            pass
        #
        rD = {}
        rD[self._returnApiErrorFlagKey] = errorFlag
        rD[self._returnApiStatusTextKey] = msg
        return rD

    def __filterErrors(self, response, msgDefault="OneDep API service failure"):
        """Check the response packet for typical error various error types and map these to
        response dictionary -

        :param rsp request response object: target response object

        :rtype tuple:  errorFlag, response dictionary (with mininal keys: api_error_flag, api_status_text)

        """
        errorFlag = False
        msg = "unprocessed"
        try:
            if response.status_code in [401, 404, 500]:
                errorFlag = True
                msg = msgDefault
                try:
                    errD = json.loads(response.text)
                    msg = errD["statustext"]
                except:  # noqa: E722 pylint: disable=bare-except
                    pass
        except:  # noqa: E722 pylint: disable=bare-except
            pass
        #
        rD = {}
        rD[self._returnApiErrorFlagKey] = errorFlag
        rD[self._returnApiStatusTextKey] = msg

        return errorFlag, rD

    def post(self, endPoint, **params):
        """Construct POST request and return the JSON response.

        :param string endPoint:  API endPoint  - valws.
        :param params: (Optional) Parameters as keyword arguments.

        :rtype: json response converted to dictionary
        """
        rD = {}
        rD[self._returnApiErrorFlagKey] = True
        rD[self._returnApiStatusTextKey] = "Miscellaneous api failure"
        url = "%s/service/%s/%s" % (self._apiUrl, self._apiName, endPoint)
        #
        _params = {}
        for p in params:
            _params[p] = params[p]
        self.__addSessionContext(_params)
        #
        log.debug("Request: %s %s", url, _params)
        try:
            response = self.__myreq.post(url, data=_params, verify=self._verify)
            log.debug("post headers %r", response.request.headers)
        except Exception as e:
            return self.__filterExceptions(e, msgDefault="POST request processing exception")

        errFlag, errD = self.__filterErrors(response)
        if errFlag:
            return errD

        try:
            rD.update(json.loads(response.text))
            rD[self._returnApiErrorFlagKey] = rD["errorflag"]
            rD[self._returnApiStatusTextKey] = rD["statusmessage"]
        except Exception as e:
            rD[self._returnApiErrorFlagKey] = True
            rD[self._returnApiStatusTextKey] = "POST request processing error %r " % str(e)

        return rD

    def get(self, endPoint, **params):
        """Construct GET request and return the JSON response.

        :param string endPoint:  API endPoint  - valws.
        :param params: (Optional) Parameters as keyword arguments.

        :rtype: json response converted to dictionary
        """
        rD = {}
        rD[self._returnApiErrorFlagKey] = True
        rD[self._returnApiStatusTextKey] = "Miscellaneous api failure"
        _params = {}
        for p in params:
            _params[p] = params[p]
        self.__addSessionContext(_params)
        #
        url = self.__encodeUrl(self._apiUrl, self._apiName, endPoint, **_params)
        try:
            response = self.__myreq.get(url, verify=self._verify)
            log.debug("get headers %r", response.request.headers)
        except Exception as e:
            return self.__filterExceptions(e, msgDefault="GET request processing exception")

        errFlag, errD = self.__filterErrors(response)
        if errFlag:
            return errD
        #
        try:
            rD.update(json.loads(response.text))
            rD[self._returnApiErrorFlagKey] = rD["errorflag"]
            rD[self._returnApiStatusTextKey] = rD["statusmessage"]
        except Exception as e:
            rD[self._returnApiErrorFlagKey] = True
            rD[self._returnApiStatusTextKey] = "Request processing error %r" % str(e)

        return rD

    def getMD5(self, path, block_size=4096, hr=True):
        """
        Chunked MD5 function -

        Block size directly depends on the block size of your filesystem
        to avoid performances issues

        Linux Ext4 block size
            sudo /sbin/blockdev --getbsz /dev/sda1
            > Block size:               4096

        """
        md5 = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(block_size), b""):
                md5.update(chunk)
        if hr:
            return md5.hexdigest()
        return md5.digest()

    def __encodeUrl(self, apiUrl, api, endPoint, **params):
        """Internal method to construct API url for a GET request.

        :param string api: the api service name -
        :param string endPoint:  API endPoint  - valws.
        :param params: (Optional) Parameters as keyword arguments.

        :rtype: string
        """
        qs = []
        for k, v in params.items():
            qs.append("%s=%s" % (k, six.moves.urllib.parse.quote_plus(str(v))))
        #
        return "%s/service/%s/%s?%s" % (apiUrl, api, endPoint, "&".join(qs))


class ApiException(Exception):
    """Service general exception."""

    pass  # pylint: disable=unnecessary-pass


class ApiAuthException(Exception):
    """Service authentication exception."""

    pass  # pylint: disable=unnecessary-pass
