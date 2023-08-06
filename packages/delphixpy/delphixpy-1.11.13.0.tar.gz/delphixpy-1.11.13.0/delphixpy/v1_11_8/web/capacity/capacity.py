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
Package "capacity"
"""
API_VERSION = "1.11.8"

from delphixpy.v1_11_8.web.capacity import snapshot
from delphixpy.v1_11_8.web.capacity import group
from delphixpy.v1_11_8.web.capacity import consumer
from delphixpy.v1_11_8.web.capacity import system
from delphixpy.v1_11_8.web.capacity import heldspace
from delphixpy.v1_11_8 import response_validator

def clear_cache(engine):
    """
    Clears cached capacity data. Forces a refresh on next retrieval.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_8.delphix_engine.DelphixEngine`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/capacity/clearCache"
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def refresh(engine):
    """
    Refresh capacity data asynchronously in a job.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_8.delphix_engine.DelphixEngine`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/capacity/refresh"
    response = engine.post(url, None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

def delete_dependencies(engine, capacity_delete_dependencies_parameters):
    """
    Delete a collection of objects in a dependency tree.

    :param engine: The Delphix Engine
    :type engine: :py:class:`delphixpy.v1_11_8.delphix_engine.DelphixEngine`
    :param capacity_delete_dependencies_parameters: Payload object.
    :type capacity_delete_dependencies_parameters:
        :py:class:`v1_11_8.web.vo.CapacityDeleteDependenciesParameters`
    """
    assert API_VERSION == engine.API_VERSION, "Wrong API version (%s) for parameter 'engine' (%s)" % (API_VERSION, engine.API_VERSION)
    url = "/resources/json/delphix/capacity/deleteDependencies"
    response = engine.post(url, capacity_delete_dependencies_parameters.to_dict(dirty=True) if capacity_delete_dependencies_parameters else None)
    result = response_validator.validate(response, engine)
    raw_result = getattr(engine, 'raw_result', False)
    return response_validator.parse_result(result, undef_enabled=True, return_types=None, returns_list=None, raw_result=raw_result)

