"""
Copyright 2021 Kelvin Inc.

Licensed under the Kelvin Inc. Developer SDK License Agreement (the "License"); you may not use
this file except in compliance with the License.  You may obtain a copy of the
License at

http://www.kelvininc.com/developer-sdk-license

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OF ANY KIND, either express or implied.  See the License for the
specific language governing permissions and limitations under the License.
"""
from typing import Optional

from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.server.models.router import KelvinSDKServerRouter

router = KelvinSDKServerRouter(
    prefix="/appregistry",
    tags=["App Registry - [kelvin appregistry]"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
def appregistry_list(query: Optional[str] = None) -> OperationResponse:
    """
    Returns the list of apps on the registry.
    """
    if query:
        from kelvin.sdk.interface import appregistry_search as _appregistry_search

        return _appregistry_search(query=query, should_display=False)
    else:
        from kelvin.sdk.interface import appregistry_list as _appregistry_list

        return _appregistry_list(should_display=False)


@router.get("/{app_name}")
def appregistry_show(app_name: str) -> OperationResponse:
    """
    Returns detailed information on the specified application.
    """
    from kelvin.sdk.interface import appregistry_show as _appregistry_show

    return _appregistry_show(app_name=app_name, should_display=False)


@router.get("/{app_name_with_version}/download")
def appregistry_download(app_name_with_version: str, override_local_tag: bool = False) -> OperationResponse:
    """
    Downloads the specified application from the platform's app registry.
    """
    from kelvin.sdk.interface import appregistry_download as _appregistry_download

    return _appregistry_download(app_name_with_version=app_name_with_version, override_local_tag=override_local_tag)


@router.delete("/{app_name_with_version}")
def appregistry_delete(app_name_with_version: str) -> OperationResponse:
    """
    Deletes the specified application the platform's app registry.
    """
    from kelvin.sdk.interface import appregistry_delete as _appregistry_delete

    return _appregistry_delete(app_name_with_version=app_name_with_version, ignore_destructive_warning=True)
