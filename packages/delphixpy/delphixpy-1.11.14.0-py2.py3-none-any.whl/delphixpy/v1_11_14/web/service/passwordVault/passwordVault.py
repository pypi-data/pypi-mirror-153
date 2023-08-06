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
Package "service.passwordVault"
"""
API_VERSION = "1.11.14"

from delphixpy.v1_11_14 import response_validator

def create(engine, password_vault=None):
    """
    Create a new PasswordVault object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_14.delphix_engine.DelphixEngine`
    :param password_vault: Payload object.
    :type password_vault: :py:class:`v1_11_14.web.vo.PasswordVault`
    :rtype: ``TEXT_TYPE``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/service/passwordVault"
    response = engine.post(url, password_vault.to_dict(dirty=True) if password_vault else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['TEXT_TYPE'], returns_list=False, raw_result=raw_result)

def get(engine, ref):
    """
    Retrieve the specified PasswordVault object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_14.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_14.web.objects.PasswordVault.PasswordVault`
        object
    :type ref: ``str``
    :rtype: :py:class:`v1_11_14.web.vo.PasswordVault`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/service/passwordVault/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['PasswordVault'], returns_list=False, raw_result=raw_result)

def get_all(engine):
    """
    List PasswordVault objects on the system.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_14.delphix_engine.DelphixEngine`
    :rtype: ``list`` of :py:class:`v1_11_14.web.vo.PasswordVault`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/service/passwordVault"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['PasswordVault'], returns_list=True, raw_result=raw_result)

def update(engine, ref, password_vault=None):
    """
    Update the specified PasswordVault object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_14.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_14.web.objects.PasswordVault.PasswordVault`
        object
    :type ref: ``str``
    :param password_vault: Payload object.
    :type password_vault: :py:class:`v1_11_14.web.vo.PasswordVault`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/service/passwordVault/%s" % ref
    response = engine.post(url, password_vault.to_dict(dirty=True) if password_vault else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def delete(engine, ref):
    """
    Delete the specified PasswordVault object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_14.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_14.web.objects.PasswordVault.PasswordVault`
        object
    :type ref: ``str``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/service/passwordVault/%s/delete" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def validate(engine, ref):
    """
    Tests connection to this password vault with the configured credentials.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_14.delphix_engine.DelphixEngine`
    :param ref: Reference to a
        :py:class:`delphixpy.v1_11_14.web.objects.PasswordVault.PasswordVault`
        object
    :type ref: ``str``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/service/passwordVault/%s/validate" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def validate_vault(engine, password_vault_test_parameters=None):
    """
    Tests connection to a password vault with the provided credentials.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_14.delphix_engine.DelphixEngine`
    :param password_vault_test_parameters: Payload object.
    :type password_vault_test_parameters:
        :py:class:`v1_11_14.web.vo.PasswordVaultTestParameters`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/service/passwordVault/validateVault"
    response = engine.post(url, password_vault_test_parameters.to_dict(dirty=True) if password_vault_test_parameters else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def request_client_certificate_upload(engine, certificate_upload_parameters):
    """
    Request upload of keystore containing a private key and associated
    certificate chain.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_14.delphix_engine.DelphixEngine`
    :param certificate_upload_parameters: Payload object.
    :type certificate_upload_parameters:
        :py:class:`v1_11_14.web.vo.CertificateUploadParameters`
    :rtype: :py:class:`v1_11_14.web.vo.FileUploadResult`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/service/passwordVault/requestClientCertificateUpload"
    response = engine.post(url, certificate_upload_parameters.to_dict(dirty=True) if certificate_upload_parameters else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['FileUploadResult'], returns_list=False, raw_result=raw_result)

