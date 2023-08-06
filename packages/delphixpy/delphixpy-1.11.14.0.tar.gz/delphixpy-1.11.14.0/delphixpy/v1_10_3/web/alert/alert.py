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
Package "alert"
"""
API_VERSION = "1.10.3"

from delphixpy.v1_10_3.web.alert import profile
try:
    from urllib import urlencode 
except ImportError:
    from urllib.parse import urlencode 
from delphixpy.v1_10_3 import response_validator

def get(engine, ref):
    """
    Retrieve the specified Alert object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_10_3.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_10_3.web.objects.Alert.Alert` object
    :type ref: ``str``
    :rtype: :py:class:`v1_10_3.web.vo.Alert`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/alert/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['Alert'], returns_list=False, raw_result=raw_result)

def get_all(engine, target=None, from_date=None, to_date=None, page_size=None, page_offset=None, max_total=None, search_text=None, ascending=None, sort_by=None):
    """
    Returns a list of alerts on the system.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_10_3.delphix_engine.DelphixEngine`
    :param target: Limit alerts to those affecting a particular object on the
        system.
    :type target: ``TEXT_TYPE``
    :param from_date: Start date to use for the search.
    :type from_date: ``TEXT_TYPE``
    :param to_date: End date to use for the search.
    :type to_date: ``TEXT_TYPE``
    :param page_size: Limit the number of alerts returned.
    :type page_size: ``int``
    :param page_offset: Offset within alert list, in units of pageSize chunks.
    :type page_offset: ``int``
    :param max_total: The upper bound for calculation of total alert count.
    :type max_total: ``int``
    :param search_text: Limit search results to only include alerts that have
        searchText string in eventTitle, eventDescription, eventResponse,
        eventAction, or severity.
    :type search_text: ``TEXT_TYPE``
    :param ascending: True if results are to be returned in ascending order.
    :type ascending: ``bool``
    :param sort_by: Search results are sorted by the field provided.
        *(permitted values: event, eventTitle, eventDescription, eventResponse,
        eventAction, eventCommandOutput, eventSeverity, target, targetName,
        timestamp)*
    :type sort_by: ``TEXT_TYPE``
    :rtype: ``list`` of :py:class:`v1_10_3.web.vo.Alert`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/alert"
    query_params = {"target": target, "fromDate": from_date, "toDate": to_date, "pageSize": page_size, "pageOffset": page_offset, "maxTotal": max_total, "searchText": search_text, "ascending": ascending, "sortBy": sort_by}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['Alert'], returns_list=True, raw_result=raw_result)

