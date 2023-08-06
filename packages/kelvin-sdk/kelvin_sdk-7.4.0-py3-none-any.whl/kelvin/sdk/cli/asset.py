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
from typing import Sequence

import click
from click import Choice

from kelvin.sdk.lib.configs.general_configs import KSDKHelpMessages
from kelvin.sdk.lib.models.apps.kelvin_app import DeviceTypeName
from kelvin.sdk.lib.utils.click_utils import KSDKCommand, KSDKGroup


@click.group(cls=KSDKGroup)
def asset() -> bool:
    """
    Manage and view assets.

    """


@asset.command(cls=KSDKCommand)
def list() -> bool:
    """
    List all the available assets in the platform.

    """
    from kelvin.sdk.interface import asset_list

    return asset_list(should_display=True).success


@asset.command(cls=KSDKCommand)
@click.argument("query", nargs=1, type=click.STRING)
def search(query: str) -> bool:
    """
    Search for specific assets based on a query.

    e.g. kelvin asset search "my-asset"
    """
    from kelvin.sdk.interface import asset_search

    return asset_search(query=query, should_display=True).success


@asset.command(cls=KSDKCommand)
@click.argument("asset_name", nargs=1, type=click.STRING)
def show(asset_name: str) -> bool:
    """
    Show the details of an Asset.

    e.g. kelvin asset show "my-asset"
    """
    from kelvin.sdk.interface import asset_show

    return asset_show(asset_name=asset_name, should_display=True).success


@asset.command(cls=KSDKCommand)
@click.argument("asset_name", nargs=1, default=None, type=click.STRING)
@click.option("--type-name", required=True, type=click.STRING, help=KSDKHelpMessages.asset_type_name)
@click.option("--title", required=True, type=click.STRING, help=KSDKHelpMessages.asset_title)
@click.option(
    "--entity-type-name",
    required=True,
    type=Choice(DeviceTypeName.as_list()),
    help=KSDKHelpMessages.asset_entity_type_name,
)
@click.option("--parent", required=False, type=click.STRING, help=KSDKHelpMessages.asset_parent_name)
def create(asset_name: str, type_name: str, title: str, entity_type_name: str, parent: str) -> bool:
    """
    Create a new Asset based on the specified parameters.

    """
    from kelvin.sdk.interface import asset_create

    entity_type = DeviceTypeName(entity_type_name)

    return asset_create(
        asset_name=asset_name,
        asset_type_name=type_name,
        asset_title=title,
        entity_type_name=entity_type,
        parent_name=parent,
    ).success


@asset.command(cls=KSDKCommand)
@click.argument("asset_names", nargs=-1, type=click.STRING)
@click.option("-y", "--yes", default=False, is_flag=True, show_default=True, help=KSDKHelpMessages.yes)
def delete(asset_names: Sequence[str], yes: bool) -> bool:
    """
    Delete an Asset from the platform.

    e.g. kelvin asset delete "my-asset"

    """
    from kelvin.sdk.interface import asset_delete

    return asset_delete(asset_names=asset_names, ignore_destructive_warning=yes).success


@asset.group(cls=KSDKGroup)
def type() -> bool:
    """
    Manage and view Asset Types.

    """


@type.command(cls=KSDKCommand, name="list")
def list_asset_type() -> bool:
    """
    List all the available Asset types in the platform.

    """
    from kelvin.sdk.interface import asset_type_list

    return asset_type_list(should_display=True).success


@type.command(cls=KSDKCommand, name="search")
@click.argument("query", nargs=1, type=click.STRING)
def search_asset_type(query: str) -> bool:
    """
    Search for specific Asset types in the platform.

    """
    from kelvin.sdk.interface import asset_type_search

    return asset_type_search(query=query, should_display=True).success


@type.command(cls=KSDKCommand, name="create")
@click.argument("name", nargs=1, default=None, type=click.STRING)
@click.argument("title", nargs=1, default=None, type=click.STRING)
@click.argument("asset_class_name", nargs=1, default=None, type=click.STRING)
def create_asset_type(name: str, title: str, asset_class_name: str) -> bool:
    """
    Create a new Asset type based on the specified parameters.

    """
    from kelvin.sdk.interface import asset_type_create

    return asset_type_create(asset_type_name=name, asset_type_title=title, asset_class_name=asset_class_name).success


@type.command(cls=KSDKCommand, name="delete")
@click.argument("asset_type_names", nargs=-1, type=click.STRING)
@click.option("-y", "--yes", default=False, is_flag=True, show_default=True, help=KSDKHelpMessages.yes)
def delete_asset_type(asset_type_names: Sequence[str], yes: bool) -> bool:
    """
    Delete Asset types from the platform.

    e.g. kelvin asset type delete "my-asset-type"

    """
    from kelvin.sdk.interface import asset_type_delete

    return asset_type_delete(asset_type_names=asset_type_names, ignore_destructive_warning=yes).success
