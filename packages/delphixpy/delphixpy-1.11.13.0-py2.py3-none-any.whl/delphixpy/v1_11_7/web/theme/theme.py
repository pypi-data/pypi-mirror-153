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
Package "theme"
"""
API_VERSION = "1.11.7"

try:
    from urllib import urlencode 
except ImportError:
    from urllib.parse import urlencode 
from delphixpy.v1_11_7 import response_validator

def create(engine, theme=None):
    """
    Create a new Theme object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_7.delphix_engine.DelphixEngine`
    :param theme: Payload object.
    :type theme: :py:class:`v1_11_7.web.vo.Theme`
    :rtype: ``TEXT_TYPE``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/theme"
    response = engine.post(url, theme.to_dict(dirty=True) if theme else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['TEXT_TYPE'], returns_list=False, raw_result=raw_result)

def get(engine, ref):
    """
    Retrieve the specified Theme object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_7.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_7.web.objects.Theme.Theme` object
    :type ref: ``str``
    :rtype: :py:class:`v1_11_7.web.vo.Theme`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/theme/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['Theme'], returns_list=False, raw_result=raw_result)

def get_all(engine, page_size=None, page_offset=None, active=None):
    """
    Returns the list of themes.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_7.delphix_engine.DelphixEngine`
    :param page_size: Limit the number of check results returned.
    :type page_size: ``int``
    :param page_offset: Offset within result list, in units of pageSize chunks.
    :type page_offset: ``int``
    :param active: Decides whether or not to only return active theme.
    :type active: ``bool``
    :rtype: ``list`` of :py:class:`v1_11_7.web.vo.Theme`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/theme"
    query_params = {"pageSize": page_size, "pageOffset": page_offset, "active": active}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['Theme'], returns_list=True, raw_result=raw_result)

def update(engine, ref, theme=None):
    """
    Update the specified Theme object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_7.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_7.web.objects.Theme.Theme` object
    :type ref: ``str``
    :param theme: Payload object.
    :type theme: :py:class:`v1_11_7.web.vo.Theme`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/theme/%s" % ref
    response = engine.post(url, theme.to_dict(dirty=True) if theme else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def delete(engine, ref):
    """
    Delete the specified Theme object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_7.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_7.web.objects.Theme.Theme` object
    :type ref: ``str``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/theme/%s/delete" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def set_active_theme(engine, theme_reference_parameter=None):
    """
    Sets a theme as active. Passing null reference resets active themes.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_7.delphix_engine.DelphixEngine`
    :param theme_reference_parameter: Payload object.
    :type theme_reference_parameter:
        :py:class:`v1_11_7.web.vo.ThemeReferenceParameter`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/theme/setActiveTheme"
    response = engine.post(url, theme_reference_parameter.to_dict(dirty=True) if theme_reference_parameter else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

