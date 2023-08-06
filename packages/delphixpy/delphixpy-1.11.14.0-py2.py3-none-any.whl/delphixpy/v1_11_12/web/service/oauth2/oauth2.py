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
Package "service.oauth2"
"""
API_VERSION = "1.11.12"

try:
    from urllib import urlencode 
except ImportError:
    from urllib.parse import urlencode 
from delphixpy.v1_11_12 import response_validator

def get(engine):
    """
    Retrieve the specified OAuth2Config object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_12.delphix_engine.DelphixEngine`
    :rtype: :py:class:`v1_11_12.web.vo.OAuth2Config`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/service/oauth2"
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['OAuth2Config'], returns_list=False, raw_result=raw_result)

def set(engine, o_auth2_config=None):
    """
    Update the specified OAuth2Config object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_12.delphix_engine.DelphixEngine`
    :param o_auth2_config: Payload object.
    :type o_auth2_config: :py:class:`v1_11_12.web.vo.OAuth2Config`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/service/oauth2"
    response = engine.post(url, o_auth2_config.to_dict(dirty=True) if o_auth2_config else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def oauth2_readiness(engine, user_matching_field_type=None):
    """
    Indicates whether the conditions for enabling OAuth2 are satisfied.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_12.delphix_engine.DelphixEngine`
    :param user_matching_field_type: Specify the user field that should be
        verified to confirm OAuth2 readiness. *(permitted values: NAME,
        EMAIL_ADDRESS, PRINCIPAL)*
    :type user_matching_field_type: ``TEXT_TYPE``
    :rtype: ``TEXT_TYPE``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/service/oauth2/oauth2Readiness"
    query_params = {"userMatchingFieldType": user_matching_field_type}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['TEXT_TYPE'], returns_list=False, raw_result=raw_result)

