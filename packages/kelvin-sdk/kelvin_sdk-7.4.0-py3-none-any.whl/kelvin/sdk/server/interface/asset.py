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

from kelvin.sdk.lib.models.apps.kelvin_app import DeviceTypeName
from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.server.models.parameter_models import AssetCreationObject
from kelvin.sdk.server.models.router import KelvinSDKServerRouter

router = KelvinSDKServerRouter(
    prefix="/assets",
    tags=["Assets - [kelvin asset]"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
def asset_list(query: Optional[str] = None) -> OperationResponse:
    """
    List all the available Assets in the platform.
    """
    if query:
        from kelvin.sdk.interface import asset_search as _asset_search

        return _asset_search(query=query, should_display=False)
    else:
        from kelvin.sdk.interface import asset_list as _asset_list

        return _asset_list(should_display=False)


@router.post("")
def asset_create(asset_creation_object: AssetCreationObject) -> OperationResponse:
    """
    Create an Asset on the platform.
    """

    from kelvin.sdk.interface import asset_create as _asset_create

    return _asset_create(
        asset_name=asset_creation_object.asset_name,
        asset_type_name=asset_creation_object.asset_type_name,
        asset_title=asset_creation_object.asset_title,
        entity_type_name=DeviceTypeName(asset_creation_object.entity_type_name),
        parent_name=asset_creation_object.parent,
    )


@router.get("/{asset_name}")
def asset_show(asset_name: str) -> OperationResponse:
    """
    Show the details of an Asset.
    """
    from kelvin.sdk.interface import asset_show as _asset_show

    return _asset_show(asset_name=asset_name, should_display=False)


@router.delete("/{asset_name}")
def asset_delete(asset_name: str) -> OperationResponse:
    """
    Delete Assets from the platform.
    """
    from kelvin.sdk.interface import asset_delete as _asset_delete

    return _asset_delete(asset_names=[asset_name], ignore_destructive_warning=True)
