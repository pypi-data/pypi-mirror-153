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
from kelvin.sdk.server.models.parameter_models import AssetTypeCreationObject
from kelvin.sdk.server.models.router import KelvinSDKServerRouter

router = KelvinSDKServerRouter(
    prefix="/asset_types",
    tags=["Asset Types - [kelvin asset type]"],
    responses={404: {"description": "Not found"}},
)


@router.get("")
def asset_type_list(query: Optional[str] = None) -> OperationResponse:
    """
    List all the available Asset Types in the platform.
    """
    if query:
        from kelvin.sdk.interface import asset_type_search as _asset_type_search

        return _asset_type_search(query=query, should_display=False)
    else:
        from kelvin.sdk.interface import asset_type_list as _asset_type_list

        return _asset_type_list(should_display=False)


@router.post("")
def asset_type_create(asset_type_creation_object: AssetTypeCreationObject) -> OperationResponse:
    """
    Create an Asset Type on the platform.
    """

    from kelvin.sdk.interface import asset_type_create as _asset_type_create

    return _asset_type_create(
        asset_type_name=asset_type_creation_object.asset_type_name,
        asset_type_title=asset_type_creation_object.asset_type_title,
        asset_class_name=asset_type_creation_object.asset_class_name,
    )


@router.delete("/{asset_type_name}")
def asset_type_delete(asset_type_name: str) -> OperationResponse:
    """
    Delete Asset types from the platform.
    """
    from kelvin.sdk.interface import asset_type_delete as _asset_type_delete

    return _asset_type_delete(asset_type_names=[asset_type_name], ignore_destructive_warning=True)
