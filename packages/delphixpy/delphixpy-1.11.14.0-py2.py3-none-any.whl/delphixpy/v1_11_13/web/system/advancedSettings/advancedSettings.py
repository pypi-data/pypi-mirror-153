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
Package "system.advancedSettings"
"""
API_VERSION = "1.11.13"

from delphixpy.v1_11_13 import response_validator

def get(engine):
    """
    Retrieve the specified AdvancedSettingsInfo object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_13.delphix_engine.DelphixEngine`
    :rtype: :py:class:`v1_11_13.web.vo.AdvancedSettingsInfo`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/system/advancedSettings"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['AdvancedSettingsInfo'], returns_list=False, raw_result=raw_result)

def get_tunable(engine, tunable_identifier):
    """
    Get the value of a system tunable.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_13.delphix_engine.DelphixEngine`
    :param tunable_identifier: Payload object.
    :type tunable_identifier: :py:class:`v1_11_13.web.vo.TunableIdentifier`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/system/advancedSettings/getTunable"
    response = engine.post(url, tunable_identifier.to_dict(dirty=True) if tunable_identifier else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def set_tunable(engine, tunable):
    """
    Set the value of a system tunable.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_13.delphix_engine.DelphixEngine`
    :param tunable: Payload object.
    :type tunable: :py:class:`v1_11_13.web.vo.Tunable`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/system/advancedSettings/setTunable"
    response = engine.post(url, tunable.to_dict(dirty=True) if tunable else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

