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
Package "system.upgradeCheckResult"
"""
API_VERSION = "1.11.2"

try:
    from urllib import urlencode 
except ImportError:
    from urllib.parse import urlencode 
from delphixpy.v1_11_2 import response_validator

def get(engine, ref):
    """
    Retrieve the specified UpgradeCheckResult object.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_2.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_11_2.web.objects.Upgrade
        CheckResult.UpgradeCheckResult` object
    :type ref: ``str``
    :rtype: :py:class:`v1_11_2.web.vo.UpgradeCheckResult`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/system/upgradeCheckResult/%s" % ref
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['UpgradeCheckResult'], returns_list=False, raw_result=raw_result)

def get_all(engine, version=None, status=None, page_size=None, page_offset=None, sort_by=None, ascending=None):
    """
    Returns the list of all the check results that match the given criteria.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_2.delphix_engine.DelphixEngine`
    :param version: The reference to the Delphix version associated with this
        verification check.
    :type version: ``TEXT_TYPE``
    :param status: The status of the upgrade check result. *(permitted values:
        ACTIVE, IGNORED, RESOLVED)*
    :type status: ``TEXT_TYPE``
    :param page_size: Limit the number of check results returned.
    :type page_size: ``int``
    :param page_offset: Offset within result list, in units of pageSize chunks.
    :type page_offset: ``int``
    :param sort_by: Search results are sorted by the field provided.
        *(permitted values: SEVERITY, TITLE, VERSION, STATUS)*
    :type sort_by: ``TEXT_TYPE``
    :param ascending: True if results are to be returned in ascending order.
    :type ascending: ``bool``
    :rtype: ``list`` of :py:class:`v1_11_2.web.vo.UpgradeCheckResult`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/system/upgradeCheckResult"
    query_params = {"version": version, "status": status, "pageSize": page_size, "pageOffset": page_offset, "sortBy": sort_by, "ascending": ascending}
    query_dct = {k: query_params[k] for k in query_params if query_params[k] is not None}
    if query_dct:
        url_params = urlencode(query_dct)
        url += "?%s" % url_params
    response = engine.get(url)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=['UpgradeCheckResult'], returns_list=True, raw_result=raw_result)

def ignore(engine, ref):
    """
    Ignore this check result. Ignored checks do not return on subsequent
    verifications.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_2.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_11_2.web.objects.Upgrade
        CheckResult.UpgradeCheckResult` object
    :type ref: ``str``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/system/upgradeCheckResult/%s/ignore" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def resolve(engine, ref):
    """
    Mark this check result as resolved. Resolved checks return if their
    requirements remain unmet.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_2.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_11_2.web.objects.Upgrade
        CheckResult.UpgradeCheckResult` object
    :type ref: ``str``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/system/upgradeCheckResult/%s/resolve" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def reset(engine, ref):
    """
    Resets this check result, clearing its ignored or resolved status.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_2.delphix_engine.DelphixEngine`
    :param ref: Reference to a :py:class:`delphixpy.v1_11_2.web.objects.Upgrade
        CheckResult.UpgradeCheckResult` object
    :type ref: ``str``
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/system/upgradeCheckResult/%s/reset" % ref
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def resolve_selected(engine, resolve_or_ignore_selected_checks_parameters):
    """
    Marks selected check results as resolved.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_2.delphix_engine.DelphixEngine`
    :param resolve_or_ignore_selected_checks_parameters: Payload object.
    :type resolve_or_ignore_selected_checks_parameters:
        :py:class:`v1_11_2.web.vo.ResolveOrIgnoreSelectedChecksParameters`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/system/upgradeCheckResult/resolveSelected"
    response = engine.post(url, resolve_or_ignore_selected_checks_parameters.to_dict(dirty=True) if resolve_or_ignore_selected_checks_parameters else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def ignore_selected(engine, resolve_or_ignore_selected_checks_parameters):
    """
    Marks selected check results as ignored.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_2.delphix_engine.DelphixEngine`
    :param resolve_or_ignore_selected_checks_parameters: Payload object.
    :type resolve_or_ignore_selected_checks_parameters:
        :py:class:`v1_11_2.web.vo.ResolveOrIgnoreSelectedChecksParameters`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/system/upgradeCheckResult/ignoreSelected"
    response = engine.post(url, resolve_or_ignore_selected_checks_parameters.to_dict(dirty=True) if resolve_or_ignore_selected_checks_parameters else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def reset_selected(engine, resolve_or_ignore_selected_checks_parameters):
    """
    Reset selected check results to active.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_2.delphix_engine.DelphixEngine`
    :param resolve_or_ignore_selected_checks_parameters: Payload object.
    :type resolve_or_ignore_selected_checks_parameters:
        :py:class:`v1_11_2.web.vo.ResolveOrIgnoreSelectedChecksParameters`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/system/upgradeCheckResult/resetSelected"
    response = engine.post(url, resolve_or_ignore_selected_checks_parameters.to_dict(dirty=True) if resolve_or_ignore_selected_checks_parameters else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def resolve_version_checks(engine, upgrade_version_checks_parameter):
    """
    Marks check results as resolved for a version. Will not update
    INFORMATIONAL checks.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_2.delphix_engine.DelphixEngine`
    :param upgrade_version_checks_parameter: Payload object.
    :type upgrade_version_checks_parameter:
        :py:class:`v1_11_2.web.vo.UpgradeVersionChecksParameter`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/system/upgradeCheckResult/resolveVersionChecks"
    response = engine.post(url, upgrade_version_checks_parameter.to_dict(dirty=True) if upgrade_version_checks_parameter else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def ignore_version_checks(engine, upgrade_version_checks_parameter):
    """
    Marks check results as ignored for a version. Only affects WARNING checks.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_2.delphix_engine.DelphixEngine`
    :param upgrade_version_checks_parameter: Payload object.
    :type upgrade_version_checks_parameter:
        :py:class:`v1_11_2.web.vo.UpgradeVersionChecksParameter`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/system/upgradeCheckResult/ignoreVersionChecks"
    response = engine.post(url, upgrade_version_checks_parameter.to_dict(dirty=True) if upgrade_version_checks_parameter else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def reset_version_checks(engine, upgrade_version_checks_parameter):
    """
    Reset check results to active for a version.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_2.delphix_engine.DelphixEngine`
    :param upgrade_version_checks_parameter: Payload object.
    :type upgrade_version_checks_parameter:
        :py:class:`v1_11_2.web.vo.UpgradeVersionChecksParameter`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/system/upgradeCheckResult/resetVersionChecks"
    response = engine.post(url, upgrade_version_checks_parameter.to_dict(dirty=True) if upgrade_version_checks_parameter else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

