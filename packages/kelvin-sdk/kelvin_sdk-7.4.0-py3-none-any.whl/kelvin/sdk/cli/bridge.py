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

from kelvin.sdk.lib.utils.click_utils import KSDKCommand, KSDKGroup


@click.group(cls=KSDKGroup)
def bridge() -> bool:
    """
    Manage and view bridges.

    """


@bridge.command(cls=KSDKCommand)
def list() -> bool:
    """
    List all available bridges in the platform.

    """
    from kelvin.sdk.interface import bridge_list

    return bridge_list(should_display=True).success


@bridge.command(cls=KSDKCommand)
@click.argument("query", nargs=1, type=click.STRING)
def search(query: str) -> bool:
    """
    Search for specific bridges based on a query.

    e.g. kelvin bridge search "my-bridge"
    """
    from kelvin.sdk.interface import bridge_search

    return bridge_search(query=query, should_display=True).success


@bridge.command(cls=KSDKCommand)
@click.argument("bridge_name", nargs=1, type=click.STRING)
def show(bridge_name: str) -> bool:
    """
    Show the details of a bridge.

    e.g. kelvin bridge show "my-bridge"
    """
    from kelvin.sdk.interface import bridge_show

    return bridge_show(bridge_name=bridge_name, should_display=True).success


@bridge.command(cls=KSDKCommand)
@click.argument("bridge_name", nargs=1, type=click.STRING)
def assets(bridge_name: str) -> bool:
    """
    List all assets associated with a specific bridge.

    """
    from kelvin.sdk.interface import bridge_assets

    return bridge_assets(bridge_name=bridge_name, should_display=True).success


@bridge.command(cls=KSDKCommand)
@click.argument("bridge_name", nargs=1, type=click.STRING)
def streams(bridge_name: str) -> bool:
    """
    List all data streams associated with a specific bridge.

    """
    from kelvin.sdk.interface import bridge_streams

    return bridge_streams(bridge_name=bridge_name, should_display=True).success


@bridge.command(cls=KSDKCommand)
@click.argument("bridge_name", nargs=1, type=click.STRING)
def metrics(bridge_name: str) -> bool:
    """
    List all metrics associated with a specific bridge.

    """
    from kelvin.sdk.interface import bridge_metrics

    return bridge_metrics(bridge_name=bridge_name, should_display=True).success
