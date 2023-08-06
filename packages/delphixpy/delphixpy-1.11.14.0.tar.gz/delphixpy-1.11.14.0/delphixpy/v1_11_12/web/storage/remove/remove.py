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
Package "storage.remove"
"""
API_VERSION = "1.11.12"

from delphixpy.v1_11_12 import response_validator

def get(engine):
    """
    Retrieve the specified StorageDeviceRemovalStatus object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_12.delphix_engine.DelphixEngine`
    :rtype: :py:class:`v1_11_12.web.vo.StorageDeviceRemovalStatus`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/storage/remove"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['StorageDeviceRemovalStatus'], returns_list=False, raw_result=raw_result)

def start(engine, storage_device_remove_parameters=None):
    """
    Remove storage devices.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_12.delphix_engine.DelphixEngine`
    :param storage_device_remove_parameters: Payload object.
    :type storage_device_remove_parameters:
        :py:class:`v1_11_12.web.vo.StorageDeviceRemoveParameters`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/storage/remove/start"
    response = engine.post(url, storage_device_remove_parameters.to_dict(dirty=True) if storage_device_remove_parameters else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def verify(engine, storage_device_remove_parameters=None):
    """
    Verify that storage devices can be removed.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_12.delphix_engine.DelphixEngine`
    :param storage_device_remove_parameters: Payload object.
    :type storage_device_remove_parameters:
        :py:class:`v1_11_12.web.vo.StorageDeviceRemoveParameters`
    :rtype: :py:class:`v1_11_12.web.vo.StorageDeviceRemovalVerifyResult`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/storage/remove/verify"
    response = engine.post(url, storage_device_remove_parameters.to_dict(dirty=True) if storage_device_remove_parameters else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['StorageDeviceRemovalVerifyResult'], returns_list=False, raw_result=raw_result)

