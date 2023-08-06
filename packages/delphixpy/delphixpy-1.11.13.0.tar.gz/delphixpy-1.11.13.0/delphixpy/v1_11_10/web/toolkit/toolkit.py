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
Package "toolkit"
"""
API_VERSION = "1.11.10"

try:
    from urllib import urlencode 
except ImportError:
    from urllib.parse import urlencode 
from delphixpy.v1_11_10 import response_validator

def get(engine, ref):
    """
    Retrieve the specified AbstractToolkit object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_10.web.objects.AbstractToolkit.AbstractToolk
        it` object
    :type ref: ``str``
    :rtype: :py:class:`v1_11_10.web.vo.AbstractToolkit`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/toolkit/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['AbstractToolkit'], returns_list=False, raw_result=raw_result)

def get_all(engine, source_environment=None):
    """
    Lists installed toolkits.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :param source_environment: Restricts list to include only toolkits that are
        valid for the given source environment.
    :type source_environment: ``TEXT_TYPE``
    :rtype: ``list`` of :py:class:`v1_11_10.web.vo.AbstractToolkit`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/toolkit"
    query_params = {"sourceEnvironment": source_environment}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['AbstractToolkit'], returns_list=True, raw_result=raw_result)

def delete(engine, ref):
    """
    Delete the specified AbstractToolkit object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_10.web.objects.AbstractToolkit.AbstractToolk
        it` object
    :type ref: ``str``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/toolkit/%s/delete" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def list_all_sources(engine, ref):
    """
    List all Sources using this toolkit.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_10.web.objects.AbstractToolkit.AbstractToolk
        it` object
    :type ref: ``str``
    :rtype: ``list`` of :py:class:`v1_11_10.web.vo.Source`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/toolkit/%s/listAllSources" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['Source'], returns_list=True, raw_result=raw_result)

def disable_all_sources(engine, ref, source_disable_parameters=None):
    """
    Disables all the sources using this toolkit.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_10.web.objects.AbstractToolkit.AbstractToolk
        it` object
    :type ref: ``str``
    :param source_disable_parameters: Payload object.
    :type source_disable_parameters:
        :py:class:`v1_11_10.web.vo.SourceDisableParameters`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/toolkit/%s/disableAllSources" % ref
    response = engine.post(url, source_disable_parameters.to_dict(dirty=True) if source_disable_parameters else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def upgrade(engine, ref):
    """
    Upgrades this toolkit and marks it active on success.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_10.web.objects.AbstractToolkit.AbstractToolk
        it` object
    :type ref: ``str``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/toolkit/%s/upgrade" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def request_upload_token(engine):
    """
    Request toolkit upload token.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :rtype: :py:class:`v1_11_10.web.vo.FileUploadResult`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/toolkit/requestUploadToken"
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['FileUploadResult'], returns_list=False, raw_result=raw_result)

def supported_virtualization_api_range(engine):
    """
    Get the range of supported Virtualization API versions.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :rtype: :py:class:`v1_11_10.web.vo.VirtualizationPlatformAPIRange`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/toolkit/supportedVirtualizationApiRange"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['VirtualizationPlatformAPIRange'], returns_list=False, raw_result=raw_result)

def request_active_toolkit(engine, toolkit=None):
    """
    Get the active toolkit based on the ref's id passed in.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :param toolkit: The object reference of the toolkit.
    :type toolkit: ``TEXT_TYPE``
    :rtype: :py:class:`v1_11_10.web.vo.AbstractToolkit`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/toolkit/requestActiveToolkit"
    query_params = {"toolkit": toolkit}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['AbstractToolkit'], returns_list=False, raw_result=raw_result)

def schema_definitions(engine):
    """
    Get the platform's JSON schema definitions that plugin schemas can
    reference.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :rtype: :py:class:`v1_11_10.web.vo.SchemaDraftV4`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/toolkit/schemaDefinitions"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['SchemaDraftV4'], returns_list=False, raw_result=raw_result)

