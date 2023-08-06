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
Package "service.snmp.v2.manager"
"""
API_VERSION = "1.11.12"

from delphixpy.v1_11_12 import response_validator

def create(engine, snmpv2_manager=None):
    """
    Create a new SNMPV2Manager object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_12.delphix_engine.DelphixEngine`
    :param snmpv2_manager: Payload object.
    :type snmpv2_manager: :py:class:`v1_11_12.web.vo.SNMPV2Manager`
    :rtype: ``TEXT_TYPE``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/service/snmp/v2/manager"
    response = engine.post(url, snmpv2_manager.to_dict(dirty=True) if snmpv2_manager else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['TEXT_TYPE'], returns_list=False, raw_result=raw_result)

def get(engine, ref):
    """
    Retrieve the specified SNMPV2Manager object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_12.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_12.web.objects.SNMPV2Manager.SNMPV2Manager`
        object
    :type ref: ``str``
    :rtype: :py:class:`v1_11_12.web.vo.SNMPV2Manager`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/service/snmp/v2/manager/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['SNMPV2Manager'], returns_list=False, raw_result=raw_result)

def get_all(engine):
    """
    Lists SNMP managers in the system.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_12.delphix_engine.DelphixEngine`
    :rtype: ``list`` of :py:class:`v1_11_12.web.vo.SNMPV2Manager`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/service/snmp/v2/manager"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['SNMPV2Manager'], returns_list=True, raw_result=raw_result)

def update(engine, ref, snmpv2_manager=None):
    """
    Update the specified SNMPV2Manager object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_12.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_12.web.objects.SNMPV2Manager.SNMPV2Manager`
        object
    :type ref: ``str``
    :param snmpv2_manager: Payload object.
    :type snmpv2_manager: :py:class:`v1_11_12.web.vo.SNMPV2Manager`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/service/snmp/v2/manager/%s" % ref
    response = engine.post(url, snmpv2_manager.to_dict(dirty=True) if snmpv2_manager else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def delete(engine, ref):
    """
    Delete the specified SNMPV2Manager object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_12.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_12.web.objects.SNMPV2Manager.SNMPV2Manager`
        object
    :type ref: ``str``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/service/snmp/v2/manager/%s/delete" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def test(engine, ref):
    """
    Tests the ability to send an SNMP INFORM message to the manager (only
    applies when useInform is true).

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_12.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_12.web.objects.SNMPV2Manager.SNMPV2Manager`
        object
    :type ref: ``str``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/service/snmp/v2/manager/%s/test" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

