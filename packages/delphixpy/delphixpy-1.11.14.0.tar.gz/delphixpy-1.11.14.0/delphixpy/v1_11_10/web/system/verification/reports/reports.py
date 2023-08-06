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
Package "system.verification.reports"
"""
API_VERSION = "1.11.10"

try:
    from urllib import urlencode 
except ImportError:
    from urllib.parse import urlencode 
from delphixpy.v1_11_10 import response_validator

def get(engine, ref):
    """
    Retrieve the specified UpgradeVerificationReport object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_11_10.web.objects.Upgrad
        eVerificationReport.UpgradeVerificationReport` object
    :type ref: ``str``
    :rtype: :py:class:`v1_11_10.web.vo.UpgradeVerificationReport`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/system/verification/reports/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['UpgradeVerificationReport'], returns_list=False, raw_result=raw_result)

def get_all(engine, version=None, page_size=None, page_offset=None, sort_by=None, ascending=None):
    """
    List UpgradeVerificationReport objects on the system.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :param version: The reference to the Delphix version associated with this
        verification report.
    :type version: ``TEXT_TYPE``
    :param page_size: Limit the number of report results returned.
    :type page_size: ``int``
    :param page_offset: Offset within result list, in units of pageSize chunks.
    :type page_offset: ``int``
    :param sort_by: Search results are sorted by the field provided.
        *(permitted values: VERSION, VERIFICATION_VERSION)*
    :type sort_by: ``TEXT_TYPE``
    :param ascending: True if results are to be returned in ascending order.
    :type ascending: ``bool``
    :rtype: ``list`` of :py:class:`v1_11_10.web.vo.UpgradeVerificationReport`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/system/verification/reports"
    query_params = {"version": version, "pageSize": page_size, "pageOffset": page_offset, "sortBy": sort_by, "ascending": ascending}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['UpgradeVerificationReport'], returns_list=True, raw_result=raw_result)

