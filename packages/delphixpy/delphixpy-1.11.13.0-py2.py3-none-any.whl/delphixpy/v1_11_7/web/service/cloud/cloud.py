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
Package "service.cloud"
"""
API_VERSION = "1.11.7"

from delphixpy.v1_11_7 import response_validator

def get(engine):
    """
    Retrieve the specified CloudStatus object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_7.delphix_engine.DelphixEngine`
    :rtype: :py:class:`v1_11_7.web.vo.CloudStatus`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/service/cloud"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['CloudStatus'], returns_list=False, raw_result=raw_result)

def set(engine, cloud_status=None):
    """
    Update the specified CloudStatus object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_7.delphix_engine.DelphixEngine`
    :param cloud_status: Payload object.
    :type cloud_status: :py:class:`v1_11_7.web.vo.CloudStatus`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/service/cloud"
    response = engine.post(url, cloud_status.to_dict(dirty=True) if cloud_status else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def enable(engine, cloud_enable_parameters=None):
    """
    Enable the Delphix Central Management Connector.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_7.delphix_engine.DelphixEngine`
    :param cloud_enable_parameters: Payload object.
    :type cloud_enable_parameters:
        :py:class:`v1_11_7.web.vo.CloudEnableParameters`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/service/cloud/enable"
    response = engine.post(url, cloud_enable_parameters.to_dict(dirty=True) if cloud_enable_parameters else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def disable(engine):
    """
    Disable the Delphix Central Management Connector.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_7.delphix_engine.DelphixEngine`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/service/cloud/disable"
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def rollback(engine):
    """
    Rollback to the previous working Delphix Central Management Connector.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_7.delphix_engine.DelphixEngine`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/service/cloud/rollback"
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

