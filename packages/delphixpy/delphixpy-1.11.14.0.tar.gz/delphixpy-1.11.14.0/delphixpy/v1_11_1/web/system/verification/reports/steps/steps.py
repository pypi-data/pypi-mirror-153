# coding: utf8
#
# Copyright 2022 by Delphix
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
Package "system.verification.reports.steps"
"""
API_VERSION = "1.11.1"

try:
    from urllib import urlencode 
except ImportError:
    from urllib.parse import urlencode 
from delphixpy.v1_11_1 import response_validator

def get_all(engine, version=None, run_status=None, page_size=None, page_offset=None, sort_by=None, ascending=None):
    """
    List UpgradeVerificationSteps objects on the system.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_1.delphix_engine.DelphixEngine`
    :param version: The reference to the Delphix version associated with this
        verification steps.
    :type version: ``TEXT_TYPE``
    :param run_status: Result status of the step. *(permitted values: SUCCESS,
        FAILURE, SKIPPED)*
    :type run_status: ``TEXT_TYPE``
    :param page_size: Limit the number of step results returned.
    :type page_size: ``int``
    :param page_offset: Offset within result list, in units of pageSize chunks.
    :type page_offset: ``int``
    :param sort_by: Search results are sorted by the field provided.
        *(permitted values: RUN_STATUS, CLASS_NAME, START_TIMESTAMP, DURATION)*
    :type sort_by: ``TEXT_TYPE``
    :param ascending: True if results are to be returned in ascending order.
    :type ascending: ``bool``
    :rtype: ``list`` of :py:class:`v1_11_1.web.vo.UpgradeVerificationSteps`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/system/verification/reports/steps"
    query_params = {"version": version, "runStatus": run_status, "pageSize": page_size, "pageOffset": page_offset, "sortBy": sort_by, "ascending": ascending}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['UpgradeVerificationSteps'], returns_list=True, raw_result=raw_result)

