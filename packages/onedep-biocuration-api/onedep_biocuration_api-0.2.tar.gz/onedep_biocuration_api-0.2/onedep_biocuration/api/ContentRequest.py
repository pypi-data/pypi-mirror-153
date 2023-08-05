# -*- coding: utf-8 -*-
"""
ContentRequest.py
^^^^^^^^^^

API for OneDep Biocuration Content Request Web Service

:copyright: @wwPDB
:license: Apache 2.0, see LICENSE file for more details.


Updates:
     10-Feb-2017 jdw  Initial version

"""
# from __future__ import print_function
from __future__ import unicode_literals

# from __future__ import division
#
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"


import logging
import sys

from onedep_biocuration import __version__
from onedep_biocuration import __apiUrl__

#
from onedep_biocuration.utils.ApiBase import ApiBase

log = logging.getLogger(__name__)


class ContentRequest(ApiBase):
    def __init__(self, apiKey=None, apiUrl=None, errorFlagKey="onedep_error_flag", statusTextKey="onedep_status_text"):
        """
        OneDep Biocuration content request webservice client API

        :param string apiKey: (Optional) security token.
        :param string apiUrl: (Optional) alternative API server URL.
        :param string errorFlagKey: (Optional) key for error flag in service return dictionary
        :param string statusTextKey: (Optional) key for status text in service return dictionary

        """
        apiUrl = apiUrl if apiUrl else __apiUrl__
        apiKey = apiKey if apiKey else "anonymous"
        userAgent = "OneDepBiocurationClient/%s Python/%s " % (__version__, sys.version.split()[0])
        apiName = "contentws"
        #
        super(ContentRequest, self).__init__(apiKey=apiKey, userAgent=userAgent, apiName=apiName, apiUrl=apiUrl, verify=False)
        #
        #
        requestContentTypes = {}
        self.setContentTypes(requestContentTypes)
        #
        self.setApiReturnStatusKeys(errorFlagKey=errorFlagKey, statusTextKey=statusTextKey)

    def newSession(self):
        """Create a new OneDep service session.

        :rtype: json service response converted to dictionary (with mininal keys: api_error_flag, api_status_text, and session_id)

        """
        return self.createSession()

    def getStatus(self):
        """Return the service status for the current session.

        :rtype: json service response converted to dictionary (with mininal keys: status, api_error_flag, api_status_text)
        """
        return self.post(endPoint="session_status")

    def getOutputByType(self, filePath, contentType, formatType="json"):
        """Store the output file containing 'contentType'/'formatType' from the current session context in the specified output file path.

        :param string filePath: full path to the output file
        :param string contentType: target contentType
        :param string contentType: target formatType (if other than json)

         :rtype: json service response converted to dictionary (with mininal keys: api_error_flag, api_status_text)
        """
        return self.download(dstPath=filePath, contentType=contentType, formatType=formatType)

    def getIndex(self):
        """Return a catalog of the data content of the current session.

        :rtype: json service response converted to dictionary (catalog plus keys - api_error_flag, api_status_text, index)
        """
        return self.post(endPoint="session_index")

    def __run(self, endPoint, **params):
        """Submit request to the input endPoint using the current session data context.

        :rtype: json service response converted to dictionary (with mininal keys: api_error_flag, api_status_text)
        """
        return self.post(endPoint=endPoint, **params)

    def requestEntryContent(self, entryId, contentType, formatType, **params):
        """For the target 'entryId' request a report corresponding to the input 'contentType'.

        :param string requestEntryId: the data set identifier target for the request
        :param string contentType: the content type target for the request
        :param string formatType:  the format type for content type target for the request

         :rtype: json service response converted to dictionary (with mininal keys: api_error_flag, api_status_text)
        """
        _params = {"request_content_type": contentType, "request_dataset_id": entryId, "request_format_type": formatType}
        for p in params:
            _params[p] = params[p]
        #
        return self.__run(endPoint="entry_content", **_params)

    def requestSummaryContent(self, contentType, formatType, **params):
        """Request a summary report corresponding to the input 'contentType'.

        :param string contentType: the content type target for the request
        :param string formatType:  the format type for content type target for the request

         :rtype: json service response converted to dictionary (with mininal keys: api_error_flag, api_status_text)
        """
        _params = {"request_content_type": contentType, "request_format_type": formatType}
        for p in params:
            _params[p] = params[p]
        #
        return self.__run(endPoint="summary_content", **_params)


#
###
#
