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
Package "storage.iscsi.target"
"""
API_VERSION = "1.11.10"

from delphixpy.v1_11_10 import response_validator

def create(engine, iscsi_target=None):
    """
    Create a new IscsiTarget object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :param iscsi_target: Payload object.
    :type iscsi_target: :py:class:`v1_11_10.web.vo.IscsiTarget`
    :rtype: ``TEXT_TYPE``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/storage/iscsi/target"
    response = engine.post(url, iscsi_target.to_dict(dirty=True) if iscsi_target else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['TEXT_TYPE'], returns_list=False, raw_result=raw_result)

def get(engine, ref):
    """
    Retrieve the specified IscsiTarget object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_10.web.objects.IscsiTarget.IscsiTarget`
        object
    :type ref: ``str``
    :rtype: :py:class:`v1_11_10.web.vo.IscsiTarget`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/storage/iscsi/target/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['IscsiTarget'], returns_list=False, raw_result=raw_result)

def get_all(engine):
    """
    List IscsiTarget objects on the system.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :rtype: ``list`` of :py:class:`v1_11_10.web.vo.IscsiTarget`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/storage/iscsi/target"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['IscsiTarget'], returns_list=True, raw_result=raw_result)

def update(engine, ref, iscsi_target=None):
    """
    Update the specified IscsiTarget object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_10.web.objects.IscsiTarget.IscsiTarget`
        object
    :type ref: ``str``
    :param iscsi_target: Payload object.
    :type iscsi_target: :py:class:`v1_11_10.web.vo.IscsiTarget`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/storage/iscsi/target/%s" % ref
    response = engine.post(url, iscsi_target.to_dict(dirty=True) if iscsi_target else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def delete(engine, ref):
    """
    Delete the specified IscsiTarget object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_10.web.objects.IscsiTarget.IscsiTarget`
        object
    :type ref: ``str``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/storage/iscsi/target/%s/delete" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def login(engine, ref):
    """
    Establish a connection and login to iSCSI entry.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_10.web.objects.IscsiTarget.IscsiTarget`
        object
    :type ref: ``str``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/storage/iscsi/target/%s/login" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def logout(engine, ref):
    """
    Terminate connection and logout of iSCSI entry.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_10.web.objects.IscsiTarget.IscsiTarget`
        object
    :type ref: ``str``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/storage/iscsi/target/%s/logout" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def discover(engine, iscsi_target_discover_parameters):
    """
    Discover targets in an iSCSI portal.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_10.delphix_engine.DelphixEngine`
    :param iscsi_target_discover_parameters: Payload object.
    :type iscsi_target_discover_parameters:
        :py:class:`v1_11_10.web.vo.IscsiTargetDiscoverParameters`
    :rtype: ``list`` of ``TEXT_TYPE``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/storage/iscsi/target/discover"
    response = engine.post(url, iscsi_target_discover_parameters.to_dict(dirty=True) if iscsi_target_discover_parameters else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['TEXT_TYPE'], returns_list=True, raw_result=raw_result)

