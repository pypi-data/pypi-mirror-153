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

from typeguard import typechecked

from kelvin.sdk.lib.models.operation import OperationResponse
from kelvin.sdk.lib.models.types import StatusDataSource


@typechecked
def node_list(should_display: bool = False) -> OperationResponse:
    """
    Returns the list of nodes available on the platform.

    Parameters
    ----------
    should_display: bool
        specifies whether or not the display should output data.

    Returns
    ----------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the nodes available on the platform.

    """
    from kelvin.sdk.lib.api.node import node_list as _node_list

    return _node_list(query=None, should_display=should_display)


@typechecked
def node_search(query: str, should_display: bool = False) -> OperationResponse:
    """
    Search for nodes on the platform that match the provided query.

    Parameters
    ----------
    query: str
        the query to search for.
    should_display: bool
        specifies whether or not the display should output data.

    Returns
    ----------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the matching nodes available on the platform.

    """
    from kelvin.sdk.lib.api.node import node_list as _node_list

    return _node_list(query=query, should_display=should_display)


@typechecked
def node_show(
    node_name: str, source: StatusDataSource = StatusDataSource.CACHE, should_display: bool = False
) -> OperationResponse:
    """
    Displays all the details of the specified node from the platform.

    Parameters
    ----------
    node_name: str
        the name of the node.
    source: StatusDataSource, Default=StatusDataSource.CACHE
        the status data source from where to obtain data.
    should_display: bool
        specifies whether or not the display should output data.

    Returns
    ----------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the yielded node instance and its detailed data.

    """
    from kelvin.sdk.lib.api.node import node_show as _node_show

    return _node_show(node_name=node_name, source=source, should_display=should_display)


@typechecked
def node_delete(node_name: str, ignore_destructive_warning: bool = False) -> OperationResponse:
    """
    Delete a node from the platform.

    Parameters
    ----------
    node_name: str
        the name of the node.
    ignore_destructive_warning: bool, Default=False
        indicates whether it should ignore the destructive warning.

    Returns
    ----------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the result of the node deletion operation.

    """
    from kelvin.sdk.lib.api.node import node_delete as _node_delete

    return _node_delete(node_name=node_name, ignore_destructive_warning=ignore_destructive_warning)


@typechecked
def node_provision_script() -> OperationResponse:
    """
    Get the provisioning script to setup a node.

    Returns
    ----------
    kelvin.sdk.lib.models.operation.OperationResponse
        an OperationResponse object encapsulating the node provision script.

    """
    from kelvin.sdk.lib.api.orchestration_provision import node_provision_script as _node_provision_script

    return _node_provision_script()
