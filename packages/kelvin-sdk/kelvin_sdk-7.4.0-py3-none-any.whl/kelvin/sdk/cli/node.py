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

import click
from click import Choice

from kelvin.sdk.lib.configs.general_configs import KSDKHelpMessages
from kelvin.sdk.lib.models.types import StatusDataSource
from kelvin.sdk.lib.utils.click_utils import KSDKCommand, KSDKGroup


@click.group(cls=KSDKGroup)
def node() -> bool:
    """
    Manage and view nodes.

    """


@node.command(cls=KSDKCommand)
def list() -> bool:
    """
    List all the available nodes in the platform.

    """
    from kelvin.sdk.interface import node_list

    return node_list(should_display=True).success


@node.command(cls=KSDKCommand)
@click.argument("query", nargs=1, type=click.STRING)
def search(query: str) -> bool:
    """
    Search for specific nodes based on a query.

    e.g. kelvin node search "my-node"
    """
    from kelvin.sdk.interface import node_search

    return node_search(query=query, should_display=True).success


@node.command(cls=KSDKCommand)
@click.argument("node_name", nargs=1, type=click.STRING)
@click.option("--source", type=Choice(StatusDataSource.as_list()), required=False, help=KSDKHelpMessages.status_source)
def show(node_name: str, source: str) -> bool:
    """
    Show the details of an node.

    e.g. kelvin node show "my-node"
    """
    from kelvin.sdk.interface import node_show

    return node_show(node_name=node_name, source=StatusDataSource(source), should_display=True).success


@node.command(cls=KSDKCommand)
@click.argument("node_name", nargs=1, type=click.STRING)
@click.option("-y", "--yes", default=False, is_flag=True, show_default=True, help=KSDKHelpMessages.yes)
def delete(node_name: str, yes: bool) -> bool:
    """
    Delete a node from the platform.

    e.g. kelvin node delete "my-node"

    """
    from kelvin.sdk.interface import node_delete

    return node_delete(node_name=node_name, ignore_destructive_warning=yes).success


@node.command(cls=KSDKCommand)
def provision_script() -> bool:
    """
    Add a node to the Kelvin platform in 2 easy steps.

    In a matter of minutes you can have your node up and running.

    """
    from kelvin.sdk.interface import node_provision_script

    return node_provision_script().success
