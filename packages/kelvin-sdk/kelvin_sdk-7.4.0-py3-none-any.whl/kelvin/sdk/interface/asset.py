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
from typing import Optional, Sequence

from typeguard import typechecked

from kelvin.sdk.lib.models.apps.kelvin_app import DeviceTypeName
from kelvin.sdk.lib.models.operation import OperationResponse


@typechecked
def asset_list(should_display: bool = False) -> OperationResponse:
    """
    List all the available Assets in the platform.

    Parameters
    ----------
    should_display : bool, Default=False
        Specifies whether or not the display should output data.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        An OperationResponse object encapsulating the Assets available on the platform.

    """
    from kelvin.sdk.lib.api.asset import asset_list as _asset_list

    return _asset_list(query=None, should_display=should_display)


@typechecked
def asset_search(query: str, should_display: bool = False) -> OperationResponse:
    """
    Search for specific Assets based on a query.

    Parameters
    ----------
    query : str
        The query to search for.
    should_display : bool, Default=False
        Specifies whether or not the display should output data.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the matching Assets available on the platform.

    """
    from kelvin.sdk.lib.api.asset import asset_list as _asset_list

    return _asset_list(query=query, should_display=should_display)


@typechecked
def asset_show(asset_name: str, should_display: bool = False) -> OperationResponse:
    """
    Show the details of an Asset.

    Parameters
    ----------
    asset_name : str
        The name of the asset.
    should_display : bool, Default=False
        Specifies whether or not the display should output data.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the yielded Asset instance and its detailed data.

    """
    from kelvin.sdk.lib.api.asset import asset_show as _asset_show

    return _asset_show(asset_name=asset_name, should_display=should_display)


@typechecked
def asset_create(
    asset_name: str,
    asset_type_name: str,
    asset_title: str,
    entity_type_name: DeviceTypeName,
    parent_name: Optional[str] = None,
) -> OperationResponse:
    """
    Create an Asset on the platform.

    Parameters
    ----------
    asset_name : str
        The name of the asset.
    asset_type_name : str
        The asset type name of the asset.
    asset_title : str
        The title of the asset.
    entity_type_name : DeviceTypeName
        The entity type of the asset.
    parent_name : Optional[str]
        Optional parent name of the created asset

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        An OperationResponse object encapsulating the result of an Asset creation operation.

    """
    from kelvin.sdk.lib.api.asset import asset_create as _asset_create

    return _asset_create(
        asset_name=asset_name,
        asset_type_name=asset_type_name,
        asset_title=asset_title,
        entity_type_name=entity_type_name,
        parent_name=parent_name,
    )


@typechecked
def asset_delete(asset_names: Sequence[str], ignore_destructive_warning: bool = False) -> OperationResponse:
    """
    Delete Assets from the platform.

    Parameters
    ----------
    asset_names : Sequence[str]
        The name of the asset.
    ignore_destructive_warning : bool, Default=False
        Indicates whether it should ignore the destructive warning.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        An OperationResponse object encapsulating the result of the Asset deletion operation.

    """
    from kelvin.sdk.lib.api.asset import asset_delete as _asset_delete

    return _asset_delete(asset_names=asset_names, ignore_destructive_warning=ignore_destructive_warning)


@typechecked
def asset_type_list(should_display: bool = False) -> OperationResponse:
    """
    List all the available Asset Types in the platform.

    Parameters
    ----------
    should_display : bool, Default=False
        Specifies whether or not the display should output data.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        An OperationResponse object encapsulating the Asset types available on the platform.

    """
    from kelvin.sdk.lib.api.asset import asset_type_list as _asset_type_list

    return _asset_type_list(query=None, should_display=should_display)


@typechecked
def asset_type_search(query: str, should_display: bool = False) -> OperationResponse:
    """
    Create an Asset on the platform.

    Parameters
    ----------
    query : str
        The query to search for.
    should_display : bool, Default=False
        Specifies whether or not the display should output data.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        An OperationResponse object encapsulating the Asset Types available on the platform.

    """
    from kelvin.sdk.lib.api.asset import asset_type_list as _asset_type_list

    return _asset_type_list(query=query, should_display=should_display)


@typechecked
def asset_type_create(asset_type_name: str, asset_type_title: str, asset_class_name: str) -> OperationResponse:
    """
    Create an Asset Type on the platform.

    Parameters
    ----------
    asset_type_name : str
        The name of the asset type.
    asset_type_title : str
        The title to be associated to the asset type.
    asset_class_name : str
        The asset class name associated to the new asset type.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        An OperationResponse object encapsulating the result of the Asset type creation operation.

    """
    from kelvin.sdk.lib.api.asset import asset_type_create as _asset_type_create

    return _asset_type_create(
        asset_type_name=asset_type_name, asset_type_title=asset_type_title, asset_class_name=asset_class_name
    )


@typechecked
def asset_type_delete(asset_type_names: Sequence[str], ignore_destructive_warning: bool = False) -> OperationResponse:
    """
    Delete Asset types from the platform.

    Parameters
    ----------
    asset_type_names : Sequence[str]
        The name of the asset types.
    ignore_destructive_warning : bool, Default=False
        Indicates whether it should ignore the destructive warning.

    Returns
    -------
    kelvin.sdk.lib.models.operation.OperationResponse
        An OperationResponse object encapsulating the result of the Asset type deletion operation.

    """
    from kelvin.sdk.lib.api.asset import asset_type_delete as _asset_type_delete

    return _asset_type_delete(asset_type_names=asset_type_names, ignore_destructive_warning=ignore_destructive_warning)
